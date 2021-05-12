"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log, log2, pi, trunc
import random
from time import time


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        node = self._root
        while True:
            if node is None:
                return None
            if item == node.data:
                return node.data
            if item < node.data:
                node = node.left
                continue
            node = node.right
                

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        else:
            node = self._root
            while True:
                if item < node.data:
                    if node.left == None:
                        node.left = BSTNode(item)
                        break
                    node = node.left
                    continue
                if node.right == None:
                    node.right = BSTNode(item)
                    break
                node = node.right

        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def is_leaf(self, node):
        '''Return True if given node does not have any children.'''
        return node.num_children() == 0

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return -1
            return 1 + max(height1(top.left), height1(top.right))
        if self._root is None:
            return 0
        return height1(self._root)

    def write_to_list(self):
        return [el for el in self]

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        if self._root is None:
            return False
        heig = self.height()
        size = self._size
        return heig < 2*log(size + 1, 2) - 1



    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        nodes_in_range = []
        def recurse(node, elem):
            if not node:
                return
            if low <= node.data <= high and node.data not in nodes_in_range:
                nodes_in_range.append(node.data)
            if node.data > elem:
                recurse(node.left, elem)
            else:
                recurse(node.right, elem)

        recurse(self._root, low)
        recurse(self._root, high)
        return nodes_in_range



    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        if self._root is None:
            return []
        nodes = sorted(self.write_to_list())
        print(nodes)
        new_tree = LinkedBST()
        def write_middle(lst):
            if len(lst) == 1:
                new_tree.add(lst[0])
            else:
                new_tree.add(lst[len(lst) // 2])
                print(lst[len(lst) // 2], end= ' ')
                write_middle(lst[0:len(lst)//2])
                if len(lst) > 2:
                    write_middle(lst[len(lst)//2 + 1:])
        write_middle(nodes)
        return new_tree

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """

        def recurse2(node):
            if not node:
                return
            if item < node.data:
                next_value = recurse2(node.left)
                if next_value is not None and (next_value < node.data):
                    return next_value
                return node.data
                
            else:
                next_value = recurse2(node.right)
                if next_value:
                    return next_value
                return

        return recurse2(self._root)

        
            

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        def recurse2(node):
            if not node:
                return
            if item > node.data:
                next_value = recurse2(node.right)
                if next_value is not None and (next_value > node.data):
                    return next_value
                return node.data
                
            else:
                next_value = recurse2(node.left)
                if next_value is not None:
                    return next_value
                return

        return recurse2(self._root)

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        with open(path, 'r') as file:
            words = file.readlines()
        random_words = [words[random.randint(0, 234935)] for _ in range(10000)]
        ordered_bin_tree = LinkedBST(words)
        not_ordered_bin_tree = LinkedBST(sorted(words, key= random.random()))

        def search_by_list():
            start_time = time()
            for word in random_words:
                words.index(word)
            finish_time = time()
            return finish_time - start_time

        def search_by_binar_tree_ordered():
            start_time = time()
            for word in random_words:
                ordered_bin_tree.find(word)
            finish_time = time()
            return finish_time - start_time

        def search_by_binar_tree_not_ordered():
            start_time = time()
            for word in random_words:
                not_ordered_bin_tree.find(word)
            finish_time = time()
            return finish_time - start_time

        def search_by_rebalanced_tree():
            rebalanced_tree = ordered_bin_tree.rebalance()
            start_time = time()
            for word in random_words:
                ordered_bin_tree.find(word)
            finish_time = time()
            return finish_time - start_time

        print('test 1')
        print(search_by_list())
        print('test 2')
        print(search_by_binar_tree_ordered())
        print('test 3')
        print(search_by_binar_tree_not_ordered())
        print('test 4')
        print(search_by_rebalanced_tree())

bt = LinkedBST()
bt.demo_bst('words.txt')


