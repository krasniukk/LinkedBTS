"""
File: bstnode.py
Author: Ken Lambert
"""

class BSTNode(object):
    """Represents a node for a linked binary search tree."""

    def __init__(self, data, left = None, right = None):
        self.data = data
        self.left = left
        self.right = right

    def num_children(self):
        children = 0
        if self.left:
            children += 1
        if self.right:
            children += 1

        return children
