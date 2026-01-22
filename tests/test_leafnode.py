import unittest
from src.leafnode import LeafNode

class TestLeafnode(unittest.TestCase):
    def test_text_only_node(self):
        node = LeafNode(None, "Hello world")
        self.assertEqual(node.to_html(), "Hello world")

    def test_simple_html_node(self):
        node = LeafNode("p", "Hello")
        self.assertEqual(node.to_html(), "<p>Hello</p>")

    def test_html_node_with_props(self):
        node = LeafNode(
            "a",
            "Click me",
            {"href": "https://example.com"}
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://example.com">Click me</a>'
        )

    def test_html_node_with_multiple_props(self):
        node = LeafNode(
            "a",
            "Click",
            {"href": "https://example.com", "class": "btn"}
        )
        html = node.to_html()
        self.assertIn('<a', html)
        self.assertIn('href="https://example.com"', html)
        self.assertIn('class="btn"', html)
        self.assertTrue(html.endswith(">Click</a>"))

    def test_missing_value_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_empty_string_value_raises(self):
        node = LeafNode("p", "")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_repr(self):
        node = LeafNode("p", "Hello", {"class": "text"})
        self.assertEqual(
            repr(node),
            "LeafNode: p, Hello, {'class': 'text'}"
        )

    def test_children_is_none(self):
        node = LeafNode("p", "Hello")
        self.assertIsNone(node.children)

    def test_props_none(self):
        node = LeafNode("p", "Hello")
        self.assertEqual(node.props_to_html(), "")


if __name__ == "__main__":
    unittest.main()    