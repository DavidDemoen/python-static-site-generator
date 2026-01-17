import unittest
from src.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq_same_values(self):
        node1 = TextNode("Hello", TextType.BOLD)
        node2 = TextNode("Hello", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_not_eq_different_text(self):
        node1 = TextNode("Hello", TextType.BOLD)
        node2 = TextNode("World", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_not_eq_different_type(self):
        node1 = TextNode("Hello", TextType.BOLD)
        node2 = TextNode("Hello", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_not_eq_different_url(self):
        node1 = TextNode("Hello", TextType.LINK, "https://a.com")
        node2 = TextNode("Hello", TextType.LINK, "https://b.com")
        self.assertNotEqual(node1, node2)

    def test_eq_with_same_url(self):
        node1 = TextNode("Hello", TextType.LINK, "https://a.com")
        node2 = TextNode("Hello", TextType.LINK, "https://a.com")
        self.assertEqual(node1, node2)

    def test_none_url_vs_url(self):
        node1 = TextNode("Hello", TextType.LINK)
        node2 = TextNode("Hello", TextType.LINK, "https://a.com")
        self.assertNotEqual(node1, node2)

    def test_repr_without_url(self):
        node = TextNode("Hello", TextType.BOLD)
        self.assertEqual(
            repr(node),
            "TextNode(Hello, bold, None)"
        )

    def test_repr_with_url(self):
        node = TextNode("Hello", TextType.LINK, "https://a.com")
        self.assertEqual(
            repr(node),
            "TextNode(Hello, link, https://a.com)"
        )

    def test_not_equal_other_type(self):
        node = TextNode("Hello", TextType.BOLD)
        self.assertNotEqual(node, "not a text node")


if __name__ == "__main__":
    unittest.main()