import os
import subprocess
from typing import Dict, List, Literal, overload, Tuple

from .platform_specs import (
    BroadcastStyle,
    InstagramStyle,
    LinkedInStyle,
    Platform,
    PlatformStyle,
    TikTokStyle,
    TwitterStyle,
    platform_specs,
    platforms,
)


class VideoRepurp:
    def __init__(self, input_file: str):
        self.input_file = input_file

        output_dir = os.path.join(os.path.dirname(input_file), "output")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        self.output_dir = output_dir

    # Overloaded function signatures for precise type checking
    @overload
    def repurp(self, platform: Literal["instagram"], style: InstagramStyle) -> str: ...

    @overload
    def repurp(self, platform: Literal["tiktok"], style: TikTokStyle) -> str: ...

    @overload
    def repurp(self, platform: Literal["twitter"], style: TwitterStyle) -> str: ...

    @overload
    def repurp(self, platform: Literal["linkedin"], style: LinkedInStyle) -> str: ...

    @overload
    def repurp(self, platform: Literal["broadcast"], style: BroadcastStyle) -> str: ...

    def repurp(self, platform: Platform, style: PlatformStyle) -> str:
        """Process video for specific platform and style with optimized performance."""
        if platform not in platform_specs:
            raise ValueError(f"Unsupported platform: {platform}")

        platform_spec = platform_specs[platform]
        output_file = os.path.join(
            self.output_dir, f"{os.path.splitext(os.path.basename(self.input_file))[0]}_{platform}_{style}.mp4"
        )

        if style not in platform_spec.__annotations__:
            raise ValueError(f"Unsupported style {style} for platform {platform}")

        # Get target dimensions
        dimensions: Tuple[int, int] = getattr(platform_spec, style)
        width, height = dimensions

        # Base FFmpeg command with optimizations
        command = [
            "ffmpeg",
            "-threads",
            "0",  # Use all available CPU cores
            "-i",
            self.input_file,
            "-c:v",
            "libx264",
            "-crf",
            "23",  # Use CRF for better quality and faster encoding
            "-preset",
            "veryfast",  # Optimize for speed
            "-tune",
            "fastdecode",
            "-profile:v",
            "high",
            "-movflags",
            "+faststart",
            "-c:a",
            "aac",
            "-b:v",
            platform_spec.bitrate,
            "-b:a",
            "128k",  # Ensure good audio quality
        ]

        # Platform-specific video transformations
        if platform in ["instagram", "tiktok"]:
            # Vertical video processing with optimized scaling
            command.extend(
                [
                    "-vf",
                    f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
                    f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1",
                ]
            )
        elif platform in ["twitter", "linkedin"] and style == "square":
            # Square video processing
            command.extend(
                [
                    "-vf",
                    f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
                    f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1",
                ]
            )
        elif platform == "broadcast" and style == "closeup":
            # Broadcast closeup (center crop with zoom)
            command.extend(["-vf", "scale=2304:1296,crop=1920:1080:192:108,setsar=1"])
        else:
            # Standard landscape processing
            command.extend(
                [
                    "-vf",
                    f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
                    f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1",
                ]
            )

        # Add output file
        command.append(output_file)

        # Execute FFmpeg command
        subprocess.run(command, check=True)
        return output_file

    def batch_repurp(self, batch_platforms: List[Platform] = platforms) -> Dict[str, str]:
        """Process video for all platforms and styles."""
        outputs = {}

        # Instagram
        if "instagram" in batch_platforms:
            outputs["instagram_story"] = self.repurp("instagram", "story")
            outputs["instagram_post"] = self.repurp("instagram", "post")
            outputs["instagram_reel"] = self.repurp("instagram", "reel")

        # TikTok
        if "tiktok" in batch_platforms:
            outputs["tiktok"] = self.repurp("tiktok", "standard")

        # Twitter/LinkedIn
        if "twitter" in batch_platforms:
            outputs["twitter_landscape"] = self.repurp("twitter", "landscape")
            outputs["twitter_square"] = self.repurp("twitter", "square")
            outputs["linkedin_landscape"] = self.repurp("linkedin", "landscape")
            outputs["linkedin_square"] = self.repurp("linkedin", "square")

        # Broadcast
        if "broadcast" in batch_platforms:
            outputs["broadcast_standard"] = self.repurp("broadcast", "standard")
            outputs["broadcast_closeup"] = self.repurp("broadcast", "closeup")

        return outputs

    def get_platform_spec(self, platform: Platform):
        """Get platform specs"""
        if platform not in platform_specs:
            raise ValueError(f"Unsupported platform: {platform}")

        return platform_specs[platform]


# Example usage
# if __name__ == "__main__":
#     # Initialize VideoRepurp
#     video_repurp = VideoRepurp("input_video.mp4")

#     # Reformat for specific platform
#     instagram_story = video_repurp.repurp("instagram", "story")

#     # Reformat for all platforms
#     outputs = video_repurp.batch_repurp(batch_platforms=["broadcast", "instagram", "tiktok"])
