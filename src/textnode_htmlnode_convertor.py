from textnode import TextType
from leafnode import LeafNode

def text_node_to_html_node(text_node):
    type_mapping = {
        TextType.TEXT: lambda node: LeafNode(None, node.text),
        TextType.BOLD: lambda node: LeafNode("b", node.text),
        TextType.ITALIC: lambda node: LeafNode("i", node.text),
        TextType.CODE: lambda node: LeafNode("code", node.text),
        TextType.LINK: lambda node: LeafNode("a", node.text, {"href": node.url}),
        TextType.IMAGE: lambda node: LeafNode("img", "", {"src": node.url, "alt": node.text})
    }
    if text_node.text_type not in type_mapping:
        raise ValueError(f"Unknown TextType: {text_node.text_type}")
    
    return type_mapping.get(text_node.text_type)(text_node)