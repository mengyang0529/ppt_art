from timeline.basics import *
from core.geometry import *
from timeline.classic_shapes import *

class BuildLines:
    def __init__(self):
        self.layout_lines = {}
    
    def update_lines(self, node, pt1, pt2):
        if node.id not in self.layout_lines:
            self.layout_lines[node.id] = []
        self.layout_lines[node.id].append((pt1, pt2))

    def handle_level_0_lines(self, node):
        self.update_lines(node, Point(0,0), Point(0,0))

    def handle_level_1_lines(self, node):
        parent = node.parent
        idx = parent.children.index(node)
        
        if idx == 0:
            pt1 = Point(parent.shape.right, parent.shape.center[1])
        else:
            prev_node = parent.children[idx - 1]
            pt1 = Point(prev_node.shape.right, prev_node.shape.center[1])

        pt2 = Point(node.shape.left, node.shape.center[1])
        self.update_lines(node, pt1, pt2)

    def handle_level_2_lines(self, node):
        parent = node.parent
        if node.id == parent.children[0].id:
            if node.level == 2:
                pt1 = Point(parent.shape.center[0], node.shape.center[1])
                pt2 = Point(node.shape.left, node.shape.center[1])
            else:
                pt1 = Point(parent.shape.right, node.shape.center[1])
                pt2 = Point(node.shape.left, node.shape.center[1])
        else:
            pt1 = Point(node.shape.left - DETAIL_SPACING, node.shape.center[1])
            pt2 = Point(node.shape.left, node.shape.center[1])
        self.update_lines(node, pt1, pt2)

        if node.id == parent.children[-1].id:
            if node.level == 2:
                if node.is_direction:
                    pt3 = Point(parent.shape.center[0], parent.shape.top)
                    pt4 = Point(parent.shape.center[0], node.shape.center[1])
                else:
                    pt3 = Point(parent.shape.center[0], node.shape.center[1])
                    pt4 = Point(parent.shape.center[0], parent.shape.bottom)
            else:
                pt3 = Point(node.shape.left - DETAIL_SPACING, parent.shape.center[1])
                pt4 = Point(node.shape.left - DETAIL_SPACING, node.shape.center[1])
            self.update_lines(node, pt3, pt4)
        
    def handle_level_more_lines(self, node):
        self.handle_level_2_lines(node)

    def build_node_lines(self, node):
        if node.level == 0:
            self.handle_level_0_lines(node)
        elif node.level == 1:
            self.handle_level_1_lines(node)
        elif node.level == 2:
            self.handle_level_2_lines(node)
        else:
            self.handle_level_more_lines(node)

        for c in node.children:
            self.build_node_lines(c)

    def build(self, root):
        self.build_node_lines(root)
        return self.layout_lines


if __name__ == "__main__":
    pass