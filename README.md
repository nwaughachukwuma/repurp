# 🎬 Repurp

> 🚀 Effortlessly repurpose videos for Instagram, Twitter, TikTok, Broadcast and more!

Repurp is a powerful library and command-line tool that helps you repurpose your videos for various social media platforms, ensuring the best quality and format for each platform's requirements.

## ✨ Features

- 📱 Support for multiple platforms:
  - Instagram (Story, Post, Reel)
  - TikTok
  - Twitter (Landscape, Square)
  - LinkedIn (Landscape, Square)
  - Broadcast (Standard, Closeup)
- 🎯 Platform-specific optimizations
- 🔄 Batch processing for multiple platforms
- ⚡ Optimized FFmpeg settings for quality and performance
- 🛠️ Easy-to-use command line interface

## 🔧 Prerequisites

Before using Repurp, ensure you have the following installed:

- 🎥 FFmpeg (required for video processing)
- 🐍 Python 3.8 or higher

## 📦 Installation

### From PyPI (Recommended)

```bash
pip install repurp
```

### From Source

```bash
git clone https://github.com/veedoai/repurp.git
cd repurp
pip install .
```

### As Executable

Download the latest release for your platform from the [releases page](https://github.com/veedoai/repurp/releases).

## 🚀 Usage

### As a Library

```python
from repurp import VideoRepurp

# Initialize with input video
video = VideoRepurp("input_video.mp4")

# Process for a specific platform and style
instagram_story = video.repurp("instagram", "story")
twitter_post = video.repurp("twitter", "landscape")

# Batch process for multiple platforms
outputs = video.batch_repurp(batch_platforms=["instagram", "tiktok", "twitter"])

# Get platform specifications
instagram_specs = video.get_platform_spec("instagram")
```

The library provides type-safe methods with platform-specific optimizations:
- Supports major social platforms (Instagram, TikTok, Twitter, LinkedIn)
- Supports Broadcast formats (Standard, Closeup)
- Automatically creates an 'output' directory next to your input video
- Returns paths to processed video files
- Handles proper video scaling, padding, and encoding for each platform

### CLI Basic Usage

```bash
# Repurpose a video for Instagram Story
repurp -i video.mp4 -p instagram -s story

# Repurpose for Twitter in landscape format
repurp -i video.mp4 -p twitter -s landscape
```

### Batch Processing

```bash
# Process for all supported platforms
repurp -i video.mp4 -b

# Process for specific platforms
repurp -i video.mp4 -b instagram twitter
```

### Convert Video for Instagram Story

```bash
repurp -i my_video.mp4 -p instagram -s story
```

### Batch Process for Multiple Social Media

```bash
repurp -i my_video.mp4 -b instagram tiktok twitter
```

### Create Broadcast-Ready Version

```bash
repurp -i my_video.mp4 -p broadcast -s standard
```

### CLI Options

```
Options:
  -i, --input     Path to the input video file (required)
  -p, --platform  Target platform (instagram, tiktok, twitter, linkedin, broadcast)
  -s, --style     Style for the platform (e.g., story, post, reel for instagram)
  -b, --batch     Batch process for specified platforms
  -h, --help      Show this help message
```

### Platform-Specific Styles

- Instagram: `story`, `post`, `reel`
- TikTok: `standard`
- Twitter: `landscape`, `square`
- LinkedIn: `landscape`, `square`
- Broadcast: `standard`, `closeup`

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

> Please make sure to update tests as appropriate and follow the existing coding style.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- FFmpeg for providing the powerful video processing capabilities
