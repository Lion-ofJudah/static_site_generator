from enum import Enum

from html_node import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    NONE = "none"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, text_node):
        return (
            isinstance(text_node, TextNode)
            and self.text == text_node.text
            and self.text_type == text_node.text_type
            and self.url == text_node.url
        )

    def __repr__(self):
        text = self.text if self.text else ""
        text_type = ", " + self.text_type.value if self.text_type else ""
        url = ", " + self.url if self.url else ""

        return f"TextNode({text}{text_type}{url})"


def text_node_to_html_node(text_node: TextNode):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(
            tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
        )
    else:
        raise ValueError(f"Invalid text type: {text_node.text_type}")
