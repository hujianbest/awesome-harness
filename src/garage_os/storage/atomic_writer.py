"""Atomic file writing with checksum support."""

import json
import hashlib
import tempfile
from pathlib import Path
from typing import Any, Optional, Union
import os


class AtomicWriter:
    """Write files atomically using temp file + rename pattern."""

    @staticmethod
    def write_text(path: Path, content: str, encoding: str = "utf-8") -> str:
        """Write text file atomically. Returns SHA-256 checksum.

        Args:
            path: Target file path
            content: Text content to write
            encoding: File encoding (default: utf-8)

        Returns:
            SHA-256 checksum of the written content
        """
        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)

        # Compute checksum before writing
        checksum = AtomicWriter.compute_checksum(content)

        # Write to temporary file in the same directory
        # This ensures the temp file is on the same filesystem
        fd, temp_path = tempfile.mkstemp(dir=path.parent, prefix=".tmp_")
        try:
            # Write content to temp file
            with os.fdopen(fd, "w", encoding=encoding) as f:
                f.write(content)
                f.flush()
                os.fsync(f.fileno())  # Ensure data is written to disk

            # Atomic rename to replace target file
            os.replace(temp_path, path)
        except Exception:
            # Clean up temp file if something went wrong
            try:
                os.unlink(temp_path)
            except OSError:
                pass
            raise

        return checksum

    @staticmethod
    def write_json(
        path: Path, data: Any, indent: int = 2, ensure_ascii: bool = False
    ) -> str:
        """Write JSON file atomically. Returns SHA-256 checksum.

        Args:
            path: Target file path
            data: Python object to serialize as JSON
            indent: JSON indentation (default: 2)
            ensure_ascii: Whether to escape non-ASCII characters (default: False)

        Returns:
            SHA-256 checksum of the written content
        """
        json_content = json.dumps(data, indent=indent, ensure_ascii=ensure_ascii)
        return AtomicWriter.write_text(path, json_content)

    @staticmethod
    def read_json(path: Path) -> Any:
        """Read JSON file with basic validation.

        Args:
            path: Path to JSON file

        Returns:
            Parsed JSON data

        Raises:
            FileNotFoundError: If file doesn't exist
            json.JSONDecodeError: If file contains invalid JSON
        """
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def compute_checksum(content: str) -> str:
        """Compute SHA-256 checksum of content.

        Args:
            content: String content to hash

        Returns:
            Hexadecimal SHA-256 checksum
        """
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    @staticmethod
    def verify_checksum(path: Path, expected_checksum: str) -> bool:
        """Verify file content matches expected checksum.

        Args:
            path: Path to file to verify
            expected_checksum: Expected SHA-256 checksum

        Returns:
            True if checksums match, False otherwise
        """
        try:
            with path.open("r", encoding="utf-8") as f:
                content = f.read()
            actual_checksum = AtomicWriter.compute_checksum(content)
            return actual_checksum == expected_checksum
        except (OSError, UnicodeDecodeError):
            return False
