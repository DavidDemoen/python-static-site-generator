class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Error: Can't access function in the HTMLNode class")
    
    def props_to_html(self):
        if not self.props:
            return ""
        out_str = ""
        for key, value in self.props.items():
            out_str += f' {key}="{value}"'
        
        return out_str
    
    def __repr__(self):
        return f"Tag: {self.tag}, Value:{self.value}, Children: {self.children}, Props: {self.props}"
    