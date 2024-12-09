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
            # Level=0 or level=1 remains unchanged
            if node.level == 0:
                # Original logic: horizontally arrange level=1 child nodes, no vertical offset
                if node.children:
                    total_width = w
                    for i, c in enumerate(node.children):
                        total_width += c.required_width + SPACING                      
                        c.is_direction = (i % 2 == 0)  # Even indexed child nodes are above, odd indexed are below
                    total_width -= SPACING  # Remove the last extra SPACING
                    node.required_width = total_width
                    node.required_height = h
                else:
                    node.required_width = w
                    node.required_height = h
            elif node.level == 1:
                # Original logic: there may be many level=1 child nodes, do not change here for now
                # Assuming they are still stacked vertically (if that was the case before)
                if node.children:
                    max_child_width = 0
                    total_child_height = 0
                    for c in node.children:
                        max_child_width = max(max_child_width, c.required_width)
                        total_child_height += c.required_height + DETAIL_SPACING
                        c.is_direction = node.is_direction  # Child nodes inherit parent's is_direction attribute
                    total_child_height -= DETAIL_SPACING
                    node.required_width = w + SUB_TOPIC_BOX_WIDTH
                    node.required_height = max(h, total_child_height)
                else:
                    node.required_width = w + SUB_TOPIC_BOX_WIDTH
                    node.required_height = h
        else:
            # Level=2 and above: use "horizontal + vertical offset" to layout child nodes
            if node.children:
                # Calculate total width (horizontally arranged)
                total_width = w
                for c in node.children:
                    total_width += c.required_width + SPACING
                    c.is_direction = node.is_direction  # Child nodes inherit parent's is_direction attribute
                total_width -= SPACING
                # Calculate maximum vertical offset
                count = len(node.children)
                half_count = (count + 1) // 2  # ceil(n/2)
                vertical_extent = half_count * (h + DETAIL_SPACING)
                required_height = max(h, 2 * vertical_extent)
                node.required_width = total_width
                node.required_height = required_height
            else:
                node.required_width = w
                node.required_height = h

        for c in node.children:
            c.parent = node
            self.measure_node(c)

    def measure(self, root):
        self.measure_node(root)
