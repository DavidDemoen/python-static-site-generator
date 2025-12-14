from .block_helpers import markdown_to_blocks, block_to_block_type, BlockType
from .htmlnode import HTMLNode
from .parentnode import ParentNode
from .text_helpers import text_to_textnodes
from .leafnode import LeafNode
from functools import partial
import textwrap

def markdown_to_html_node(md_text: str) -> HTMLNode:
    blocks = markdown_to_blocks(md_text)

    transformer_function_dict = {
        BlockType.PARAGRAPH: paragraph_transformer,
        BlockType.QUOTE: quote_transformer,
        BlockType.UNORDERED_LIST: partial(list_transformer, type="unordered", marker="-"),
        BlockType.ORDERED_LIST: partial(list_transformer, type="ordered", marker="."),
        BlockType.CODE: code_transformer,
        BlockType.HEADING: header_transformer
    }

    html_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        block_html_node = transformer_function_dict.get(block_type)(block=block)
        html_nodes.append(block_html_node)

    out_node = parent_node_wrapper("div", html_nodes)
    return out_node



def paragraph_transformer(block: str) -> HTMLNode:
    formatted_block = block.replace("\n", " ")
    html_nodes = text_to_html_node_transformer(formatted_block)
    return parent_node_wrapper("p", html_nodes)

def quote_transformer(block: str) -> HTMLNode:
    block_lines = block.split("\n")
    block_lines = list(map(lambda line: remove_md_marker(line, ">"),block_lines))
    formatted_block = " ".join(block_lines)
    html_nodes = text_to_html_node_transformer(formatted_block)
    return parent_node_wrapper("blockquote", html_nodes)

def list_transformer(block: str, type, marker) -> HTMLNode:
    tag_dict = {
        "unordered": "ul",
        "ordered": "ol"
    }

    block_lines = block.split("\n")
    block_lines = list(map(lambda line: remove_md_marker(line, marker),block_lines))
    html_nodes = []

    for line in block_lines:
        leaf_nodes = text_to_html_node_transformer(line)
        html_nodes.append(ParentNode("li", leaf_nodes))

    return ParentNode(tag_dict.get(type) , html_nodes)

def code_transformer(block: str) -> HTMLNode:
    block_lines = block.split("\n")

    # Remove starting and ending code fences
    if block_lines[0].strip().startswith("```"):
        block_lines = block_lines[1:]
    if block_lines and block_lines[-1].strip().startswith("```"):
        block_lines = block_lines[:-1]

    # Join lines and remove common leading indentation
    formatted_block = textwrap.dedent("\n".join(block_lines))

    # Wrap as a code block
    block_leaf_node = LeafNode(tag="", value=formatted_block)
    return ParentNode("pre", [parent_node_wrapper("code", [block_leaf_node])])

def header_transformer(block:str) -> HTMLNode:
    marker, sep, title = block.strip().partition(" ")
    level = len(marker)  # number of '#' characters
    html_nodes = text_to_html_node_transformer(title)
    return parent_node_wrapper(f"h{level}", html_nodes)

def text_to_html_node_transformer(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    return list(map(lambda node: node.to_html_node(), text_nodes))

def parent_node_wrapper(tag: str, children: list[HTMLNode]) -> ParentNode:
    return ParentNode(tag, children)

def block_text_formatter(block: str, ) -> str:
    return block.replace("\n", " ")

def remove_md_marker(text_line: str, marker: str) -> str:
    return text_line.split(f"{marker} ", maxsplit=1)[1]