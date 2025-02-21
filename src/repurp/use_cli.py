#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
from typing import Any, cast

from .platform_specs import Platform, PlatformStyle, platform_specs, platforms
from .repurp import VideoRepurp


def validate_platform_style(platform: str, style: str) -> tuple[Platform, PlatformStyle]:
    """Validate platform and style arguments."""
    if platform not in platforms:
        raise ValueError(f"Invalid platform: {platform}. Choices: {', '.join(platforms)}")

    valid_styles = [k for k in platform_specs[platform].__annotations__.keys() if k not in ["max_duration", "bitrate"]]
    if style not in valid_styles:
        raise ValueError(f"Invalid style for {platform}: {style}. Choices: {', '.join(valid_styles)}")

    return platform, cast(PlatformStyle, style)


def cli_video_repurp(input_file: str, platform: str, style: str) -> None:
    """Reformat a video for a specific platform and style."""
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        sys.exit(1)

    try:
        video_repurp = VideoRepurp(input_file)
        platform, style = validate_platform_style(platform, style)
        output_file = video_repurp.repurp(cast(Any, platform), style)
        print(f"Reformatted video saved to: {output_file}")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


def cli_batch_repurp_video(input_file: str, batch_platforms: list[str]) -> None:
    """Batch repurpose a video for specified platforms."""
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        sys.exit(1)

    invalid_platforms = [p for p in batch_platforms if p not in platforms]
    if invalid_platforms:
        print(f"Error: Invalid platforms: {', '.join(invalid_platforms)}. Choices: {', '.join(platforms)}")
        sys.exit(1)

    try:
        video_repurp = VideoRepurp(input_file)
        outputs = video_repurp.batch_repurp(batch_platforms=cast(list[Platform], batch_platforms))
        print("Batch repurposing complete. Output files:")
        for key, output_file in outputs.items():
            print(f"  {key}: {output_file}")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Reformat videos for various platforms.",
        epilog="Example: video_repurp -i input.mp4 -p instagram -s story",
    )
    parser.add_argument("-i", "--input", required=True, help="Path to the input video file")
    parser.add_argument("-p", "--platform", help=f"Target platform ({', '.join(platforms)})")
    parser.add_argument("-s", "--style", help="Style for the platform (e.g., story, post, reel for instagram)")
    parser.add_argument(
        "-b",
        "--batch",
        nargs="*",
        default=None,
        help=f"Batch process for specified platforms (e.g., instagram tiktok). Default: all ({', '.join(platforms)})",
    )

    args = parser.parse_args()

    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: FFmpeg is not installed or not found in PATH. Please install FFmpeg.")
        sys.exit(1)

    if args.platform or args.style:
        if not (args.platform and args.style):
            parser.error("--platform and --style must both be provided for single-platform mode.")
        cli_video_repurp(args.input, args.platform, args.style)
    elif args.batch is not None:
        batch_platforms = args.batch if args.batch else cast(list[str], platforms)
        cli_batch_repurp_video(args.input, batch_platforms)
    else:
        parser.error("You must specify either --platform and --style, or --batch.")


if __name__ == "__main__":
    main()
