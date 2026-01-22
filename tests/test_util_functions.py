import unittest 
from src.textnode import TextNode, TextType
from src.util_functions import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link


class TestTexNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("Plain text", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Plain text")
        self.assertIsNone(html_node.props)

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertIsNone(html_node.props)

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertIsNone(html_node.props)

    def test_code(self):
        node = TextNode("Code snippet", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code snippet")
        self.assertIsNone(html_node.props)

    def test_link(self):
        node = TextNode("Click here", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertIsNotNone(html_node.props)
        self.assertIn("href", html_node.props)
        self.assertEqual(html_node.props["href"], "https://example.com")

    def test_image(self):
        node = TextNode("Alt text", TextType.IMAGE, "image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertIsNotNone(html_node.props)
        self.assertIn("src", html_node.props)
        self.assertEqual(html_node.props["src"], "image.png")
        self.assertIn("alt", html_node.props)
        self.assertEqual(html_node.props["alt"], "Alt text")

    def test_invalid_type(self):
        class FakeTextType:
            pass

        node = TextNode("Invalid", FakeTextType())
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(node)
        self.assertIn("Invalid TextType", str(context.exception))

    def test_all_text_types(self):
        # Define a list of test cases: (TextType, text, url, expected_tag, expected_value, expected_props)
        test_cases = [
            (TextType.TEXT, "Plain text", None, None, "Plain text", None),
            (TextType.BOLD, "Bold text", None, "b", "Bold text", None),
            (TextType.ITALIC, "Italic text", None, "i", "Italic text", None),
            (TextType.CODE, "Code snippet", None, "code", "Code snippet", None),
            (TextType.LINK, "Click me", "https://example.com", "a", "Click me", {"href": "https://example.com"}),
            (TextType.IMAGE, "Alt text", "image.png", "img", "", {"src": "image.png", "alt": "Alt text"}),
        ]

        for text_type, text, url, expected_tag, expected_value, expected_props in test_cases:
            with self.subTest(text_type=text_type):
                node = TextNode(text, text_type, url)
                html_node = text_node_to_html_node(node)

                self.assertEqual(html_node.tag, expected_tag)
                self.assertEqual(html_node.value, expected_value)
                if expected_props is None:
                    self.assertIsNone(html_node.props)
                else:
                    self.assertEqual(html_node.props, expected_props)

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_basic_code_split(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, expected)

    def test_multiple_code_blocks(self):
        node = TextNode("`code1` and `code2`", TextType.TEXT)
        expected = [
            TextNode("code1", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("code2", TextType.CODE),
        ]
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, expected)

    def test_missing_closing_delimiter(self):
        node = TextNode("Text with `unclosed code", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_no_delimiters(self):
        node = TextNode("Just plain text", TextType.TEXT)
        expected = [TextNode("Just plain text", TextType.TEXT)]
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, expected)

    def test_non_text_nodes_skipped(self):
        node1 = TextNode("Hello ", TextType.TEXT)
        node2 = TextNode("bold", TextType.BOLD)
        node3 = TextNode(" world", TextType.TEXT)
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" world", TextType.TEXT),
        ]
        result = split_nodes_delimiter([node1, node2, node3], "`", TextType.CODE)
        self.assertEqual(result, expected)

    def test_bold_split(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, expected)

    def test_italic_split(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(result, expected)

    def test_nested_delimiters(self):
        node = TextNode("`code with **bold** inside`", TextType.TEXT)
        expected = [
            TextNode("code with **bold** inside", TextType.CODE)
        ]
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, expected)

    def test_adjacent_delimiters(self):
        node = TextNode("**bold1****bold2**", TextType.TEXT)
        expected = [
            TextNode("bold1", TextType.BOLD),
            TextNode("bold2", TextType.BOLD),
        ]
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, expected)

    def test_delimiter_at_start_and_end(self):
        node = TextNode("`code`", TextType.TEXT)
        expected = [TextNode("code", TextType.CODE)]
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, expected)

class TestMarkdownExtraction(unittest.TestCase):

    # --- Images ---
    def test_single_image(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(extract_markdown_images(text), expected)

    def test_multiple_images(self):
        text = (
            "Here is ![img1](https://example.com/1.png) "
            "and ![img2](https://example.com/2.jpg)"
        )
        expected = [
            ("img1", "https://example.com/1.png"),
            ("img2", "https://example.com/2.jpg"),
        ]
        self.assertListEqual(extract_markdown_images(text), expected)

    def test_no_images(self):
        text = "This has no images at all"
        expected = []
        self.assertListEqual(extract_markdown_images(text), expected)

    def test_image_with_empty_alt(self):
        text = "Here is an image ![](https://example.com/empty.png)"
        expected = [("", "https://example.com/empty.png")]
        self.assertListEqual(extract_markdown_images(text), expected)

    def test_image_with_special_characters_in_alt(self):
        text = "Check ![hello_world-123](https://example.com/img.png)"
        expected = [("hello_world-123", "https://example.com/img.png")]
        self.assertListEqual(extract_markdown_images(text), expected)

    # --- Links ---
    def test_single_link(self):
        text = "Go to [Boot.dev](https://www.boot.dev)"
        expected = [("Boot.dev", "https://www.boot.dev")]
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_multiple_links(self):
        text = (
            "Links: [Google](https://google.com) and [YouTube](https://youtube.com)"
        )
        expected = [
            ("Google", "https://google.com"),
            ("YouTube", "https://youtube.com"),
        ]
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_no_links(self):
        text = "Just plain text, no links."
        expected = []
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_link_with_special_characters(self):
        text = "Visit [user-page](https://example.com/user_123)"
        expected = [("user-page", "https://example.com/user_123")]
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_link_and_image_combined(self):
        text = (
            "![img](https://example.com/img.png) and [link](https://example.com)"
        )
        self.assertListEqual(
            extract_markdown_images(text), [("img", "https://example.com/img.png")]
        )
        self.assertListEqual(
            extract_markdown_links(text), [("link", "https://example.com")]
        )

    def test_links_not_confused_with_images(self):
        text = "![image](https://img.com) [link](https://link.com)"
        self.assertListEqual(
            extract_markdown_links(text), [("link", "https://link.com")]
        )
        self.assertListEqual(
            extract_markdown_images(text), [("image", "https://img.com")]
        )

class TestSplitNodesImage(unittest.TestCase):

    def test_single_image(self):
        node = TextNode(
            "This is text with an ![image](https://example.com/img.png)",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
            ],
            result,
        )

    def test_multiple_images(self):
        node = TextNode(
            "Start ![one](url1) middle ![two](url2) end",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("one", TextType.IMAGE, "url1"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("two", TextType.IMAGE, "url2"),
                TextNode(" end", TextType.TEXT),
            ],
            result,
        )

    def test_image_at_start(self):
        node = TextNode("![img](url) rest", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("img", TextType.IMAGE, "url"),
                TextNode(" rest", TextType.TEXT),
            ],
            result,
        )

    def test_image_at_end(self):
        node = TextNode("text ![img](url)", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("text ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "url"),
            ],
            result,
        )

    def test_only_image(self):
        node = TextNode("![img](url)", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("img", TextType.IMAGE, "url")],
            result,
        )

    def test_no_images(self):
        node = TextNode("Just plain text", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertListEqual([node], result)

    def test_non_text_node_passthrough(self):
        node = TextNode("bold", TextType.BOLD)
        result = split_nodes_image([node])
        self.assertListEqual([node], result)


class TestSplitNodesLink(unittest.TestCase):

    def test_single_link(self):
        node = TextNode(
            "Click [here](https://example.com)",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Click ", TextType.TEXT),
                TextNode("here", TextType.LINK, "https://example.com"),
            ],
            result,
        )

    def test_multiple_links(self):
        node = TextNode(
            "[one](url1) and [two](url2)",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("one", TextType.LINK, "url1"),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.LINK, "url2"),
            ],
            result,
        )

    def test_link_at_start(self):
        node = TextNode("[link](url) rest", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "url"),
                TextNode(" rest", TextType.TEXT),
            ],
            result,
        )

    def test_link_at_end(self):
        node = TextNode("text [link](url)", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("text ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
            ],
            result,
        )

    def test_only_link(self):
        node = TextNode("[link](url)", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("link", TextType.LINK, "url")],
            result,
        )

    def test_no_links(self):
        node = TextNode("No links here", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertListEqual([node], result)

    def test_image_not_treated_as_link(self):
        node = TextNode("![img](url)", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertListEqual([node], result)

    def test_non_text_node_passthrough(self):
        node = TextNode("italic", TextType.ITALIC)
        result = split_nodes_link([node])
        self.assertListEqual([node], result)


class TestCombinedBehavior(unittest.TestCase):

    def test_images_then_links_pipeline(self):
        node = TextNode(
            "![img](img_url) and [link](link_url)",
            TextType.TEXT,
        )

        step1 = split_nodes_image([node])
        step2 = split_nodes_link(step1)

        self.assertListEqual(
            [
                TextNode("img", TextType.IMAGE, "img_url"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "link_url"),
            ],
            step2,
        )


if __name__ == "__main__":
    unittest.main()