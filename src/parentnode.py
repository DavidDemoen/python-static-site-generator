from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Error: no tag in partennode.")
        if not self.children:
            raise ValueError("Error: no children in parentnode")
        childeren_rec_str = ""
        for child in self.children:
            childeren_rec_str += child.to_html()
        return f"<{self.tag}>{childeren_rec_str}</{self.tag}>"