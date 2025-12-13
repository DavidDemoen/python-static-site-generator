import unittest

from textnode_helpers import split_nodes_image, split_nodes_link, split_nodes_delimiter, text_to_textnodes
from textnode import TextNode, TextType

node_two_links = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,
)
node_text_only = TextNode("This is plain text with no links.", TextType.TEXT)

node_one_link_start = TextNode(
    "[first](https://a.com) with text after",
    TextType.TEXT,
)

node_one_link_end = TextNode(
    "Text before [first](https://a.com)",
    TextType.TEXT,
)

node_two_links_with_text = TextNode(
    "Start [first](https://a.com) middle [second](https://b.com) end",
    TextType.TEXT,
)

node_multiple_link_nodes = [
    TextNode("Node1 with [link1](https://x.com)", TextType.TEXT),
    TextNode("Node2 plain text", TextType.TEXT),
    TextNode("Node3 [link2](https://y.com) and [link3](https://z.com)", TextType.TEXT),
]

node_one_image = TextNode(
    "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
    TextType.TEXT,
)
node_only_one_image = TextNode(
    "![image](https://i.imgur.com/zjjcJKZ.png)",
    TextType.TEXT,
)
node_two_images = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
node_text_only = TextNode("This is plain text with no images.", TextType.TEXT)

node_one_image_start = TextNode(
    "![image](https://i.imgur.com/zjjcJKZ.png) with text after",
    TextType.TEXT,
)

node_one_image_end = TextNode(
    "Text before ![image](https://i.imgur.com/zjjcJKZ.png)",
    TextType.TEXT,
)

node_two_images_with_text = TextNode(
    "Start ![first](https://i.imgur.com/1.png) middle ![second](https://i.imgur.com/2.png) end",
    TextType.TEXT,
)

node_multiple_nodes = [
    TextNode("Node1 with ![img1](https://i.imgur.com/a.png)", TextType.TEXT),
    TextNode("Node2 plain text", TextType.TEXT),
    TextNode("Node3 ![img2](https://i.imgur.com/b.png) and ![img3](https://i.imgur.com/c.png)", TextType.TEXT),
]

# Mixed node
node_mixed = TextNode(
    "Text before ![img1](https://i.imgur.com/a.png) middle [link1](https://example.com) and ![img2](https://i.imgur.com/b.png) end",
    TextType.TEXT,
)


class TestMdTextNodeConvertor(unittest.TestCase):
    def test_md_code_one_node(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT),TextNode("code block", TextType.CODE),TextNode(" word", TextType.TEXT),])
    
    def test_node_one_image_start(self):
        new_nodes = split_nodes_image([node_one_image_start])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" with text after", TextType.TEXT),
            ],
        )

    def test_node_one_image_end(self):
        new_nodes = split_nodes_image([node_one_image_end])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
        )


    def test_md_code_two_nodes(self):
        node_01 = TextNode("This is text with a `code block` word", TextType.TEXT)
        node_02 = TextNode("This is a second text with a `second code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node_01, node_02], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT),TextNode("code block", TextType.CODE),TextNode(" word", TextType.TEXT),TextNode("This is a second text with a ", TextType.TEXT),TextNode("second code block", TextType.CODE),TextNode(" word", TextType.TEXT)])

    def test_md_bold_one_node(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT),TextNode("bold", TextType.BOLD),TextNode(" word", TextType.TEXT),])

    

class TestTextnodeImageHelper(unittest.TestCase):
    def test_one_node_one_image(self):
        new_nodes = split_nodes_image([node_one_image])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes
        )
    def test_one_node_only_one_image(self):
        new_nodes = split_nodes_image([node_only_one_image])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes
        )
    def test_one_node_two_images(self):
        new_nodes = split_nodes_image([node_two_images])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_node_two_images_with_text(self):
        new_nodes = split_nodes_image([node_two_images_with_text])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("first", TextType.IMAGE, "https://i.imgur.com/1.png"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("second", TextType.IMAGE, "https://i.imgur.com/2.png"),
                TextNode(" end", TextType.TEXT),
            ],
        )

    def test_multiple_img_nodes_mixed(self):
        new_nodes = split_nodes_image(node_multiple_nodes)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("Node1 with ", TextType.TEXT),
                TextNode("img1", TextType.IMAGE, "https://i.imgur.com/a.png"),
                TextNode("Node2 plain text", TextType.TEXT),
                TextNode("Node3 ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "https://i.imgur.com/b.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("img3", TextType.IMAGE, "https://i.imgur.com/c.png"),
            ],
        )

class TestTextnodeLinkHelperExtended(unittest.TestCase):

    def test_text_only_node(self):
        new_nodes = split_nodes_link([node_text_only])
        # No link → unchanged
        self.assertListEqual(new_nodes, [node_text_only])

    def test_node_one_link_start(self):
        new_nodes = split_nodes_link([node_one_link_start])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("first", TextType.LINK, "https://a.com"),
                TextNode(" with text after", TextType.TEXT),
            ],
        )

    def test_node_one_link_end(self):
        new_nodes = split_nodes_link([node_one_link_end])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("first", TextType.LINK, "https://a.com"),
            ],
        )

    def test_node_two_links_with_text(self):
        new_nodes = split_nodes_link([node_two_links_with_text])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("first", TextType.LINK, "https://a.com"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("second", TextType.LINK, "https://b.com"),
                TextNode(" end", TextType.TEXT),
            ],
        )

    def test_multiple_link_nodes_mixed(self):
        new_nodes = split_nodes_link(node_multiple_link_nodes)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("Node1 with ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "https://x.com"),
                TextNode("Node2 plain text", TextType.TEXT),
                TextNode("Node3 ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "https://y.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link3", TextType.LINK, "https://z.com"),
            ],
        )

class TestTextnodeMixedContent(unittest.TestCase):

    def test_split_images_only(self):
        """Ensure split_nodes_image only captures images and ignores links"""
        new_nodes = split_nodes_image([node_mixed])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("img1", TextType.IMAGE, "https://i.imgur.com/a.png"),
                TextNode(" middle [link1](https://example.com) and ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "https://i.imgur.com/b.png"),
                TextNode(" end", TextType.TEXT),
            ],
        )

    def test_split_links_only(self):
        """Ensure split_nodes_link only captures links and ignores images"""
        new_nodes = split_nodes_link([node_mixed])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("Text before ![img1](https://i.imgur.com/a.png) middle ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "https://example.com"),
                TextNode(" and ![img2](https://i.imgur.com/b.png) end", TextType.TEXT),
            ],
        )

generic_string = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"


class TestTextToTextnodes(unittest.TestCase):
    def test_generic_string(self):
        nodes = text_to_textnodes(generic_string)
        self.assertListEqual(
            [
    TextNode("This is ", TextType.TEXT),
    TextNode("text", TextType.BOLD),
    TextNode(" with an ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word and a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.TEXT),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", TextType.TEXT),
    TextNode("link", TextType.LINK, "https://boot.dev"),
], nodes
        )


if __name__ == "__main__":
    unittest.main()