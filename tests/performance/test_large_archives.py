
# tests/performance/test_large_archives.py
import pytest
import os
from pathlib import Path
from oslolo.core.archive_manager import ArchiveManager

# This requires pytest-benchmark
# Create a large dummy file for testing
DUMMY_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
DUMMY_FILE_NAME = "large_file.bin"

@pytest.fixture(scope="module")
def large_file(tmp_path_factory):
    """Creates a large dummy file for benchmarking."""
    path = tmp_path_factory.mktemp("data") / DUMMY_FILE_NAME
    with open(path, "wb") as f:
        f.write(os.urandom(DUMMY_FILE_SIZE))
    return path

@pytest.mark.performance
def test_create_large_zip(benchmark, large_file, tmp_path):
    manager = ArchiveManager()
    archive_path = tmp_path / "large_archive.zip"
    
    def create_op():
        manager.create(str(archive_path), [str(large_file)], format='zip')

    benchmark(create_op)
    assert archive_path.exists()

@pytest.mark.performance
def test_extract_large_zip(benchmark, large_file, tmp_path):
    manager = ArchiveManager()
    archive_path = tmp_path / "large_archive.zip"
    # Create the archive first
    manager.create(str(archive_path), [str(large_file)], format='zip')

    extract_dir = tmp_path / "extracted"
    
    def extract_op():
        manager.extract(str(archive_path), str(extract_dir))

    benchmark(extract_op)
    extracted_file = extract_dir / DUMMY_FILE_NAME
    assert extracted_file.exists()
    assert extracted_file.stat().st_size == DUMMY_FILE_SIZE
