from timeline.basics import *
from core.geometry import *
from timeline.classic_shapes import *
from timeline.optimize import *

class ApplyLayout:
    def __init__(self):
        self.placed_nodes = {}  # Already placed nodes and their status

    def resolve_overlaps(self):
        """Check and resolve all box overlaps"""
        resolve_cross_level1_overlaps(self.placed_nodes,DETAIL_SPACING, 0, "horizontal")
        resolve_within_level1_overlaps(self.placed_nodes, 0, DETAIL_BOX_HEIGHT + DETAIL_SPACING, "horizontal")

    def layout_node(self, node, x, y):
        """Recursively layout according to node level"""
        if node.level == 0:
            w, h = MAIN_TOPIC_BOX_WIDTH, MAIN_TOPIC_BOX_HEIGHT
        elif node.level == 1:
            w, h = SUB_TOPIC_BOX_WIDTH, SUB_TOPIC_BOX_HEIGHT
        else:
            w, h = DETAIL_BOX_WIDTH, DETAIL_BOX_HEIGHT

        node.shape = Box(x, y, w, h)
        # Add this node to the placed list and initialize as unshifted
        self.placed_nodes[node.id] = {"node": node}

        if node.level == 0 and node.children:
            center_y = node.shape.center[1]
            current_x = node.shape.right + SPACING
            for i, c in enumerate(node.children):
                child_y = center_y - SUB_TOPIC_BOX_HEIGHT / 2
                self.layout_node(c, current_x, child_y)
                current_x += c.required_width

        elif node.level == 1 and node.children:
            top_center_x = node.shape.center[0] + DETAIL_SPACING
            top_center_y = node.shape.top
            top_center_bottom = node.shape.bottom
            for i, c in enumerate(node.children):
                node_left = top_center_x
                if c.is_above:
                    node_top = top_center_y - DETAIL_SPACING - i * (DETAIL_BOX_HEIGHT + DETAIL_SPACING) - DETAIL_BOX_HEIGHT
                else:
                    node_top = top_center_bottom + DETAIL_SPACING + i * (DETAIL_BOX_HEIGHT + DETAIL_SPACING)
                self.layout_node(c, node_left, node_top)

        elif node.level >= 2:
            node_left_base = node.shape.right + DETAIL_SPACING
            if len(node.children) > 1:
                node_left_base = node.shape.right + 2 * DETAIL_SPACING
            
            for i, c in enumerate(node.children):
                node_left = node_left_base
                if c.is_above:
                    node_top = node.shape.top - i * (DETAIL_BOX_HEIGHT + DETAIL_SPACING)
                else:
                    node_top = node.shape.top + i * (DETAIL_BOX_HEIGHT + DETAIL_SPACING)
                self.layout_node(c, node_left, node_top)

    def apply(self, root):
        """Main layout entry point"""
        rw, rh = MAIN_TOPIC_BOX_WIDTH, MAIN_TOPIC_BOX_HEIGHT
        root_x = LEFT_MARGIN
        root_y = (SLIDE_HEIGHT / 2) - (rh / 2)
        self.layout_node(root, root_x, root_y)
        # Check and resolve all overlaps after layout is complete
        self.resolve_overlaps()  

if __name__ == "__main__":
    pass
