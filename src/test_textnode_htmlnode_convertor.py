import unittest

from textnode import TextType, TextNode
from textnode_htmlnode_convertor import text_node_to_html_node

class TestTextHtmlConvertor(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("alt text", TextType.IMAGE, "http://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "http://www.boot.dev", "alt": "alt text"})

    def test_image_to_html(self):
        node = TextNode("alt text", TextType.IMAGE, "http://www.boot.dev")
        html_node = text_node_to_html_node(node)
        to_html = html_node.to_html()
        self.assertEqual(to_html, '<img src="http://www.boot.dev" alt="alt text"></img>')
    
    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), '<b>This is a text node</b>')

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), '<i>This is a text node</i>')
    
    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), '<code>This is a text node</code>')

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "http://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "http://www.boot.dev"})
        self.assertEqual(html_node.to_html(), '<a href="http://www.boot.dev">This is a link node</a>')
    
if __name__ == "__main__":
    unittest.main()