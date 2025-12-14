import re

def markdown_to_blocks(md_text):
    pattern = r'(?:\r?\n){2,}'
    return [block.strip() for block in re.split(pattern, md_text) if block.strip()]