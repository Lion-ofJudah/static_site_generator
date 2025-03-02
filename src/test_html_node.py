import unittest

from html_node import HTMLNode, LeafNode, ParentNode

# from textnode import TextNode, TextType


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props = HTMLNode().props_to_html()
        expected_props = ""
        props2 = HTMLNode(
            tag="p", value="Hello world", children=[], props={"style": "color: orange"}
        ).props_to_html()
        expected_props2 = ' style="color: orange"'
        self.assertEqual(props, expected_props)
        self.assertEqual(props2, expected_props2)


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode(tag=None, value="Hello world").to_html()
        node2 = LeafNode(tag="p", value="Hello world").to_html()
        node3 = LeafNode(
            value="Hello world", tag="a", props={"href": "www.hello.world.com"}
        ).to_html()
        self.assertEqual(node, "Hello world")
        self.assertEqual(node2, "<p>Hello world</p>")
        self.assertEqual(node3, '<a href="www.hello.world.com">Hello world</a>')


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            tag="div",
            children=[
                LeafNode(tag="b", value="Hello world"),
                ParentNode(
                    tag="div", children=[LeafNode(tag="p", value="Hello world")]
                ),
                LeafNode(tag="b", value="Bold text"),
                LeafNode(tag=None, value="Normal text"),
                LeafNode(tag="i", value="italic text"),
                LeafNode(tag=None, value="Normal text"),
            ],
        ).to_html()
        expected_html = "<div><b>Hello world</b><div><p>Hello world</p></div><b>Bold text</b>Normal text<i>italic text</i>Normal text</div>"
        self.assertEqual(node, expected_html)


if __name__ == "__main__":
    unittest.main()
