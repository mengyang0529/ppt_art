
class TreeNode:
    def __init__(self, value:str):
        self.level = 0
        self.value = value
        self.id = 0
        self.parent = None
        self.shape = None
        self.draw_child_id = 0
        self.max_depth = 0
        self.children = []
        self.is_above = True
        self.required_width = 0
        self.required_height = 0
    
    def add_child(self, node):
        self.children.append(node)
    
    def remove_node(self):
        print("TBD")
        pass

    def find_parent(self, level):
        """Find the level=1 parent of the current node"""
        if self.level < level:  # If current node is already at level=1, return None
            return None
        if self.parent.level == level:  # If current node's parent is at level=1, return it
            return self.parent
        current = self.parent
        while current and current.level > level:  # Traverse up until finding the level=1 node
            current = current.parent
        return current  # Return level=1 parent (returns None if not found)

    def display(self, level=0):
        print(" " * level * 2 + str(self.value), str(self.id), str(self.parent_id))
        for child in self.children:
            child.display(level + 1)

if __name__ == "__main__":
    pass