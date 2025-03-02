import unittest

from text_node import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.BOLD, "https://google.com")
        node4 = TextNode("This is a text node", TextType.BOLD, "https://google.com")
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertEqual(node3, node4)

    def test_text_node_to_html_node(self):
        node = text_node_to_html_node(
            TextNode("Hello", TextType.IMAGE, "www.example.com")
        ).to_html()
        expected_html = '<img src="www.example.com" alt="Hello"></img>'
        self.assertEqual(node, expected_html)


if __name__ == "__main__":
    unittest.main()
