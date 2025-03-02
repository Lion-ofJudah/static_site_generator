import re
from enum import Enum

from inline_markdown import text_to_text_nodes
from text_node import text_node_to_html_node
from html_node import ParentNode, LeafNode


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str):
    blocks = re.split(r"\n\s*\n", markdown)
    return [block for block in blocks if block.strip()]


def block_to_block_type(block: str):
    lines = block.split("\n")

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if len(lines) > 0:
        # Unordered List
        if all(re.match(r"^[*\-]\s", line) for line in lines):
            return BlockType.UNORDERED_LIST

        # Ordered List (check sequential numbering)
        ordered = True
        for i, line in enumerate(lines):
            if not re.match(rf"^{i+1}\.\s", line):
                ordered = False
                break
        if ordered:
            return BlockType.ORDERED_LIST

    if re.match(r"^#{1,6}\s", block):
        return BlockType.HEADING

    return BlockType.PARAGRAPH


def text_to_children(text: str):
    text_nodes = text_to_text_nodes(text)
    return [text_node_to_html_node(node) for node in text_nodes if node]


def parent_tag(block_type: BlockType):
    return {
        BlockType.PARAGRAPH: "p",
        BlockType.HEADING: "h",
        BlockType.CODE: "pre",
        BlockType.QUOTE: "blockquote",
        BlockType.UNORDERED_LIST: "ul",
        BlockType.ORDERED_LIST: "ol",
    }.get(block_type, "div")


def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown=markdown)
    html_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block=block)
        tag = parent_tag(block_type=block_type)

        if block_type == BlockType.HEADING:
            match = re.match(r"^(#+)\s+(.*)", block)
            if not match:
                raise ValueError(f"Invalid heading format: {block}")
            level = len(match.group(1))
            content = match.group(2)
            tag = f"h{level}"

            html_nodes.append(ParentNode(tag, text_to_children(content)))

        elif block_type == BlockType.CODE:
            code_content = block.strip("```").split("\n", 1)[-1].strip()
            code_node = LeafNode(tag="code", value=code_content)
            html_nodes.append(ParentNode("pre", [code_node]))

        elif block_type in (BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST):
            items = []
            for line in block.split("\n"):
                parts = re.split(r"^[*\-]\s+|\d+\.\s+", line, 1)
                content = parts[1] if len(parts) > 1 else ""
                children = text_to_children(content)
                items.append(ParentNode("li", children))
            tag = "ul" if block_type == BlockType.UNORDERED_LIST else "ol"
            html_nodes.append(ParentNode(tag, items))

        elif block_type == BlockType.QUOTE:
            lines = [line.lstrip("> ").strip() for line in block.split("\n")]
            quote_content = " ".join(lines)
            children = text_to_children(quote_content)
            html_nodes.append(ParentNode("blockquote", children))

        else:
            children = text_to_children(block)
            html_nodes.append(ParentNode("p", children))

    return ParentNode(tag="div", children=html_nodes)


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown=markdown)
    h1_headings = []

    for block in blocks:
        block_type = block_to_block_type(block=block)
        if block_type != BlockType.HEADING:
            continue

        match = re.match(r"^#\s+(.*?)\s*$", block, re.IGNORECASE)
        if match:
            h1_headings.append(match.group(1).strip())

    if len(h1_headings) == 0:
        raise ValueError("No H1 heading found in markdown")
    if len(h1_headings) > 1:
        raise ValueError(f"Multiple H1 headings found: {h1_headings}")

    return h1_headings[0]
