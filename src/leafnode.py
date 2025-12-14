from .htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Error: A Leaf Node must have a value")
        if not self.tag:
            return f"{self.value}"

        return f'<{self.tag}{self.props_to_html()}>"{self.value}"</{self.tag}>'