from timeline.basics import *
from core.geometry import *
from timeline.classic_shapes import *
from timeline.horizontal.measure import MeasureLayout
from timeline.horizontal.apply import ApplyLayout
from timeline.horizontal.lines import BuildLines

class Layout():
    def __init__(self):
        pass

    def collect_layout_boxes(self, node, layout_boxes):
        layout_boxes[node.id] = node.shape
        for child in node.children:
            self.collect_layout_boxes(child, layout_boxes)

    def create_layout(self, root_node):
        measure = MeasureLayout()
        measure.measure(root_node)

        layout = ApplyLayout()
        layout.apply(root_node)

        layout_boxes = {}
        self.collect_layout_boxes(root_node, layout_boxes)

        lines_builder = BuildLines()
        layout_lines = lines_builder.build(root_node)

        return layout_boxes, layout_lines

if __name__ == "__main__":
    pass
