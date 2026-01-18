import unittest
from src.parentnode import ParentNode
from src.leafnode import LeafNode
from src.textnode import TextNode, TextType


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], props={"class": "myClass", "id": "myId"})
        self.assertEqual(parent_node.to_html(), "<div class=\"myClass\" id=\"myId\"><span>child</span></div>")

    def test_to_html_with_raw_string_child(self):
        parent_node = ParentNode("p", ["raw string"])
        self.assertEqual(parent_node.to_html(), "<p>raw string</p>")

    def test_to_html_with_mixed_children(self):
        child1 = LeafNode("span", "s")
        child2 = "plain text"
        child3 = ParentNode("em", [LeafNode("i", "italic")])
        parent_node = ParentNode("div", [child1, child2, child3])
        self.assertEqual(parent_node.to_html(), "<div><span>s</span>plain text<em><i>italic</i></em></div>")

    def test_leafnode_without_tag_returns_value_inside_parent(self):
        child = LeafNode(None, "plain")
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(), "<div>plain</div>")

    def test_props_with_nonstring_value_are_stringified(self):
        child = LeafNode("span", "x")
        parent = ParentNode("div", [child], props={"data-num": 123})
        self.assertEqual(parent.to_html(), "<div data-num=\"123\"><span>x</span></div>")

    def test_non_htmlnode_children_are_stringified(self):
        tn = TextNode("hello", TextType.BOLD)
        parent = ParentNode("div", [tn])
        # TextNode.__repr__ is used when stringified
        self.assertEqual(parent.to_html(), f"<div>{repr(tn)}</div>")

    def test_raises_on_no_tag(self):
        child = LeafNode("span", "x")
        parent = ParentNode("", [child])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_raises_on_no_children_empty_list(self):
        parent = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_raises_on_no_children_none(self):
        parent = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent.to_html()


if __name__ == "__main__":
    unittest.main()
