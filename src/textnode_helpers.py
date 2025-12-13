from textnode import TextType, TextNode
from markdown_helpers import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    out_lst = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            out_lst.append(old_node)
            continue
        temp_lst =[]
        split_node = old_node.text.split(delimiter)
        if len(split_node) % 2 == 0:
            raise Exception("Error: No closing delimiter found")
        for index in range(len(split_node)):
            temp_lst.append(TextNode(split_node[index], TextType.TEXT if index % 2 == 0  else text_type))
        out_lst.extend(temp_lst)
    return out_lst

def split_nodes_image(old_nodes):
    return generic_node_splitter(old_nodes, TextType.IMAGE)

def split_nodes_link(old_nodes):
    return generic_node_splitter(old_nodes, TextType.LINK)


def generic_node_splitter(nodes, type):
    if (type != TextType.IMAGE) and (type != TextType.LINK):
        raise TypeError("Wrong textype for node splitter")
    
    out_lst = []
    
    extracter_lu_dict = {
        TextType.IMAGE: extract_markdown_images,
        TextType.LINK: extract_markdown_links
    }
    for node in nodes:
        md_components = extracter_lu_dict.get(type)(node.text)
        if not md_components:
            out_lst.append(node)
            continue
        working_string = node.text
        for idx in range(0, len(md_components)):
            sections = working_string.split(f'{"!" if type == TextType.IMAGE else ""}[{md_components[idx][0]}]({md_components[idx][1]})', 1)
            if sections[0]:
                out_lst.append(TextNode(sections[0], TextType.TEXT))
            out_lst.append(TextNode(md_components[idx][0], type, md_components[idx][1]))
            working_string = sections[1]
            if idx == len(md_components) - 1 and sections[1]:
                out_lst.append(TextNode(sections[1], TextType.TEXT))
        
    return out_lst

def text_to_textnodes(text):
    return split_nodes_image(split_nodes_link(split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD), "_", TextType.ITALIC), "`", TextType.CODE)))