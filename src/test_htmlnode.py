import unittest

from htmlnode import HTMLNode

props_01 = {
    "href": "https://www.google.com",
    "target": "_blank",
}
props_01_html_str = ' href="https://www.google.com" target="_blank"'


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a", "value string", None, props_01)
        html_str = node.props_to_html()
        self.assertEqual(html_str, props_01_html_str)

    def test_repr_self(self):
        node_01 = HTMLNode("a", "value string", None, props_01)
        node_str = str(node_01)
        self.assertEqual(node_str, "HTMLNode(a, value string, children: None, {'href': 'https://www.google.com', 'target': '_blank'})")

        node = HTMLNode(
            "p",
            "What a strange world",
            node_01,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            f"HTMLNode(p, What a strange world, children: {node_01}, {{'class': 'primary'}})"
        )
    
    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

        

if __name__ == "__main__":
    unittest.main()
