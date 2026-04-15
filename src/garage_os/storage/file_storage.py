"""File storage operations with locking support."""

import json
from pathlib import Path
from typing import Any, Optional, List
from filelock import FileLock, Timeout
from .atomic_writer import AtomicWriter


class FileStorage:
    """File system storage with atomic writes and file locking."""

    # Default timeout for file lock acquisition (seconds)
    DEFAULT_LOCK_TIMEOUT = 10.0

    def __init__(self, base_path: Path):
        """Initialize file storage with a base path.

        Args:
            base_path: Root directory for file storage operations
        """
        self.base_path = base_path

    def _get_full_path(self, relative_path: str) -> Path:
        """Get full path from relative path.

        Args:
            relative_path: Relative path from base_path

        Returns:
            Full absolute path

        Raises:
            ValueError: If path contains .. (path traversal attempt)
        """
        # Path traversal safety check
        if ".." in relative_path.split("/") or ".." in relative_path.split("\\"):
            raise ValueError("Path traversal not allowed: '..' in path")

        return self.base_path / relative_path

    def _get_lock_path(self, file_path: Path) -> Path:
        """Get lock file path for a given file.

        Args:
            file_path: Path to the file

        Returns:
            Path to the lock file
        """
        return file_path.with_suffix(file_path.suffix + ".lock")

    def read_json(self, relative_path: str) -> Optional[dict]:
        """Read JSON file. Returns None if not exists.

        Args:
            relative_path: Relative path to JSON file

        Returns:
            Parsed JSON data as dict, or None if file doesn't exist
        """
        full_path = self._get_full_path(relative_path)

        if not full_path.exists():
            return None

        return AtomicWriter.read_json(full_path)

    def write_json(self, relative_path: str, data: dict) -> str:
        """Write JSON atomically with lock. Returns checksum.

        Args:
            relative_path: Relative path to JSON file
            data: Data to write

        Returns:
            SHA-256 checksum of written content
        """
        full_path = self._get_full_path(relative_path)
        lock_path = self._get_lock_path(full_path)

        # Acquire lock for atomic write
        with FileLock(lock_path, timeout=self.DEFAULT_LOCK_TIMEOUT):
            return AtomicWriter.write_json(full_path, data)

    def write_text(self, relative_path: str, content: str) -> str:
        """Write text atomically with lock. Returns checksum.

        Args:
            relative_path: Relative path to text file
            content: Text content to write

        Returns:
            SHA-256 checksum of written content
        """
        full_path = self._get_full_path(relative_path)
        lock_path = self._get_lock_path(full_path)

        # Acquire lock for atomic write
        with FileLock(lock_path, timeout=self.DEFAULT_LOCK_TIMEOUT):
            return AtomicWriter.write_text(full_path, content)

    def read_text(self, relative_path: str) -> Optional[str]:
        """Read text file. Returns None if not exists.

        Args:
            relative_path: Relative path to text file

        Returns:
            File content as string, or None if file doesn't exist
        """
        full_path = self._get_full_path(relative_path)

        if not full_path.exists():
            return None

        return full_path.read_text(encoding="utf-8")

    def exists(self, relative_path: str) -> bool:
        """Check if file exists.

        Args:
            relative_path: Relative path to check

        Returns:
            True if file exists, False otherwise
        """
        full_path = self._get_full_path(relative_path)
        return full_path.exists()

    def delete(self, relative_path: str) -> bool:
        """Delete file. Returns True if file existed.

        Args:
            relative_path: Relative path to file

        Returns:
            True if file existed and was deleted, False otherwise
        """
        full_path = self._get_full_path(relative_path)

        if not full_path.exists():
            return False

        full_path.unlink()
        return True

    def list_files(self, relative_dir: str, pattern: str = "*") -> List[Path]:
        """List files in directory matching pattern.

        Args:
            relative_dir: Relative path to directory
            pattern: Glob pattern to match files (default: "*")

        Returns:
            List of matching file paths (relative to base_path)
        """
        full_dir = self._get_full_path(relative_dir)

        if not full_dir.exists():
            return []

        # Path traversal safety check for pattern
        if ".." in pattern:
            raise ValueError("Path traversal not allowed in pattern")

        return list(full_dir.glob(pattern))

    def ensure_dir(self, relative_path: str) -> Path:
        """Ensure directory exists.

        Args:
            relative_path: Relative path to directory

        Returns:
            Full path to the directory
        """
        full_path = self._get_full_path(relative_path)
        full_path.mkdir(parents=True, exist_ok=True)
        return full_path

    def move(self, src: str, dst: str) -> bool:
        """Move file/dir atomically.

        Args:
            src: Source relative path
            dst: Destination relative path

        Returns:
            True if move succeeded, False otherwise

        Raises:
            ValueError: If paths contain traversal attempts
        """
        src_path = self._get_full_path(src)
        dst_path = self._get_full_path(dst)

        if not src_path.exists():
            return False

        # Ensure destination directory exists
        dst_path.parent.mkdir(parents=True, exist_ok=True)

        # Atomic rename/move
        src_path.rename(dst_path)
        return True
