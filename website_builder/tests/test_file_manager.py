import pytest
from pathlib import Path
import tempfile
import os
from website_builder.utils.file_manager import FileManager

@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname

@pytest.fixture
def file_manager(temp_dir):
    """Create a FileManager instance with a temporary directory."""
    return FileManager(output_dir=temp_dir)

def test_file_manager_initialization(file_manager, temp_dir):
    """Test FileManager initialization."""
    assert file_manager.output_dir == Path(temp_dir)
    assert file_manager.output_dir.exists()

def test_write_and_read_file(file_manager):
    """Test writing and reading files."""
    test_content = "Hello, World!"
    filename = "test.txt"
    
    # Write file
    file_path = file_manager.write_file(filename, test_content)
    assert file_path.exists()
    assert file_path.read_text() == test_content
    
    # Read file
    content = file_manager.read_file(filename)
    assert content == test_content

def test_file_exists(file_manager):
    """Test file existence check."""
    filename = "test.txt"
    assert not file_manager.file_exists(filename)
    
    file_manager.write_file(filename, "test")
    assert file_manager.file_exists(filename)

def test_invalid_file_operations(file_manager):
    """Test error handling for invalid file operations."""
    # Test reading non-existent file
    with pytest.raises(IOError):
        file_manager.read_file("nonexistent.txt")
    
    # Test writing to invalid path
    with pytest.raises(IOError):
        file_manager.write_file("/invalid/path/test.txt", "test") 