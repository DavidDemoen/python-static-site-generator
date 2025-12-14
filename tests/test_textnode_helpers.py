import unittest

from src.textnode import TextNode, TextType
from src.textnode_helpers import split_nodes_delimiter, split_nodes_link, split_nodes_image


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_single_delimiter_basic(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_backtick_code_block(self):
        node = TextNode("Use `code` here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(
            new_nodes,
            [
                TextNode("Use ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" here", TextType.TEXT),
            ],
        )

    def test_italic_with_underscore(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_multiple_delimiters_in_one_text_node(self):
        node = TextNode("**Bold** and **strong** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("", TextType.TEXT),
                TextNode("Bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("strong", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_non_text_nodes_are_unchanged(self):
        nodes = [
            TextNode("Hello", TextType.TEXT),
            TextNode("Bold", TextType.BOLD),
        ]

        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)

        self.assertEqual(new_nodes, nodes)

    def test_multiple_input_nodes(self):
        nodes = [
            TextNode("Hello **world**", TextType.TEXT),
            TextNode("Another **test**", TextType.TEXT),
        ]

        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("world", TextType.BOLD),
                TextNode("", TextType.TEXT),
                TextNode("Another ", TextType.TEXT),
                TextNode("test", TextType.BOLD),
                TextNode("", TextType.TEXT),
            ],
        )

    def test_delimiter_at_start(self):
        node = TextNode("**Bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("", TextType.TEXT),
                TextNode("Bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_delimiter_at_end(self):
        node = TextNode("Text **bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("Text ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode("", TextType.TEXT),
            ],
        )

    def test_adjacent_delimiters(self):
        node = TextNode("**bold****bold2**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode("", TextType.TEXT),
                TextNode("bold2", TextType.BOLD),
                TextNode("", TextType.TEXT),
            ],
        )

    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(new_nodes, [node])

    def test_unmatched_delimiter_raises(self):
        node = TextNode("This is **broken", TextType.TEXT)

class TestSplitNodesLink(unittest.TestCase):
    def test_single_link(self):
        node = TextNode("Check out [Boot.dev](https://www.boot.dev)!", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check out ", TextType.TEXT),
                TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
                TextNode("!", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_multiple_links(self):
        node = TextNode(
            "Links: [Boot](https://www.boot.dev) and [YouTube](https://youtube.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Links: ", TextType.TEXT),
                TextNode("Boot", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("YouTube", TextType.LINK, "https://youtube.com"),
            ],
            new_nodes,
        )

    def test_link_at_start(self):
        node = TextNode("[Start](https://start.com) of text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Start", TextType.LINK, "https://start.com"),
                TextNode(" of text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_link_at_end(self):
        node = TextNode("End of text [End](https://end.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("End of text ", TextType.TEXT),
                TextNode("End", TextType.LINK, "https://end.com"),
            ],
            new_nodes,
        )

    def test_no_links(self):
        node = TextNode("Plain text with no links.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_link_with_special_chars(self):
        node = TextNode(
            "Click [here!](https://example.com/?q=test&lang=en)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Click ", TextType.TEXT),
                TextNode("here!", TextType.LINK, "https://example.com/?q=test&lang=en"),
            ],
            new_nodes,
        )

    def test_multiple_input_nodes(self):
        nodes = [
            TextNode("First [Link](https://first.com)", TextType.TEXT),
            TextNode("Second [Link](https://second.com)", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("First ", TextType.TEXT),
                TextNode("Link", TextType.LINK, "https://first.com"),
                TextNode("Second ", TextType.TEXT),
                TextNode("Link", TextType.LINK, "https://second.com"),
            ],
            new_nodes,
        )

    def test_non_text_nodes_unchanged(self):
        # Already a LINK node should remain unchanged
        node = TextNode("Link", TextType.LINK, "https://example.com")
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

class TestSplitNodesImage(unittest.TestCase):
    def test_single_image(self):
        node = TextNode("Here is an image: ![Alt text](https://example.com/image.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Here is an image: ", TextType.TEXT),
                TextNode("Alt text", TextType.IMAGE, "https://example.com/image.png"),
            ],
            new_nodes,
        )

    def test_multiple_images(self):
        node = TextNode(
            "Images: ![Img1](https://img1.com) and ![Img2](https://img2.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Images: ", TextType.TEXT),
                TextNode("Img1", TextType.IMAGE, "https://img1.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("Img2", TextType.IMAGE, "https://img2.com"),
            ],
            new_nodes,
        )

    def test_no_images(self):
        node = TextNode("Just some text without images.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_image_with_special_chars(self):
        node = TextNode(
            "Check this image: ![Alt-text_123](https://example.com/path/image-name_1.0.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Check this image: ", TextType.TEXT),
                TextNode("Alt-text_123", TextType.IMAGE, "https://example.com/path/image-name_1.0.png"),
            ],
            new_nodes,
        )
    def test_multiple_input_nodes(self):
        nodes = [
            TextNode("First image ![Img1](https://img1.com)", TextType.TEXT),
            TextNode("Second image ![Img2](https://img2.com)", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("First image ", TextType.TEXT),
                TextNode("Img1", TextType.IMAGE, "https://img1.com"),
                TextNode("Second image ", TextType.TEXT),
                TextNode("Img2", TextType.IMAGE, "https://img2.com"),
            ],
            new_nodes,
        )
    def test_non_text_nodes_unchanged(self):
        # Already an IMAGE node should remain unchanged
        node = TextNode("Alt text", TextType.IMAGE, "https://example.com/image.png")
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

if __name__ == "__main__":
    unittest.main()
