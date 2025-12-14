from .htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("Error: A parent node must have a tag")
        if not self.children:
            raise ValueError("Error: A parent node must have children")
        
        children_str = ""
        for child in self.children:
            children_str += child.to_html()
            
        return f"<{self.tag}>{children_str}</{self.tag}>"