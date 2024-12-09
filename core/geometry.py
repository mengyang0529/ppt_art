from pptx.util import Inches, Cm
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

class Point:
    def __init__(self, x, y) -> None:
        self.x = Inches(x)
        self.y = Inches(y)

class Box:
    def __init__(self, left, top, width, height) -> None:
        self.left = left
        self.top = top
        self.width = width
        self.height = height

        self.right = self.left + self.width
        self.bottom = self.top + self.height
        self.center = ((self.left+self.right)/2, (self.top+self.bottom)/2)

        self.id = 0
        self.draw_child_id = 0

    def convert_to_box(self, shape):
        self.box = shape

    def copy_to(self, x, y):
        return Box(x, y, self.width, self.height)
    
    def is_overlapping(self, other):
        """Simple rectangle overlap detection"""
        return not (self.right < other.left or self.left > other.right or
                    self.bottom < other.top or self.top > other.bottom)

def shift_subtree(node, dx, dy):
    """Translate node and its children, updating the status in placed_nodes"""
    def _shift(n, dx, dy):
        n.shape = Box(n.shape.left + dx, n.shape.top + dy, n.shape.width, n.shape.height)
        for child in n.children:
            _shift(child, dx, dy)
    _shift(node, dx, dy)
    
if __name__ == '__main__':
    pass