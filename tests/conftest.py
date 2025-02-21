import pytest
from unittest.mock import patch
from pathlib import Path


@pytest.fixture
def mock_subprocess_run():
    """Mock subprocess.run to avoid actual FFmpeg calls"""
    with patch("subprocess.run") as mock_run:
        yield mock_run


@pytest.fixture
def temp_video(tmp_path: Path):
    """Create a temporary video file path"""
    video_path = tmp_path / "test_video.mp4"
    # Create empty file
    video_path.touch()
    return str(video_path)


@pytest.fixture
def output_dir(tmp_path: Path):
    """Create a temporary output directory"""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return str(output_dir)


@pytest.fixture
def mock_makedirs():
    """Mock os.makedirs to avoid directory creation"""
    with patch("os.makedirs") as mock_mk:
        yield mock_mk
