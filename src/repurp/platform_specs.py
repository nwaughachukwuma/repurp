from dataclasses import dataclass
from typing import Dict, List, Literal, Tuple

Platform = Literal["instagram", "tiktok", "twitter", "linkedin", "broadcast"]

platforms: List[Platform] = ["instagram", "tiktok", "twitter", "linkedin", "broadcast"]


InstagramStyle = Literal["story", "post", "reel"]
TikTokStyle = Literal["standard"]
TwitterStyle = Literal["landscape", "square"]
LinkedInStyle = Literal["landscape", "square"]
BroadcastStyle = Literal["standard", "closeup"]

PlatformStyle = Literal[InstagramStyle, TikTokStyle, TwitterStyle, LinkedInStyle, BroadcastStyle]

PlatformStyles = {
    "instagram": InstagramStyle,
    "tiktok": TikTokStyle,
    "twitter": TwitterStyle,
    "linkedin": LinkedInStyle,
    "broadcast": BroadcastStyle,
}

Dimensions = Tuple[int, int]


@dataclass
class PlatformSpec:
    bitrate: str
    max_duration: int | None = None
    story: Dimensions | None = None
    post: Dimensions | None = None
    reel: Dimensions | None = None
    standard: Dimensions | None = None
    landscape: Dimensions | None = None
    square: Dimensions | None = None
    closeup: Dimensions | None = None


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
}


# Create instances of the dataclasses
instagram = platform_specs["instagram"]

tiktok = platform_specs["tiktok"]

twitter = platform_specs["twitter"]

linkedin = platform_specs["linkedin"]

broadcast = platform_specs["broadcast"]

# Example usage
# Now you can access the attributes using dot notation
# print(instagram.story)  # Output: (1080, 1920)
# print(tiktok.max_duration)  # Output: 180
# print(twitter.bitrate)  # Output: 2M
# print(linkedin.landscape)  # Output: (1920, 1080)
# print(broadcast.closeup)  # Output: (1920, 1080)
