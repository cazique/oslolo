
# tests/test_core.py
import pytest
from pathlib import Path
import zipfile
from oslolo.core.archive_manager import ArchiveManager

@pytest.fixture
def temp_archive(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    f = d / "hello.txt"
    f.write_text("hello world")
    
    zip_path = tmp_path / "test.zip"
    with zipfile.ZipFile(zip_path, 'w') as zf:
        zf.write(f, arcname="sub/hello.txt")
    
    return zip_path

def test_list_contents(temp_archive):
    manager = ArchiveManager()
    contents = list(manager.list_contents(str(temp_archive)))
    assert "sub/hello.txt" in contents

def test_extract(temp_archive, tmp_path):
    manager = ArchiveManager()
    extract_dir = tmp_path / "extracted"
    manager.extract(str(temp_archive), str(extract_dir))
    
    extracted_file = extract_dir / "sub" / "hello.txt"
    assert extracted_file.exists()
    assert extracted_file.read_text() == "hello world"

def test_create(tmp_path):
    manager = ArchiveManager()
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    (source_dir / "file1.txt").write_text("file1")
    
    archive_path = tmp_path / "new_archive.zip"
    manager.create(str(archive_path), [str(source_dir / "file1.txt")], format='zip')
    
    assert archive_path.exists()
    with zipfile.ZipFile(archive_path, 'r') as zf:
        assert "file1.txt" in zf.namelist()
