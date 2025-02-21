import pytest
from unittest.mock import patch, Mock
from repurp.use_cli import (
    validate_platform_style,
    cli_video_repurp,
    cli_batch_repurp_video,
    main,
)


def test_validate_platform_style_valid():
    """Test platform and style validation with valid inputs"""
    platform, style = validate_platform_style("instagram", "story")
    assert platform == "instagram"
    assert style == "story"


def test_validate_platform_style_invalid_platform():
    """Test validation with invalid platform"""
    with pytest.raises(ValueError, match="Invalid platform: invalid_platform."):
        validate_platform_style("invalid_platform", "story")


def test_validate_platform_style_invalid_style():
    """Test validation with invalid style"""
    with pytest.raises(ValueError, match="Invalid style for instagram: invalid_style."):
        validate_platform_style("instagram", "invalid_style")


def test_cli_video_repurp_success(temp_video, mock_subprocess_run):
    """Test successful single platform video processing"""
    with patch("sys.exit") as mock_exit:
        cli_video_repurp(temp_video, "instagram", "story")
        mock_exit.assert_not_called()


def test_cli_video_repurp_missing_file(mock_subprocess_run):
    """Test error handling for missing input file"""
    with patch("sys.exit") as mock_exit:
        cli_video_repurp("nonexistent.mp4", "instagram", "story")
        mock_exit.assert_called_once_with(1)


def test_cli_video_repurp_error(temp_video, mock_subprocess_run):
    """Test error handling for processing errors"""
    with patch("repurp.repurp.VideoRepurp.repurp", side_effect=Exception("Processing error")):
        with patch("sys.exit") as mock_exit:
            cli_video_repurp(temp_video, "instagram", "story")
            mock_exit.assert_called_once_with(1)


def test_cli_batch_repurp_success(temp_video, mock_subprocess_run):
    """Test successful batch processing"""
    with patch("sys.exit") as mock_exit:
        cli_batch_repurp_video(temp_video, ["instagram", "tiktok"])
        mock_exit.assert_not_called()


def test_cli_batch_repurp_invalid_platform(temp_video, mock_subprocess_run):
    """Test batch processing with invalid platform"""
    with patch("sys.exit") as mock_exit:
        cli_batch_repurp_video(temp_video, ["instagram", "invalid_platform"])
        mock_exit.assert_called_once_with(1)


@pytest.mark.parametrize(
    "args,should_exit",
    [
        (["-i", "video.mp4", "-p", "instagram", "-s", "story"], False),
        (["-i", "video.mp4", "-b", "instagram", "tiktok"], False),
        (["-i", "video.mp4", "-p", "instagram"], True),  # Missing style
        (["-i", "video.mp4", "-s", "story"], True),  # Missing platform
        (["-i", "video.mp4"], True),  # No mode specified
    ],
)
def test_main_argument_parsing(args, should_exit):
    """Test main function argument parsing"""
    with patch("sys.argv", ["repurp"] + args):
        with patch("subprocess.run") as mock_ffmpeg:
            mock_ffmpeg.return_value = Mock(returncode=0)
            with patch("repurp.use_cli.cli_video_repurp") as mock_single:
                with patch("repurp.use_cli.cli_batch_repurp_video") as mock_batch:
                    if should_exit:
                        with pytest.raises(SystemExit):
                            main()
                    else:
                        main()
                        assert mock_single.called or mock_batch.called


def test_main_ffmpeg_check():
    """Test FFmpeg availability check"""
    with patch("sys.argv", ["repurp", "-i", "video.mp4", "-p", "instagram", "-s", "story"]):
        with patch("subprocess.run", side_effect=FileNotFoundError):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1


def test_main_batch_all_platforms(temp_video, mock_subprocess_run):
    """Test batch processing with no specified platforms (should use all)"""
    with patch("sys.argv", ["repurp", "-i", temp_video, "-b"]):
        with patch("repurp.use_cli.cli_batch_repurp_video") as mock_batch:
            main()
            # Verify called with all platforms
            args = mock_batch.call_args[0]
            assert len(args[1]) == len(["instagram", "tiktok", "twitter", "linkedin", "broadcast"])
