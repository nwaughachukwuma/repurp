import os
import subprocess
import pytest
from repurp.repurp import VideoRepurp


def test_init_creates_output_dir(temp_video, mock_makedirs):
    """Test that VideoRepurp creates output directory on initialization"""
    video = VideoRepurp(temp_video)
    expected_output_dir = os.path.join(os.path.dirname(temp_video), "output")
    mock_makedirs.assert_called_once_with(expected_output_dir)
    assert video.output_dir == expected_output_dir


def test_repurp_instagram_story(temp_video, mock_subprocess_run, mock_makedirs):
    """Test video repurposing for Instagram story"""
    video = VideoRepurp(temp_video)
    output_file = video.repurp("instagram", "story")
    
    # Verify FFmpeg command
    mock_subprocess_run.assert_called_once()
    args = mock_subprocess_run.call_args[0][0]
    
    # Check essential FFmpeg parameters
    assert args[0] == "ffmpeg"
    assert "-i" in args and args[args.index("-i") + 1] == temp_video
    assert "-b:v" in args and args[args.index("-b:v") + 1] == "4M"
    
    # Check output dimensions for Instagram story (1080x1920)
    vf_idx = args.index("-vf")
    assert "1080:1920" in args[vf_idx + 1]
    
    # Verify output path
    assert output_file.endswith("_instagram_story.mp4")


def test_repurp_twitter_landscape(temp_video, mock_subprocess_run, mock_makedirs):
    """Test video repurposing for Twitter landscape"""
    video = VideoRepurp(temp_video)
    output_file = video.repurp("twitter", "landscape")
    
    # Verify FFmpeg command
    mock_subprocess_run.assert_called_once()
    args = mock_subprocess_run.call_args[0][0]
    
    # Check essential FFmpeg parameters
    assert "-b:v" in args and args[args.index("-b:v") + 1] == "2M"
    
    # Check output dimensions for Twitter landscape (1920x1080)
    vf_idx = args.index("-vf")
    assert "1920:1080" in args[vf_idx + 1]
    
    # Verify output path
    assert output_file.endswith("_twitter_landscape.mp4")


def test_batch_repurp(temp_video, mock_subprocess_run, mock_makedirs):
    """Test batch processing for multiple platforms"""
    video = VideoRepurp(temp_video)
    outputs = video.batch_repurp(["instagram", "tiktok"])
    
    # Should have multiple outputs for Instagram (story, post, reel) and TikTok (standard)
    assert "instagram_story" in outputs
    assert "instagram_post" in outputs
    assert "instagram_reel" in outputs
    assert "tiktok" in outputs
    
    # Verify FFmpeg was called multiple times
    assert mock_subprocess_run.call_count == 4


def test_invalid_platform(temp_video, mock_makedirs):
    """Test error handling for invalid platform"""
    video = VideoRepurp(temp_video)
    with pytest.raises(ValueError, match="Unsupported platform: invalid_platform"):
        video.repurp("invalid_platform", "story")  # type: ignore


def test_invalid_style(temp_video, mock_makedirs):
    """Test error handling for invalid style"""
    video = VideoRepurp(temp_video)
    with pytest.raises(ValueError, match="Unsupported style invalid_style for platform instagram"):
        video.repurp("instagram", "invalid_style")  # type: ignore


def test_get_platform_spec(temp_video, mock_makedirs):
    """Test getting platform specifications"""
    video = VideoRepurp(temp_video)
    spec = video.get_platform_spec("instagram")
    assert spec.story == (1080, 1920)
    assert spec.bitrate == "4M"
    
    with pytest.raises(ValueError, match="Unsupported platform"):
        video.get_platform_spec("invalid_platform")  # type: ignore


def test_ffmpeg_error_handling(temp_video, mock_subprocess_run, mock_makedirs):
    """Test handling of FFmpeg execution errors"""
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, "ffmpeg")
    video = VideoRepurp(temp_video)
    
    with pytest.raises(subprocess.CalledProcessError):
        video.repurp("instagram", "story")
