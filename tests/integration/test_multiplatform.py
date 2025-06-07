
# tests/integration/test_multiplatform.py
import pytest
import platform
from pathlib import Path
from oslolo.core.archive_manager import ArchiveManager

@pytest.mark.integration
def test_path_handling_on_current_os(tmp_path):
    """
    Tests that creating and extracting an archive with platform-specific paths works.
    """
    manager = ArchiveManager()
    
    # Create a path structure that might be tricky
    source_dir = tmp_path / "src"
    file_path = source_dir / "a file with spaces.txt"
    source_dir.mkdir()
    file_path.write_text("test")
    
    archive_path = tmp_path / "test_paths.zip"
    
    # Create
    manager.create(str(archive_path), [str(file_path)], format='zip')
    
    # Extract
    extract_dir = tmp_path / "out"
    manager.extract(str(archive_path), str(extract_dir))
    
    expected_file = extract_dir / file_path.name
    
    assert expected_file.exists()
    assert expected_file.read_text() == "test"
    
@pytest.mark.skipif(platform.system() != "Windows", reason="Test for Windows-specific paths")
def test_windows_long_paths():
    # Placeholder for a test that would create paths > 260 chars on Windows
    # This requires specific setup and is complex to demonstrate here.
    pass
