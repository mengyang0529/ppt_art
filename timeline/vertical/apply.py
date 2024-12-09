from timeline.basics import *
from core.geometry import *
from timeline.optimize import resolve_cross_level1_overlaps, resolve_within_level1_overlaps

class ApplyLayout:
    def __init__(self):
        self.placed_nodes = {}  # Already placed nodes and their status

    def resolve_overlaps(self):
        """Check and resolve all box overlaps"""
        # Implementation specific to vertical layout, if required
        resolve_cross_level1_overlaps(self.placed_nodes, 0, DETAIL_SPACING, "vertical")
        resolve_within_level1_overlaps(self.placed_nodes, DETAIL_BOX_WIDTH + DETAIL_SPACING, 0, "vertical")

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
            current_y = node.shape.bottom + SPACING
            for c in node.children:
                child_x = x + (node.shape.width - c.required_width) / 2
                self.layout_node(c, child_x, current_y)
                current_y += c.required_height + SPACING

        elif node.level == 1 and node.children:
            node_top = node.shape.center[1] + DETAIL_SPACING
            if node.is_direction:
                node_left = node.shape.left - DETAIL_BOX_WIDTH
            else:
                node_left = node.shape.right

            for c in node.children:
                if c.is_direction:
                    node_left -= DETAIL_SPACING + DETAIL_BOX_WIDTH
                else:
                    node_left += DETAIL_SPACING + DETAIL_BOX_WIDTH
                
                self.layout_node(c, node_left, node_top)            

        elif node.level >= 2:
            node_top_base = node.shape.bottom + DETAIL_SPACING
            if len(node.children) > 1:
                node_top_base = node.shape.bottom + 2 * DETAIL_SPACING
            
            for i, c in enumerate(node.children):
                node_top = node_top_base
                if c.is_direction:
                    node_left = node.shape.left - i * (DETAIL_BOX_WIDTH + DETAIL_SPACING)
                else:
                    node_left = node.shape.right + i * (DETAIL_BOX_WIDTH + DETAIL_SPACING) - DETAIL_BOX_WIDTH
                self.layout_node(c, node_left, node_top) 
                

    def apply(self, root):
        """Main layout entry point"""
        rw, rh = MAIN_TOPIC_BOX_WIDTH, MAIN_TOPIC_BOX_HEIGHT
        root_x = (SLIDE_WIDTH / 2) - (rw / 2)
        root_y = TOP_MARGIN
        self.layout_node(root, root_x, root_y)
        # Check and resolve all overlaps after layout is complete
        self.resolve_overlaps()  

if __name__ == "__main__":
    pass
