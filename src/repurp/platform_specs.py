from __future__ import annotations  # Enables future type hints in Python 3.8+
from dataclasses import dataclass
from typing import Dict, List, Literal, Tuple, Optional

Platform = Literal["instagram", "tiktok", "twitter", "linkedin", "broadcast", "youtube", "facebook", "vimeo", "rumble"]
platforms: List[Platform] = [
    "instagram",
    "tiktok",
    "twitter",
    "linkedin",
    "broadcast",
    "youtube",
    "facebook",
    "vimeo",
    "rumble",
]


InstagramStyle = Literal["story", "post", "reel"]
TikTokStyle = Literal["standard"]
TwitterStyle = Literal["landscape", "square"]
LinkedInStyle = Literal["landscape", "square"]
BroadcastStyle = Literal["standard", "closeup"]
YouTubeStyle = Literal["standard", "shorts"]
FacebookStyle = Literal["post", "story"]
VimeoStyle = Literal["standard"]
RumbleStyle = Literal["standard"]

PlatformStyle = Literal[
    InstagramStyle,
    TikTokStyle,
    TwitterStyle,
    LinkedInStyle,
    BroadcastStyle,
    YouTubeStyle,
    FacebookStyle,
    VimeoStyle,
    RumbleStyle,
]

PlatformStyles = {
    "instagram": InstagramStyle,
    "tiktok": TikTokStyle,
    "twitter": TwitterStyle,
    "linkedin": LinkedInStyle,
    "broadcast": BroadcastStyle,
    "youtube": YouTubeStyle,
    "facebook": FacebookStyle,
    "vimeo": VimeoStyle,
    "rumble": RumbleStyle,
}

Dimensions = Tuple[int, int]


@dataclass
class PlatformSpec:
    bitrate: str
    max_duration: Optional[int] = None
    story: Optional[Dimensions] = None
    post: Optional[Dimensions] = None
    reel: Optional[Dimensions] = None
    standard: Optional[Dimensions] = None
    landscape: Optional[Dimensions] = None
    square: Optional[Dimensions] = None
    closeup: Optional[Dimensions] = None
    shorts: Optional[Dimensions] = None


platform_specs: Dict[Platform, PlatformSpec] = {
    "instagram": PlatformSpec(
        story=(1080, 1920),
        post=(1080, 1080),
        reel=(1080, 1920),
        max_duration=60,
        bitrate="4M",
    ),
    "tiktok": PlatformSpec(
        standard=(1080, 1920),
        max_duration=180,
        bitrate="4M",
    ),
    "twitter": PlatformSpec(
        landscape=(1920, 1080),
        square=(720, 720),
        max_duration=140,
        bitrate="2M",
    ),
    "linkedin": PlatformSpec(
        landscape=(1920, 1080),
        square=(1080, 1080),
        max_duration=600,
        bitrate="5M",
    ),
    "broadcast": PlatformSpec(
        standard=(1920, 1080),
        closeup=(1920, 1080),
        bitrate="20M",
    ),
    "youtube": PlatformSpec(
        standard=(1920, 1080),
        shorts=(1080, 1920),
        max_duration=600,
        bitrate="10M",
    ),
    "facebook": PlatformSpec(
        post=(1080, 1080),
        story=(1080, 1920),
        max_duration=240,
        bitrate="4M",
    ),
    "vimeo": PlatformSpec(
        standard=(1920, 1080),
        bitrate="5M",
    ),
    "rumble": PlatformSpec(
        standard=(1920, 1080),
        bitrate="5M",
    ),
}


# Create instances of the dataclasses
instagram = platform_specs["instagram"]
tiktok = platform_specs["tiktok"]
twitter = platform_specs["twitter"]
linkedin = platform_specs["linkedin"]
broadcast = platform_specs["broadcast"]
youtube = platform_specs["youtube"]
facebook = platform_specs["facebook"]
vimeo = platform_specs["vimeo"]
rumble = platform_specs["rumble"]

# Example usage
# Now you can access the attributes using dot notation
# print(instagram.story)  # Output: (1080, 1920)
# print(tiktok.max_duration)  # Output: 180
# print(twitter.bitrate)  # Output: 2M
# print(linkedin.landscape)  # Output: (1920, 1080)
# print(broadcast.closeup)  # Output: (1920, 1080)
