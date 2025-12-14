import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(md_text):
    pattern = r'(?:\r?\n){2,}'
    return [block.strip() for block in re.split(pattern, md_text) if block.strip()]

def block_to_block_type(block: str) -> BlockType:
    block_lines = block.splitlines()
    
    if not block_lines:
        return BlockType.PARAGRAPH
    if re.match(r'#{1,6} ', block_lines[0]):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in block_lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in block_lines):
        return BlockType.UNORDERED_LIST
    if ordered_match(block_lines):
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH
    

def ordered_match(block_lines: list[str]) -> bool:
    for i, line in enumerate(block_lines, start=1):
        if not line.startswith(f"{i}. "):
            return False
    return True