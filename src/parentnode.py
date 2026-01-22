from src.htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("invalid HTML: no tag")
        if not self.children:
            raise ValueError("invalid HTML: no children")
        
        children_html = ''.join(
            child.to_html() if isinstance(child, HTMLNode) else str(child)
            for child in self.children
        )
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"