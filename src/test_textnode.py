import unittest

from textnode import TextType, TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD, 'http://www.boot.dev')
        node2 = TextNode("This is a text node", TextType.BOLD, 'http://www.boot.dev')
        self.assertEqual(node, node2)


    def test_text_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_type_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.CODE)
        self.assertNotEqual(node, node2)
    
    def test_none_url_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
if __name__ == "__main__":
    unittest.main()