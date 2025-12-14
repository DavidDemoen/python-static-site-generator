import re
from .textnode import TextNode, TextType

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)
    
def text_to_textnodes(text):
   from .textnode_helpers import split_nodes_delimiter, split_nodes_link, split_nodes_image

   return  split_nodes_link(split_nodes_image(split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter([TextNode(text, TextType.TEXT)], '**', TextType.BOLD), '*', TextType.ITALIC), '`', TextType.CODE)))