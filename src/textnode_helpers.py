
from .textnode import TextType, TextNode
from .text_helpers import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    text_nodes_out_lst = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            text_nodes_out_lst.append(node)
            continue

        sections = node.text.split(delimiter)

        if len(sections) <= 1:
            text_nodes_out_lst.append(node)
            continue
        
        if len(sections) % 2 == 0:
            raise Exception(f"Error: No closing caption for delimiter {delimiter} in: {node.text}")
        
        for idx in range(len(sections)):
            text_nodes_out_lst.append(TextNode(sections[idx], TextType.TEXT if idx % 2 == 0 else text_type))
    
    return text_nodes_out_lst

def split_nodes_link(nodes):
    return generic_node_splitter(nodes, TextType.LINK)

def split_nodes_image(nodes):
    return generic_node_splitter(nodes, TextType.IMAGE)

def generic_node_splitter(nodes, text_type):
    out_lst = []

    extractor_dict = {
        TextType.LINK: extract_markdown_links,
        TextType.IMAGE: extract_markdown_images,
    }

    for node in nodes:
        extracted_items = extractor_dict[text_type](node.text)
        if not extracted_items:
            out_lst.append(node)
            continue
        working_string = node.text
        for extracted_item in extracted_items:
            sections = working_string.split(f'{"!" if text_type == TextType.IMAGE else ""}[{extracted_item[0]}]({extracted_item[1]})', 1)
            if sections[0] != "":
                out_lst.append(TextNode(sections[0], TextType.TEXT))
            out_lst.append(TextNode(extracted_item[0], text_type, extracted_item[1]))
            working_string = sections[1]
        if working_string != "":
            out_lst.append(TextNode(working_string, TextType.TEXT))
    
    return out_lst