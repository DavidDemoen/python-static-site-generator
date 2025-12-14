import unittest

from src.textnode import TextNode, TextType
from src.leafnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_textnode_init(self):
        text_node = TextNode("Test", TextType.LINK, "http://www.test.io")
        self.assertEqual(text_node.text, "Test")
        self.assertEqual(text_node.text_type, TextType.LINK)
        self.assertEqual(text_node.url, "http://www.test.io")
    
    def test_textnode_eq_basic(self):
        # Basic equality
        tn1 = TextNode("Hello", TextType.TEXT)
        tn2 = TextNode("Hello", TextType.TEXT)
        self.assertEqual(tn1, tn2)

    def test_textnode_eq_with_url(self):
        # Equality with URL
        tn1 = TextNode("Link", TextType.LINK, "http://example.com")
        tn2 = TextNode("Link", TextType.LINK, "http://example.com")
        self.assertEqual(tn1, tn2)

    def test_textnode_neq_text(self):
        # Different text
        tn1 = TextNode("Hello", TextType.TEXT)
        tn2 = TextNode("World", TextType.TEXT)
        self.assertNotEqual(tn1, tn2)

    def test_textnode_neq_type(self):
        # Different TextType
        tn1 = TextNode("Hello", TextType.TEXT)
        tn2 = TextNode("Hello", TextType.BOLD)
        self.assertNotEqual(tn1, tn2)

    def test_textnode_neq_url(self):
        # Different URL
        tn1 = TextNode("Link", TextType.LINK, "http://a.com")
        tn2 = TextNode("Link", TextType.LINK, "http://b.com")
        self.assertNotEqual(tn1, tn2)

    def test_textnode_eq_none_url(self):
        # URL None vs None
        tn1 = TextNode("Text", TextType.TEXT)
        tn2 = TextNode("Text", TextType.TEXT, None)
        self.assertEqual(tn1, tn2)

    def test_textnode_neq_none_vs_url(self):
        # URL None vs non-None
        tn1 = TextNode("Link", TextType.LINK)
        tn2 = TextNode("Link", TextType.LINK, "http://example.com")
        self.assertNotEqual(tn1, tn2)

    def test_textnode_eq_different_objects(self):
        # Compare with non-TextNode object
        tn = TextNode("Hello", TextType.TEXT)
        self.assertFalse(tn == "not a TextNode")

    def test_textnode_repr(self):
        # __repr__ returns correct string
        tn = TextNode("Hello", TextType.TEXT, "http://example.com")
        expected = "TextNode(Hello, TextType.TEXT, http://example.com)"
        self.assertEqual(repr(tn), expected)

    def test_all_texttypes(self):
        # Test all TextType values
        for ttype in TextType:
            tn = TextNode("Sample", ttype)
            self.assertEqual(tn.text_type, ttype)
            self.assertEqual(tn.text, "Sample")
            self.assertIsNone(tn.url)

class TestToHtmlNode(unittest.TestCase):
    # ---------- VALID TEXT TYPES ----------

    def test_text_type_text(self):
        node = TextNode("Hello", TextType.TEXT)
        html_node = node.to_html_node()

        self.assertIsInstance(html_node, LeafNode)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "Hello")
        self.assertIsNone(html_node.props)

    def test_text_type_bold(self):
        node = TextNode("Bold", TextType.BOLD)
        html_node = node.to_html_node()

        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold")
        self.assertIsNone(html_node.props)

    def test_text_type_italic(self):
        node = TextNode("Italic", TextType.ITALIC)
        html_node = node.to_html_node()

        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic")
        self.assertIsNone(html_node.props)

    def test_text_type_code(self):
        node = TextNode("print(x)", TextType.CODE)
        html_node = node.to_html_node()

        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print(x)")
        self.assertIsNone(html_node.props)

    def test_text_type_link(self):
        node = TextNode("My link", TextType.LINK, "http://example.com")
        html_node = node.to_html_node()

        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "text")  # literal per implementation
        self.assertEqual(html_node.props, {"href": "http://example.com"})

    def test_text_type_image(self):
        node = TextNode("Alt text", TextType.IMAGE, "image.png")
        html_node = node.to_html_node()

        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "image.png", "alt": "Alt text"}
        )

    # ---------- EDGE CASES ----------

    def test_invalid_text_type_raises(self):
        node = TextNode("Oops", "NOT_A_TYPE")

        with self.assertRaises(Exception) as context:
            node.to_html_node()

        self.assertIn("invalid TextType", str(context.exception))

    def test_missing_url_for_link(self):
        node = TextNode("Link", TextType.LINK, None)
        html_node = node.to_html_node()

        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href": None})

    def test_missing_url_for_image(self):
        node = TextNode("Alt", TextType.IMAGE, None)
        html_node = node.to_html_node()

        self.assertEqual(html_node.tag, "img")
        self.assertEqual(
            html_node.props,
            {"src": None, "alt": "Alt"}
        )

    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        html_node = node.to_html_node()

        self.assertEqual(html_node.value, "")

    def test_none_text(self):
        node = TextNode(None, TextType.TEXT)
        html_node = node.to_html_node()

        self.assertIsNone(html_node.value)


if __name__ == "__main__":
    unittest.main()