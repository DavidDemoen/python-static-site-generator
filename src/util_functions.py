from src.textnode import TextType, TextNode
from src.leafnode import LeafNode
import re

def text_node_to_html_node(text_node):
    mapping = {
        TextType.TEXT:  lambda tn: LeafNode(None, tn.text),
        TextType.BOLD:  lambda tn: LeafNode("b", tn.text),
        TextType.ITALIC: lambda tn: LeafNode("i", tn.text),
        TextType.CODE:  lambda tn: LeafNode("code", tn.text),
        TextType.LINK:  lambda tn: LeafNode("a", tn.text, {"href": tn.url}),
        TextType.IMAGE: lambda tn: LeafNode("img", "", {"src": tn.url, "alt": tn.text}),
    }

    try:
        return mapping[text_node.text_type](text_node)
    except KeyError:
        raise Exception(f"Invalid TextType: {text_node.text_type}")
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise ValueError("Invalid Markdown syntax: no closing delimiter found")
        for index, text_part in enumerate(split_text):
            if text_part == "":
                continue
            type =  text_type if index % 2 != 0 else TextType.TEXT
            new_nodes.append(TextNode(text_part, type))
    
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        node_text = node.text
        images = extract_markdown_images(node_text)

        if len(images) == 0:
            new_nodes.append(node)
            continue

        for alt, url in images:
            markdown = f"![{alt}]({url})"
            sections = node_text.split(markdown, 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            node_text = sections[1]
        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        links = extract_markdown_links(text)

        if len(links) == 0:
            new_nodes.append(node)
            continue

        for anchor, url in links:
            markdown = f"[{anchor}]({url})"
            before, after = text.split(markdown, 1)

            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(anchor, TextType.LINK, url))
            text = after

        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes