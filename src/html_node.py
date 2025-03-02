class HTMLNode:
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: list = None,
        props: dict = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        props = ""

        if self.props:
            for k, v in self.props.items():
                props += f' {k}="{v}"'

        return props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, value: str, tag: str = None, props: dict = None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")

        return (
            f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
            if self.tag != None
            else f"{self.value}"
        )

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict = None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.children is None:
            raise ValueError("invalid HTML: no children")

        html = f"<{self.tag}{self.props_to_html()}>"
        for node in self.children:
            if node.tag == self.tag:
                if node.value:
                    html += node.value
                else:
                    html += node.to_html()
            else:
                html += node.to_html()

        html += f"</{self.tag}>"

        return html

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
