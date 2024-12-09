from timeline.basics import *
from core.geometry import *

class MeasureLayout:
    def measure_node(self, node):
        # Determine basic size
        if node.level == 0:
            w, h = MAIN_TOPIC_BOX_WIDTH, MAIN_TOPIC_BOX_HEIGHT
        elif node.level == 1:
            w, h = SUB_TOPIC_BOX_WIDTH, SUB_TOPIC_BOX_HEIGHT
        else:
            w, h = DETAIL_BOX_WIDTH, DETAIL_BOX_HEIGHT

        if node.level < 2:
            # Level=0 or level=1 vertically stack child nodes
            if node.level == 0:
                # Vertically arrange level=1 child nodes
                if node.children:
                    max_child_width = w
                    total_height = h
                    for i, c in enumerate(node.children):
                        max_child_width = max(max_child_width, c.required_width)
                        total_height += c.required_height + SPACING
                        c.is_direction = (i % 2 == 0)
                    total_height -= SPACING  # Remove the last extra SPACING
                    node.required_width = max_child_width
                    node.required_height = total_height
                else:
                    node.required_width = w
                    node.required_height = h
            elif node.level == 1:
                # Vertically stack level=2 child nodes
                if node.children:
                    max_child_width = 0
                    total_child_height = 0
                    for c in node.children:
                        max_child_width = max(max_child_width, c.required_width)
                        total_child_height += c.required_height + DETAIL_SPACING
                        c.is_direction = node.is_direction
                    total_child_height -= DETAIL_SPACING
                    node.required_width = max(w, max_child_width)
                    node.required_height = h + total_child_height
                else:
                    node.required_width = w
                    node.required_height = h
        else:
            # Level=2 and above: vertically stack child nodes
            if node.children:
                max_child_width = w
                total_height = h
                for c in node.children:
                    max_child_width = max(max_child_width, c.required_width)
                    total_height += c.required_height + DETAIL_SPACING
                    c.is_direction = node.is_direction
                total_height -= DETAIL_SPACING
                node.required_width = max_child_width
                node.required_height = total_height
            else:
                node.required_width = w
                node.required_height = h

        for c in node.children:
            c.parent = node
            self.measure_node(c)

    def measure(self, root):
        self.measure_node(root)
