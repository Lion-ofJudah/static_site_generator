import unittest

from text_node import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_link,
    split_nodes_image,
    text_to_text_nodes,
)


class TestSplitDelimiter(unittest.TestCase):
    def test_split_node_delimiter(self):
        text = "This is text with a **bolded phrase** in the middle"
        result = split_nodes_delimiter(
            old_nodes=[TextNode(text=text, text_type=TextType.TEXT)],
            delimiter="**",
            text_type=TextType.BOLD,
        )
        expected = [
            TextNode(text="This is text with a ", text_type=TextType.TEXT),
            TextNode(text="bolded phrase", text_type=TextType.BOLD),
            TextNode(text=" in the middle", text_type=TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image(self):
        node = TextNode(
            text="This is a text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            text_type=TextType.TEXT,
        )
        expected = [
            TextNode(
                text="This is a text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                text_type=TextType.TEXT,
            )
        ]
        node2 = TextNode(
            text="This is a text with image ![Hello](https://hello.world.com) and a link [to boot dev](https://www.boot.dev)",
            text_type=TextType.TEXT,
        )
        expected2 = [
            TextNode(text="This is a text with image ", text_type=TextType.TEXT),
            TextNode(
                text="Hello", text_type=TextType.IMAGE, url="https://hello.world.com"
            ),
            TextNode(
                text=" and a link [to boot dev](https://www.boot.dev)",
                text_type=TextType.TEXT,
            ),
        ]
        self.assertEqual(split_nodes_image([node]), expected)
        self.assertEqual(split_nodes_image([node2]), expected2)

    def test_split_nodes_links(self):
        node = TextNode(
            text="This is a text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            text_type=TextType.TEXT,
        )
        expected = [
            TextNode(text="This is a text with a link ", text_type=TextType.TEXT),
            TextNode(
                text="to boot dev", text_type=TextType.LINK, url="https://www.boot.dev"
            ),
            TextNode(text=" and ", text_type=TextType.TEXT),
            TextNode(
                text="to youtube",
                text_type=TextType.LINK,
                url="https://www.youtube.com/@bootdotdev",
            ),
        ]
        self.assertEqual(split_nodes_link([node]), expected)

    def test_text_to_text_nodes(self):
        node = text_to_text_nodes(
            text="This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        expected = [
            TextNode(text="This is ", text_type=TextType.TEXT),
            TextNode(text="text", text_type=TextType.BOLD),
            TextNode(text=" with an ", text_type=TextType.TEXT),
            TextNode(text="italic", text_type=TextType.ITALIC),
            TextNode(text=" word and a ", text_type=TextType.TEXT),
            TextNode(text="code block", text_type=TextType.CODE),
            TextNode(text=" and an ", text_type=TextType.TEXT),
            TextNode(
                text="obi wan image",
                text_type=TextType.IMAGE,
                url="https://i.imgur.com/fJRm4Vk.jpeg",
            ),
            TextNode(text=" and a ", text_type=TextType.TEXT),
            TextNode(text="link", text_type=TextType.LINK, url="https://boot.dev"),
        ]
        self.assertEqual(node, expected)


if __name__ == "__main__":
    unittest.main()
