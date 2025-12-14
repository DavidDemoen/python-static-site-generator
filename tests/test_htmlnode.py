import unittest

from src.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_default_initialization(self):
        # No arguments
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_initialization_with_all_args(self):
        # All arguments provided
        children = [HTMLNode("span", "child")]
        props = {"class": "my-class"}
        node = HTMLNode(tag="div", value="Hello", children=children, props=props)
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    def test_to_html_raises(self):
        node = HTMLNode("div")
        with self.assertRaises(NotImplementedError) as context:
            node.to_html()
        self.assertIn("Can't access function in the HTMLNode class", str(context.exception))

    def test_props_to_html_none(self):
        node = HTMLNode("div")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict(self):
        node = HTMLNode("div", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_property(self):
        node = HTMLNode("div", props={"id": "main"})
        self.assertEqual(node.props_to_html(), ' id="main"')

    def test_props_to_html_multiple_properties(self):
        props = {"id": "main", "class": "my-class"}
        node = HTMLNode("div", props=props)
        result = node.props_to_html()
        self.assertEqual(result, ' id="main" class="my-class"')

    def test_repr_no_props_no_children(self):
        node = HTMLNode("div", "value")
        expected = "Tag: div, Value:value, Children: None, Props: None"
        self.assertEqual(repr(node), expected)

    def test_repr_with_children_and_props(self):
        children = [HTMLNode("span", "child")]
        props = {"class": "my-class"}
        node = HTMLNode("div", "parent", children=children, props=props)
        expected = f"Tag: div, Value:parent, Children: {children}, Props: {props}"
        self.assertEqual(repr(node), expected)

    def test_children_as_empty_list(self):
        node = HTMLNode("div", children=[])
        self.assertEqual(node.children, [])

    def test_props_with_special_characters(self):
        props = {"data-value": "some:value", "style": "color:red;"}
        node = HTMLNode("div", props=props)
        result = node.props_to_html()
        self.assertEqual(result, ' data-value="some:value" style="color:red;"')

    def test_value_as_none_or_empty_string(self):
        node1 = HTMLNode("div", value=None)
        node2 = HTMLNode("div", value="")
        self.assertIsNone(node1.value)
        self.assertEqual(node2.value, "")

    def test_tag_as_none_or_empty_string(self):
        node1 = HTMLNode(tag=None)
        node2 = HTMLNode(tag="")
        self.assertIsNone(node1.tag)
        self.assertEqual(node2.tag, "")

if __name__ == "__main__":
    unittest.main()