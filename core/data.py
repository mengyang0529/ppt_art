from core.tree import TreeNode

class Data:
    def __init__(self, file_path:str) -> None:
        self.file_path = file_path
        self.nodes_num = 0
        self.color_id = 0
        self.max_level = 0

    def parse_file(self):
        root = None
        stack = []  

        with open(self.file_path, "r") as file:
            for idx, line in enumerate(file):
                line = line.rstrip()  
                if not line:
                    continue  

                level = line.count("    ")  
                node_value = line.lstrip("- ").strip().replace("\n", " ")
                node = TreeNode(node_value)
                node.id = idx
                node.level = level
                self.max_level = max(self.max_level, level)
                if level == 1:
                    node.color_id = self.color_id
                    self.color_id += 1
                if idx == 0:  
                    root = node
                    root.parent = None
                    stack.append((node, level))
                else:
                    while stack and stack[-1][1] >= level:
                        stack.pop()

                    if stack:
                        node.parent = stack[-1][0]
                        stack[-1][0].add_child(node)

                    stack.append((node, level))
                self.nodes_num += 1
        root.max_depth = self.max_level
        return root

if __name__ == "__main__":
    pass