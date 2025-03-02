import unittest

from block import BlockType, block_to_block_type, markdown_to_html_node, extract_title


class TestBlock(unittest.TestCase):
    def test_block_to_block_type(self):
        markdown = "This is a paragraph"
        markdown2 = "1. This is an ordered list"
        markdown3 = "* This is an unordered list"
        markdown4 = "```This is a code block```"
        markdown5 = ">This is a quote"
        markdown6 = "# This is a heading"
        markdown7 = "## This is also a heading"
        markdown8 = "#This is a paragraph"
        expected = BlockType.PARAGRAPH
        expected2 = BlockType.ORDERED_LIST
        expected3 = BlockType.UNORDERED_LIST
        expected4 = BlockType.CODE
        expected5 = BlockType.QUOTE
        expected6 = BlockType.HEADING
        expected7 = BlockType.HEADING
        expected8 = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(markdown), expected)
        self.assertEqual(block_to_block_type(markdown2), expected2)
        self.assertEqual(block_to_block_type(markdown3), expected3)
        self.assertEqual(block_to_block_type(markdown4), expected4)
        self.assertEqual(block_to_block_type(markdown5), expected5)
        self.assertEqual(block_to_block_type(markdown6), expected6)
        self.assertEqual(block_to_block_type(markdown7), expected7)
        self.assertEqual(block_to_block_type(markdown8), expected8)

    def test_empty_input(self):
        md = ""
        result = markdown_to_html_node(md)
        self.assertEqual(result.to_html(), "<div></div>")

    def test_paragraphs(self):
        md = """This is a paragraph
        
And another paragraph"""
        expected = "<div><p>This is a paragraph</p><p>And another paragraph</p></div>"
        self.assertEqual(markdown_to_html_node(md).to_html(), expected)

    def test_headings(self):
        md = """# H1

## H2

### H3"""
        expected = "<div><h1>H1</h1><h2>H2</h2><h3>H3</h3></div>"
        self.assertEqual(markdown_to_html_node(md).to_html(), expected)

    def test_code_block(self):
        md = """```
print('Hello World')
```"""
        expected = "<div><pre><code>print('Hello World')</code></pre></div>"
        self.assertEqual(markdown_to_html_node(md).to_html(), expected)

    def test_quote_block(self):
        md = """> First quote line
> Second quote line"""
        expected = (
            "<div><blockquote>First quote line Second quote line</blockquote></div>"
        )
        self.assertEqual(markdown_to_html_node(md).to_html(), expected)

    def test_unordered_list(self):
        md = """* Item 1
- Item 2"""
        expected = "<div><ul><li>Item 1</li><li>Item 2</li></ul></div>"
        self.assertEqual(markdown_to_html_node(md).to_html(), expected)

    def test_ordered_list(self):
        md = """1. First
2. Second"""
        expected = "<div><ol><li>First</li><li>Second</li></ol></div>"
        self.assertEqual(markdown_to_html_node(md).to_html(), expected)

    def test_mixed_content(self):
        md = """# Header

Paragraph with **bold** text

- List item 1
- List item 2"""

        expected = (
            "<div>"
            "<h1>Header</h1>"
            "<p>Paragraph with <b>bold</b> text</p>"
            "<ul><li>List item 1</li><li>List item 2</li></ul>"
            "</div>"
        )
        self.assertEqual(markdown_to_html_node(md).to_html(), expected)

    def test_inline_formatting(self):
        md = "Paragraph with *italic* and `code`"
        expected = (
            "<div><p>Paragraph with <i>italic</i> and <code>code</code></p></div>"
        )
        self.assertEqual(markdown_to_html_node(md).to_html(), expected)


class TestExtractTitle(unittest.TestCase):
    def test_valid_title(self):
        md = """# My Awesome Title
        
## Subheading
Some content"""
        self.assertEqual(extract_title(md), "My Awesome Title")

    def test_no_title(self):
        md = """## Not a Title
        This document has no H1"""
        with self.assertRaises(ValueError) as context:
            extract_title(md)
        self.assertIn("No H1 heading found", str(context.exception))

    def test_multiple_titles(self):
        md = """# First Title

# Second Title"""
        with self.assertRaises(ValueError) as context:
            extract_title(md)
        self.assertIn("Multiple H1 headings found", str(context.exception))
        self.assertIn("First Title", str(context.exception))
        self.assertIn("Second Title", str(context.exception))

    def test_case_insensitivity(self):
        md = """# TITLE IN UPPERCASE"""
        self.assertEqual(extract_title(md), "TITLE IN UPPERCASE")

    def test_inline_formatting(self):
        md = """# Title with **bold** and *italic*"""
        self.assertEqual(extract_title(md), "Title with **bold** and *italic*")

    def test_other_headings(self):
        md = """## Not a Title

# Actual Title

### Another Heading"""
        self.assertEqual(extract_title(md), "Actual Title")

    def test_title_not_first(self):
        md = """Some content

# The Real Title"""
        self.assertEqual(extract_title(md), "The Real Title")

    def test_multiline_title(self):
        md = """# Title spanning
        multiple lines"""
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_code_block_title(self):
        md = """```
        # Not a title
        ```

# Actual Title"""
        self.assertEqual(extract_title(md), "Actual Title")


if __name__ == "__main__":
    unittest.main()
