import unittest
from src.htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_init_defaults(self):
            node = HTMLNode()
            self.assertIsNone(node.tag)
            self.assertIsNone(node.value)
            self.assertIsNone(node.children)
            self.assertIsNone(node.props)

    def test_init_with_values(self):
        props = {"class": "btn"}
        children = ["child"]
        node = HTMLNode("p", "Hello", children, props)

        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    def test_props_to_html_none(self):
        node = HTMLNode("p", "Hello")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict(self):
        node = HTMLNode("p", "Hello", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        node = HTMLNode("a", "Link", props={"href": "https://example.com"})
        self.assertEqual(
            node.props_to_html(),
            ' href="https://example.com"'
        )

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(
            "a",
            "Link",
            props={"href": "https://example.com", "class": "nav"}
        )
        result = node.props_to_html()

        # Order-independent assertions
        self.assertIn(' href="https://example.com"', result)
        self.assertIn(' class="nav"', result)

    def test_repr(self):
        node = HTMLNode("p", "Hello", None, {"class": "text"})
        self.assertEqual(
            repr(node),
            "p, Hello, None, {'class': 'text'}"
        )

    def test_to_html_not_implemented(self):
        node = HTMLNode("p", "Hello")
        with self.assertRaises(NotImplementedError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()