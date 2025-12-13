import unittest

from parentnode import ParentNode
from leafnode import LeafNode

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
    
    def test_missing_tag_raises(self):
        child = LeafNode("span", "child")
        with self.assertRaises(ValueError):
            ParentNode(None, [child]).to_html()

    def test_none_children_raises(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()

    def test_empty_children_list_raises(self):
        with self.assertRaises(ValueError):
            ParentNode("div", []).to_html()

    def test_child_not_htmlnode_object(self):
        parent = ParentNode("div", ["not a node"])
        with self.assertRaises(AttributeError):
            parent.to_html()

    def test_child_to_html_raises(self):
        # Create a fake node whose to_html always raises
        class BadNode:
            def to_html(self):
                raise RuntimeError("bad child")

        parent = ParentNode("div", [BadNode()])
        with self.assertRaises(RuntimeError):
            parent.to_html()

    def test_multiple_children(self):
        c1 = LeafNode("span", "one")
        c2 = LeafNode("b", "two")
        parent = ParentNode("div", [c1, c2])
        self.assertEqual(
            parent.to_html(),
            "<div><span>one</span><b>two</b></div>",
        )

    def test_deep_nested_structure(self):
        deepest = LeafNode("i", "deep")
        middle = ParentNode("span", [deepest])
        outer = ParentNode("section", [middle])
        root = ParentNode("div", [outer])

        self.assertEqual(
            root.to_html(),
            "<div><section><span><i>deep</i></span></section></div>",
        )

    def test_props_are_ignored_in_output(self):
        # Only if HTMLNode.props exist but ParentNode.to_html does not use them
        c = LeafNode("span", "x")
        p = ParentNode("div", [c], props={"class": "test"})
        # since ParentNode doesn't render props, this should ignore them
        self.assertEqual(p.to_html(), "<div><span>x</span></div>")


if __name__ == "__main__":
    unittest.main()