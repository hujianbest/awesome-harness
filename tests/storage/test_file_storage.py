"""Tests for file_storage module."""

import tempfile
from pathlib import Path

import pytest

from garage_os.storage.file_storage import FileStorage


@pytest.fixture
def temp_storage():
    """Create a temporary FileStorage instance."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield FileStorage(Path(tmpdir))


class TestFileStorage:
    """Test cases for FileStorage class."""

    def test_read_write_json(self, temp_storage):
        """Test CRUD operations on JSON files."""
        test_path = "test.json"
        data = {"key": "value", "number": 42}

        # Create
        checksum = temp_storage.write_json(test_path, data)
        assert isinstance(checksum, str)
        assert len(checksum) == 64

        # Read
        read_data = temp_storage.read_json(test_path)
        assert read_data == data

        # Update
        updated_data = {"key": "updated", "number": 100}
        temp_storage.write_json(test_path, updated_data)
        read_data = temp_storage.read_json(test_path)
        assert read_data == updated_data

        # Delete
        assert temp_storage.delete(test_path)
        assert temp_storage.read_json(test_path) is None

    def test_read_nonexistent(self, temp_storage):
        """Test reading a nonexistent file returns None."""
        assert temp_storage.read_json("nonexistent.json") is None
        assert temp_storage.read_text("nonexistent.txt") is None

    def test_write_creates_dirs(self, temp_storage):
        """Test that writing creates parent directories automatically."""
        nested_path = "level1/level2/test.json"
        data = {"nested": "data"}

        # Parent directories shouldn't exist
        assert not temp_storage.exists("level1/level2")

        # Write should create directories
        temp_storage.write_json(nested_path, data)

        # Verify directories were created and file exists
        assert temp_storage.exists(nested_path)
        read_data = temp_storage.read_json(nested_path)
        assert read_data == data

    def test_delete(self, temp_storage):
        """Test deleting files."""
        test_path = "to_delete.txt"
        temp_storage.write_text(test_path, "content")

        # Verify file exists
        assert temp_storage.exists(test_path)

        # Delete
        assert temp_storage.delete(test_path)
        assert not temp_storage.exists(test_path)

        # Delete nonexistent file returns False
        assert not temp_storage.delete(test_path)

    def test_list_files(self, temp_storage):
        """Test listing files in a directory."""
        # Create test files
        temp_storage.write_text("dir1/file1.txt", "content1")
        temp_storage.write_text("dir1/file2.txt", "content2")
        temp_storage.write_text("dir1/subdir/file3.txt", "content3")
        temp_storage.write_text("dir2/file4.json", '{"key": "value"}')

        # List all files in dir1
        files = temp_storage.list_files("dir1", "*.txt")
        file_names = [f.name for f in files]
        assert "file1.txt" in file_names
        assert "file2.txt" in file_names
        assert "file3.txt" not in file_names  # Not in direct dir1

        # List all files recursively
        files = temp_storage.list_files("dir1", "**/*.txt")
        assert len(files) >= 3

        # List nonexistent directory returns empty
        assert temp_storage.list_files("nonexistent") == []

    def test_move(self, temp_storage):
        """Test moving files and directories."""
        # Test moving a file
        temp_storage.write_text("source.txt", "content")
        assert temp_storage.exists("source.txt")

        result = temp_storage.move("source.txt", "destination.txt")
        assert result
        assert not temp_storage.exists("source.txt")
        assert temp_storage.exists("destination.txt")

        # Test moving to nested directory
        temp_storage.write_text("file2.txt", "content2")
        temp_storage.move("file2.txt", "nested/file2.txt")
        assert temp_storage.exists("nested/file2.txt")

        # Test moving nonexistent file returns False
        assert not temp_storage.move("nonexistent.txt", "dest.txt")

    def test_path_traversal_safety(self, temp_storage):
        """Test that relative path traversal is prevented."""
        data = {"test": "data"}

        # Test various path traversal attempts
        with pytest.raises(ValueError, match="Path traversal not allowed"):
            temp_storage.write_json("../outside.json", data)

        with pytest.raises(ValueError, match="Path traversal not allowed"):
            temp_storage.read_json("../../etc/passwd")

        with pytest.raises(ValueError, match="Path traversal not allowed"):
            temp_storage.list_files("../*")

        with pytest.raises(ValueError, match="Path traversal not allowed"):
            temp_storage.delete("../../../file")

    def test_text_operations(self, temp_storage):
        """Test reading and writing text files."""
        test_path = "text.txt"
        content = "Hello, World!\nLine 2"

        checksum = temp_storage.write_text(test_path, content)
        assert isinstance(checksum, str)

        # Read back
        read_content = temp_storage.read_text(test_path)
        assert read_content == content

    def test_ensure_dir(self, temp_storage):
        """Test ensuring directory exists."""
        dir_path = "new/nested/directory"

        # Directory shouldn't exist
        assert not temp_storage.exists(dir_path)

        # Ensure directory
        result = temp_storage.ensure_dir(dir_path)

        # Verify directory was created
        assert result.exists()
        assert result.is_dir()

        # Calling again should not fail
        result2 = temp_storage.ensure_dir(dir_path)
        assert result2 == result

    def test_exists(self, temp_storage):
        """Test checking file existence."""
        # Test with file
        temp_storage.write_text("file.txt", "content")
        assert temp_storage.exists("file.txt")
        assert not temp_storage.exists("nonexistent.txt")

        # Test with directory
        temp_storage.ensure_dir("directory")
        assert temp_storage.exists("directory")

    def test_write_with_unicode(self, temp_storage):
        """Test that Unicode content is handled correctly."""
        test_path = "unicode.txt"
        content = "Hello 世界 🌍 Привет"

        temp_storage.write_text(test_path, content)
        read_content = temp_storage.read_text(test_path)
        assert read_content == content

    def test_json_with_complex_data(self, temp_storage):
        """Test writing complex JSON data structures."""
        test_path = "complex.json"
        data = {
            "string": "value",
            "number": 42,
            "float": 3.14,
            "bool": True,
            "null": None,
            "list": [1, 2, 3],
            "nested": {"a": 1, "b": {"c": 2}},
        }

        temp_storage.write_json(test_path, data)
        read_data = temp_storage.read_json(test_path)
        assert read_data == data

    def test_multiple_writes_same_file(self, temp_storage):
        """Test that multiple writes to the same file work correctly."""
        test_path = "overwrite.txt"

        for i in range(5):
            content = f"Version {i}"
            temp_storage.write_text(test_path, content)
            read_content = temp_storage.read_text(test_path)
            assert read_content == content
