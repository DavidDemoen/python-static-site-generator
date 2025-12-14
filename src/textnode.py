from enum import Enum
from .leafnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, value):
        if not isinstance(value, TextNode):
            return False
        if self.text != value.text or self.text_type != value.text_type or self.url != value.url:
            return False
        return True
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
    def to_html_node(self):
        text_type_leaf_lu_dict = {
            TextType.TEXT: lambda: LeafNode(tag=None, value=self.text),
            TextType.BOLD: lambda: LeafNode(tag="b", value=self.text),
            TextType.ITALIC: lambda: LeafNode(tag="i", value=self.text),
            TextType.CODE: lambda: LeafNode(tag="code", value=self.text),
            TextType.LINK: lambda: LeafNode(tag="a", value="text", props={"href": self.url}),
            TextType.IMAGE: lambda: LeafNode(tag="img", value="", props={"src": self.url, "alt": self.text})
        }
        if self.text_type not in text_type_leaf_lu_dict:
            raise Exception("Error: TextNode has an invalid TextType")
        return text_type_leaf_lu_dict.get(self.text_type)()
