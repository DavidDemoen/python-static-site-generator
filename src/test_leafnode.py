import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_tag_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.tag, "p")
    
    def test_leaf_value_hello(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.value, "Hello, world!")