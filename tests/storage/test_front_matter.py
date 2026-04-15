"""Tests for front_matter module."""

import tempfile
from pathlib import Path

import pytest

from garage_os.storage.front_matter import FrontMatterParser


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


class TestFrontMatterParser:
    """Test cases for FrontMatterParser class."""

    def test_parse_basic(self, temp_dir):
        """Test basic front matter parsing."""
        content = """---
title: Test Title
author: John Doe
---

This is the body content."""

        front_matter, body = FrontMatterParser.parse(content)

        assert front_matter == {"title": "Test Title", "author": "John Doe"}
        assert body == "This is the body content."

    def test_parse_no_front_matter(self, temp_dir):
        """Test parsing content without front matter raises ValueError."""
        content = "This is just markdown without front matter."

        with pytest.raises(ValueError, match="No valid YAML front matter found"):
            FrontMatterParser.parse(content)

    def test_parse_complex_yaml(self, temp_dir):
        """Test parsing complex YAML structures."""
        content = """---
title: Complex Document
tags:
  - python
  - testing
  - yaml
metadata:
  created: "2024-01-01"
  nested:
    value: 42
    items:
      - a
      - b
---

Body content here."""

        front_matter, body = FrontMatterParser.parse(content)

        assert front_matter["title"] == "Complex Document"
        assert front_matter["tags"] == ["python", "testing", "yaml"]
        assert front_matter["metadata"]["created"] == "2024-01-01"
        assert front_matter["metadata"]["nested"]["value"] == 42
        assert front_matter["metadata"]["nested"]["items"] == ["a", "b"]
        assert body == "Body content here."

    def test_render(self, temp_dir):
        """Test rendering front matter and body."""
        front_matter = {"title": "Test", "author": "Jane"}
        body = "Content here"

        rendered = FrontMatterParser.render(front_matter, body)

        assert rendered.startswith("---")
        assert "---" in rendered[4:]  # Second set of dashes
        assert "title: Test" in rendered
        assert "author: Jane" in rendered
        assert rendered.endswith("Content here")

    def test_round_trip(self, temp_dir):
        """Test that parse -> render -> parse produces same result."""
        original_content = """---
title: Original Title
tags:
  - one
  - two
---

Original body content."""

        # Parse
        front_matter_1, body_1 = FrontMatterParser.parse(original_content)

        # Render
        rendered = FrontMatterParser.render(front_matter_1, body_1)

        # Parse again
        front_matter_2, body_2 = FrontMatterParser.parse(rendered)

        # Should be identical
        assert front_matter_1 == front_matter_2
        assert body_1 == body_2

    def test_write_and_read_file(self, temp_dir):
        """Test writing and reading a file with front matter."""
        test_file = temp_dir / "test.md"
        front_matter = {"title": "File Test", "version": 1}
        body = "# Heading\n\nContent"

        # Write file
        FrontMatterParser.write_file(test_file, front_matter, body)

        # Read file
        read_front_matter, read_body = FrontMatterParser.parse_file(test_file)

        assert read_front_matter == front_matter
        assert read_body == body

    def test_parse_empty_front_matter(self, temp_dir):
        """Test parsing content with empty front matter."""
        content = """---
---

Body here."""

        front_matter, body = FrontMatterParser.parse(content)

        assert front_matter == {}
        assert body == "Body here."

    def test_parse_multiline_body(self, temp_dir):
        """Test parsing content with multiline body."""
        content = """---
title: Multi-line Test
---

# Header

Paragraph 1.

Paragraph 2.

- List item 1
- List item 2
"""

        front_matter, body = FrontMatterParser.parse(content)

        assert front_matter == {"title": "Multi-line Test"}
        assert "# Header" in body
        assert "Paragraph 1." in body
        assert "- List item 1" in body

    def test_parse_file_not_found(self, temp_dir):
        """Test parsing nonexistent file raises FileNotFoundError."""
        nonexistent_file = temp_dir / "nonexistent.md"

        with pytest.raises(FileNotFoundError):
            FrontMatterParser.parse_file(nonexistent_file)

    def test_parse_invalid_yaml(self, temp_dir):
        """Test parsing invalid YAML in front matter raises ValueError."""
        content = """---
title: [unclosed bracket
---

Body."""

        with pytest.raises(ValueError, match="Invalid YAML in front matter"):
            FrontMatterParser.parse(content)

    def test_render_empty_front_matter(self, temp_dir):
        """Test rendering with empty front matter."""
        rendered = FrontMatterParser.render({}, "Body content")

        # yaml.dump({}) outputs "{}\n"
        assert "---\n{}\n---\nBody content" == rendered

    def test_front_matter_with_special_characters(self, temp_dir):
        """Test front matter with special characters."""
        content = r"""---
title: "Title with \"quotes\""
description: Text with \n newlines
emoji: 😀🎉
---

Body content."""

        front_matter, body = FrontMatterParser.parse(content)

        assert 'Title with "quotes"' == front_matter["title"]
        assert body == "Body content."

    def test_parse_preserve_body_formatting(self, temp_dir):
        """Test that body formatting is preserved."""
        content = """---
title: Formatting Test
---

# Header 1

## Header 2

**Bold** and *italic*.

```python
code block
```
"""

        front_matter, body = FrontMatterParser.parse(content)

        assert "# Header 1" in body
        assert "## Header 2" in body
        assert "**Bold**" in body
        assert "*italic*" in body
        assert "```python" in body
        assert "code block" in body

    def test_render_with_list_values(self, temp_dir):
        """Test rendering front matter with list values."""
        front_matter = {"items": ["one", "two", "three"]}
        body = "Content"

        rendered = FrontMatterParser.render(front_matter, body)

        # Parse back to verify
        parsed_front_matter, _ = FrontMatterParser.parse(rendered)
        assert parsed_front_matter["items"] == ["one", "two", "three"]

    def test_render_with_nested_dict(self, temp_dir):
        """Test rendering front matter with nested dictionaries."""
        front_matter = {
            "metadata": {"author": "Test", "version": 1, "nested": {"key": "value"}}
        }
        body = "Content"

        rendered = FrontMatterParser.render(front_matter, body)

        # Parse back to verify
        parsed_front_matter, _ = FrontMatterParser.parse(rendered)
        assert parsed_front_matter["metadata"]["author"] == "Test"
        assert parsed_front_matter["metadata"]["nested"]["key"] == "value"
