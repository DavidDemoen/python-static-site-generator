import unittest

from src.leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leafnode_basic_tag_and_value(self):
        node = LeafNode("span", "Hello")
        expected_html = '<span>"Hello"</span>'
        self.assertEqual(node.to_html(), expected_html)

    def test_leafnode_value_none_raises(self):
        node = LeafNode("span", None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertIn("A Leaf Node must have a value", str(context.exception))

    def test_leafnode_tag_none_returns_value_only(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leafnode_with_props_no_href(self):
        node = LeafNode("div", "Content", props={"class": "my-class", "id": "main"})
        expected_html = '<div class="my-class" id="main">"Content"</div>'
        self.assertEqual(node.to_html(), expected_html)

    def test_leafnode_with_href_prop(self):
        node = LeafNode("a", "Click me", props={"href": "http://example.com"})
        expected_html = '<a href="http://example.com">"Click me"</a>'
        self.assertEqual(node.to_html(), expected_html)

    def test_leafnode_value_empty_string(self):
        node = LeafNode("span", "")
        self.assertEqual(node.to_html(), '<span>""</span>')

    def test_leafnode_tag_empty_string(self):
        node = LeafNode("", "Text")
        self.assertEqual(node.to_html(), "Text")

    def test_leafnode_props_with_special_characters(self):
        node = LeafNode("button", "Click", props={"data-action": "save:1"})
        expected_html = '<button data-action="save:1">"Click"</button>'
        self.assertEqual(node.to_html(), expected_html)

    def test_leafnode_repr(self):
        node = LeafNode("span", "Text", props={"class": "cls"})
        expected_repr = f'Tag: span, Value:Text, Children: None, Props: {{\'class\': \'cls\'}}'
        self.assertEqual(repr(node), expected_repr)

if __name__ == "__main__":
    unittest.main()