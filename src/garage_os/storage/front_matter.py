"""YAML front matter parsing for markdown files."""

import re
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
import yaml

# Regex pattern for YAML front matter
# Matches: ---\n<yaml content>\n---
FRONT_MATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n?---\s*\n?(.*)$", re.DOTALL)


class FrontMatterParser:
    """Parse and write YAML front matter in markdown files."""

    @staticmethod
    def parse(content: str) -> Tuple[Dict[str, Any], str]:
        """Parse front matter from markdown content.

        Args:
            content: Markdown file content

        Returns:
            Tuple of (front_matter_dict, body_text)

        Raises:
            ValueError: If no valid front matter found
        """
        match = FRONT_MATTER_PATTERN.match(content)

        if not match:
            raise ValueError("No valid YAML front matter found in content")

        yaml_text = match.group(1)
        body = match.group(2)

        try:
            front_matter = yaml.safe_load(yaml_text)
            if front_matter is None:
                front_matter = {}
            return front_matter, body
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in front matter: {e}") from e

    @staticmethod
    def parse_file(path: Path) -> Tuple[Dict[str, Any], str]:
        """Parse front matter from a markdown file.

        Args:
            path: Path to markdown file

        Returns:
            Tuple of (front_matter_dict, body_text)

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If no valid front matter found
        """
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        content = path.read_text(encoding="utf-8")
        return FrontMatterParser.parse(content)

    @staticmethod
    def render(front_matter: Dict[str, Any], body: str) -> str:
        """Render front matter + body into a complete markdown string.

        Args:
            front_matter: Dictionary of front matter attributes
            body: Markdown body content

        Returns:
            Complete markdown string with front matter
        """
        yaml_content = yaml.dump(
            front_matter, default_flow_style=False, sort_keys=False
        ).rstrip("\n")
        return f"---\n{yaml_content}\n---\n{body}"

    @staticmethod
    def write_file(path: Path, front_matter: Dict[str, Any], body: str) -> None:
        """Write a markdown file with front matter atomically.

        Args:
            path: Target file path
            front_matter: Dictionary of front matter attributes
            body: Markdown body content
        """
        # Import here to avoid circular dependency
        from .atomic_writer import AtomicWriter

        content = FrontMatterParser.render(front_matter, body)
        AtomicWriter.write_text(path, content)
