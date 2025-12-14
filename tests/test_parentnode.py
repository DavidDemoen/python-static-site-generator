import unittest

from src.parentnode import ParentNode
from src.leafnode import LeafNode
from src.htmlnode import HTMLNode


class TestParentNode(unittest.TestCase):

    # ---------- BASIC FUNCTIONALITY ----------

    def test_parent_to_html_simple(self):
        node = ParentNode("div", [LeafNode("span", "Hello")])
        self.assertEqual(
            node.to_html(),
            '<div><span>Hello</span></div>'
        )

    def test_parent_to_html_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold"),
                LeafNode(None, " text "),
                LeafNode("i", "Italic"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            '<p><b>Bold</b> text <i>Italic</i></p>'
        )

    def test_nested_parent_nodes(self):
        p1 = ParentNode("p", [LeafNode(None, "Paragraph 1")])
        p2 = ParentNode("p", [LeafNode(None, "Paragraph 2")])
        div = ParentNode("div", [p1, p2])

        self.assertEqual(
            div.to_html(),
            '<div><p>Paragraph 1</p><p>Paragraph 2</p></div>'
        )

    # ---------- GIVEN EXAMPLE ----------

    def test_given_div_example(self):
        p_node_1 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        p_node_2 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        div_node = ParentNode("div", [p_node_1, p_node_2])

        self.assertEqual(
            div_node.to_html(),
            '<div>'
            '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
            '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
            '</div>'
        )

    # ---------- EDGE CASES ----------

    def test_parent_no_tag_raises(self):
        node = ParentNode(None, [LeafNode("span", "Text")])
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertIn("must have a tag", str(context.exception))

    def test_parent_empty_tag_raises(self):
        node = ParentNode("", [LeafNode("span", "Text")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_no_children_raises(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertIn("must have children", str(context.exception))

    def test_parent_empty_children_list_raises(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_child_without_to_html(self):
        class BadNode:
            pass

        node = ParentNode("div", [BadNode()])
        with self.assertRaises(AttributeError):
            node.to_html()

    # ---------- MIXED CHILD TYPES ----------

    def test_parent_with_only_text_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode(None, "Hello"),
                LeafNode(None, " "),
                LeafNode(None, "World"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p>Hello World</p>"
        )

    def test_parent_with_htmlnode_child(self):
        # HTMLNode.to_html raises NotImplementedError
        node = ParentNode("div", [HTMLNode("span", "test")])
        with self.assertRaises(NotImplementedError):
            node.to_html()

    # ---------- PROPS HANDLING ----------

    def test_parent_props_ignored_in_html(self):
        node = ParentNode(
            "div",
            [LeafNode("span", "Hi")],
            props={"class": "container"},
        )
        # ParentNode does not render props
        self.assertEqual(
            node.to_html(),
            '<div><span>Hi</span></div>'
        )

    # ---------- DEEP NESTING ----------

    def test_deeply_nested_structure(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "section",
                    [
                        ParentNode(
                            "p",
                            [LeafNode("b", "Deep")]
                        )
                    ],
                )
            ],
        )

        self.assertEqual(
            node.to_html(),
            '<div><section><p><b>Deep</b></p></section></div>'
        )


if __name__ == "__main__":
    unittest.main()
