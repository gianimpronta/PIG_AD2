#!/usr/bin/env python
# coding: UTF-8
# vim: tabstop=4:softtabstop=4:shiftwidth=4
#
## @package BalancedBSTSet
#
#  Balanced Binary Tree.
#
#  @author Gianpaolo Martins Impronta
#   @since 27/02/2019
#

from __future__ import print_function

import math
import sys
from BSTSet import cmp, BSTSet, generateRandomArray
try:
    from peekable import peekable
except ImportError:
    ## return an iterator for a BSTSet .
    def peekable(it): #pragma: no cover
        return it.iterator()

##
# Balanced Binary search tree implementation of the Collections interface.
#  - The \_\_contains\_\_() and remove() methods of Collections Abstract Base Classes are overridden
#    to search the tree without using the iterator.
#
#   To run:
#      - python BalancedBSTSet.py
#
#   @author Gianpaolo Martins Impronta
#   @since 27/02/2019
#   @see <a href="http://en.wikipedia.org/wiki/Scapegoat_tree">Scapegoat tree</a>
#   @see <a href="http://cg.scs.carleton.ca/~morin/teaching/5408/refs/gr93.pdf">Original paper</a>
#   @see <a href="https://docs.python.org/3/library/collections.abc.html">Collections Abstract Base Classes</a>
#   @see <a href="https://walkccc.github.io/CLRS/Chap17/Problems/17-3/">Amortized weight-balanced trees</a>
#
class BalancedBSTSet(BSTSet):

    ## Node type for this implementation
    #
    class Node(BSTSet.Node):

        ##  Constructor given a data object and the parent of this node.
        #
        #  @param key data object.
        #  @param parent parent node.        #
        def __init__(self, key, parent):

            ## Counter contains the number of nodes of the subtree starting in this node.
            self.counter = 0
            super().__init__(key, parent)

    ## For self-balacing bst, alpha is the criterion used to rebalance the tree.
    # If isSelfBalancing is True, builds a self balanced BST, and alpha = top/bottom
    # If isSelfBalancing is False, top and bottom will be ignored
    # if bottom is zero, top = 2 e bottom =3.
    #
    # @param isSelfBalancing indicates whether or not it is a self-balacing tree
    # @param top alpha fraction enumerator
    # @param bottom alpha fraction denominator
    def __init__(self, isSelfBalancing=False, top =0, bottom =0):
        super().__init__()
        ## stores whether or not this is a self-balancing tree
        self.self_balancing = isSelfBalancing

        if bottom == 0:
            ## initialize bottom attribute
            self.bottom = 3
            ## initialize top attribute
            self.top = 2
        else:
            self.top = top
            self.bottom = bottom

        ## Root of this tree
        self.__root = None

        ## Number of elements in this tree
        self.__size = 0

    ##
    # Returns a read-only view of the root node of this tree.
    # @return root node of this tree.
    #
    def root(self):
        return self.__root

    ## Return whether this tree is empty.
    def isEmpty(self):
        return self.__root is None

    ##
    #  Executes an in order traversal of the tree rooted at a given node.
    #
    #  @param node root.
    #  @param arr array for holding the node data.
    #  @return arr.
    #
    def __inOrder(self, node, arr):
        if arr is None: #pragma: no cover
            arr = []
        if node is not None:
            self.__inOrder(node.left, arr)
            arr.append(node)
            self.__inOrder(node.right, arr)

        return arr


    ##
    # Adds the given object to this tree.
    #
    # @param key given object.
    # @return True if the object was added, and False otherwise.
    #
    def add(self, key):
        if self.__root is None:
            self.__root = self.Node(key, None)
            self.__size += 1
            self.count_node(self.__root)
            return True

        current = self.__root
        while True:
            comp = current.compareTo(key)
            if comp == 0:
                # key is already in the tree
                return False
            elif comp > 0:
                if current.left is not None:
                    current = current.left
                else:
                    current.left = self.Node(key, current)
                    self.__size += 1

                    # updates all tree counters
                    self.count_node(self.__root)

                    # rebalance tree if it is a self-balacing tree
                    if self.self_balancing:
                        unbalanced_node = self.find_unbalanced(current)
                        if unbalanced_node is not None:
                            self.rebalance(unbalanced_node)
                    return True
            else:
                if current.right is not None:
                    current = current.right
                else:
                    current.right = self.Node(key, current)
                    self.__size += 1

                    # updates all tree counters
                    self.count_node(self.__root)

                    # rebalance tree if it is a self-balacing tree
                    if self.self_balancing:
                        unbalanced_node = self.find_unbalanced(current)
                        if unbalanced_node is not None:
                            self.rebalance(unbalanced_node)
                    return True


    ##
    # Removes the given object from this tree.
    #
    # @param obj given object.
    # @return True if the object was found, and False otherwise.
    #
    def remove(self, obj):
        n = self.findEntry(obj)
        if n is None:
            return False
        parent = n.parent

        self.unlinkNode(n)
        # updates all tree counters
        self.count_node(self.__root)

        # rebalance tree if it is a self-balacing tree
        if self.self_balancing:
            unbalanced_node = self.find_unbalanced(parent)
            if unbalanced_node is not None:
                self.rebalance(unbalanced_node)

        return True

    ##
    # Returns the node containing key, or None if the key is not
    # found in the tree.
    # @param key
    # @return the node containing key, or None if not found.
    #
    def findEntry(self, key):
        current = self.__root
        while current is not None:
            comp = current.compareTo(key)
            if comp == 0:
                return current
            elif comp > 0:
                current = current.left
            else:
                current = current.right
        return None


    ##
    # Removes the given node, preserving the binary search
    # tree property of the tree.
    #
    # @param n node to be removed.
    #
    def unlinkNode(self, n):
        # first deal with the two-child case copy
        # data from successor up to n, and then delete successor
        # node instead of given node n
        startNode = None
        if n.left is not None and n.right is not None:
            s = self.successor(n)
            n.data = s.data
            n = s  # causes s to be deleted in code below
            startNode = s.parent

        # n has at most one child
        replacement = None
        if n.left is not None:
            replacement = n.left
        elif n.right is not None:
            replacement = n.right

        # link replacement on tree in place of node n
        # (replacement may be None)
        if n.parent is None:
            self.__root = replacement
        else:
            if n == n.parent.left:
                n.parent.left = replacement
            else:
                n.parent.right = replacement

        if replacement is not None:
            replacement.parent = n.parent

        self.__size -= 1

    ## Returns an iterator for this tree.
    def iterator(self):
        return self.BSTIterator(self)

    ## Returns the number of elements in this tree.
    def __len__(self):
        return self.__size



    ## Indexing operator [].
    #
    # @throw IndexError.
    # @param ind index to retrieve.
    # @return ind-ith value in the tree, or an exception.
    #
    def __getitem__(self, ind):
        if ind < 0 or ind >= self.__size:
            raise IndexError

        for i, n in enumerate(self.iterator()):
            if i == ind:
                return n

    ## Iterator as a generator.
    #
    # Generators are functions having an yield keyword.
    # Any function which has “yield” in it is a generator.
    #
    # Generator takes care of creating the iterable.
    # It also takes care of creating the underlying iterator.
    # And next() of this iterator() is such that it returns each ‘yield’
    #
    # @see https://www.agiliq.com/blog/2017/11/how-python-generators-are-similar-iterators/
    #
    def __iter__(self):
        for n in self.iterator():
            yield n

    ## Return the height of this tree.
    # The height of a tree is the height of its root node.
    #
    def height(self):
        return self.getHeight(self.__root)

    ## Return the height of a subtree.
    # The height of a node is the number of edges on the longest path between that node and a leaf.
    # The height of a leaf is 0.
    #
    # @param root node of the subtree.
    #
    def getHeight(self, root):
        if root is not None:
            return 1 + max(self.getHeight(root.left), self.getHeight(root.right))
        else:
            return -1

    ##
    # Returns a representation of this tree as a multi-line string.
    # The tree is drawn with the root at the left and children are
    # shown top-to-bottom.  Leaves are marked with a "-" and non-leaves
    # are marked with a "+".
    #
    def __repr__(self):
        sb = []
        self.__toStringRec(self.__root, sb, 0)
        return ''.join(sb)

    ## Prints the nodes of this tree in order.
    def __str__(self):
        st = ""
        for n in self:
            st += str(n) + " "
        return st

    ##
    # Preorder traversal of the tree that builds a string representation
    # in the given StringBuilder.
    #
    # @param n root of subtree to be traversed.
    # @param sb list in which to create a string representation.
    # @param depth depth of the given node in the tree.
    #
    def __toStringRec(self, n, sb, depth):
        sb.append("  " * depth)

        if n is None:
            sb.append("-\n")
            return

        if (n.left is not None or n.right is not None):
            sb.append("+ ")
        else:
            sb.append("- ")

        sb.append(str(n))
        sb.append("\n")
        if (n.left is not None or n.right is not None):
            self.__toStringRec(n.left, sb, depth + 1)
            self.__toStringRec(n.right, sb, depth + 1)

    ##
    # Execute the rebalancing operation of the subtree starting from a given node.
    #
    # @param bstNode root node of the subtree
    def rebalance(self, bstNode):

        ## Reorganize the subtree recursively without creating another tree,
        # returning it's new root node
        #
        # @param nodes ordered node list
        # @param start initial index
        # @param end end index
        # @param parent node that will serve as root parent
        # @return subtree root node
        def rebuild_tree(nodes, start, end, parent):
            if start > end:
                return None

            # finds midpoint that will serve as root for subtree
            mid = int(math.ceil(start + (end - start) / 2.0))
            node = nodes[mid]
            node.parent = parent
            node.left = rebuild_tree(nodes, start, mid - 1, node)
            node.right = rebuild_tree(nodes, mid + 1, end, node)
            return node

        # empty tree
        if bstNode is None:
            return
        node_parent = bstNode.parent

        # creates list of ordered nodes
        node_list = []
        self.__inOrder(bstNode, node_list)

        subtree_root = rebuild_tree(node_list, 0, len(node_list)-1, bstNode.parent)

        # bstNode was tree root
        if subtree_root.parent is None:
            self.__root = subtree_root

        # bstNode was left node
        elif node_parent.left == bstNode:
            node_parent.left = subtree_root

        # bstNode was right node
        else:
            node_parent.right = subtree_root

        # update all tree counters
        self.count_node(self.__root)

    ##
    # Recursively go upward in the tree from a given node until it finds a
    # node that is the root of an unbalanced subtree and returns it,
    # if not even the tree root is unbalanced, returns None.
    #
    # @param n starting node
    # @return unbalanced node or None

    def find_unbalanced(self, n):
        while self.is_balanced(n):
            if n == self.__root:
                return None
            n = n.parent
        return n


    ##
    # Checks if a subtree whose root is a given node is balanced.
    #
    # @param node root node of subtree
    # @return returns True if the subtree if balanced and False otherwise.
    #
    def is_balanced(self, node):
        # empty subtree
        if node is None:
            return True
        size = node.counter

        # leaf nodes have l and r = 0
        l = 0
        r = 0

        # checking if there's nodes in left and right
        if node.left:
            l = node.left.counter
        if node.right:
            r = node.right.counter

        # balancing equations
        if l * self.bottom > size * self.top:
            return False

        if r * self.bottom > size * self.top:
            return False

        return True

    ##
    # Updates all the subtree counters recursively from a root node.
    # A root node counter is the sum of the left subtree counter and
    # the right subtree counter.
    #
    # @param current root node
    # @return number of elements of the root node
    #
    def count_node(self, current):
        # leaf node
        if current is None:
            return 0

        current.counter = self.count_node(current.left) + \
                          self.count_node(current.right) + 1

        return current.counter

    ##
    # Iterator implementation for this binary search tree. The elements
    # are returned in ascending order according to their natural ordering.
    #
    class BSTIterator(object):
        ## return the smallest value of the tree.
        def getSmallestValue(self, n):
            if n is not None:
                while n.left is not None:
                    n = n.left
            return n

        ##
        # Constructs an iterator starting at the smallest
        # ot largest element in the tree.
        #
        def __init__(self, tree):
            ## Node returned by last call to next() and available
            #  for removal. This field is None when no node is
            #  available to be removed.
            self.__pending = None

            ## The tree to be traversed.
            #  Inner classes do not have access to outer class variables.
            self.__tree = tree

            ## Node to be returned by next call to next().
            self.__current = self.getSmallestValue(self.__tree.root())

        ## Forward iterator.
        def __iter__(self):
            # start out at smallest value
            self.__current = self.getSmallestValue(self.__tree.root())
            return self

        ##
        # Whether current is not None.
        #
        def hasNext(self):
            return self.__current != None

        ## Return the content of the current node without advancing.
        def peek(self):
            if self.__current is None:
                return None
            return self.__current.data

        ##
        # Returns current node, which is saved in pending.
        # Current is set to successor(current).
        #
        def __next__(self):
            if not self.hasNext(): raise StopIteration
            self.__pending = self.__current
            self.__current = self.__tree.successor(self.__current)
            return self.__pending.data

        ## For python 2.
        def next(self):
            return self.__next__()

        ##
        # Removes the node returned by the last call to next().
        # Current pos to the successor of
        # pending, but if pending has two children, then
        # unlinkNode(pending) will copy the successor's data
        # o pending and delete the successor node.
        # So in this case, we want to end up with current
        # poing to the pending node.
        #
        def remove(self):
            if self.__pending is None: raise IndexError
            parent = self.__pending.parent
            if self.__pending.left is not None and self.__pending.right is not None:
                self.__current = self.__pending

            self.__tree.unlinkNode(self.__pending)
            self.__pending = None

            # update all tree counters
            self.__tree.count_node(self.__tree.root())

            # rebalance tree if it is a self-balacing tree
            if self.__tree.self_balancing:
                unbalanced_node = self.__tree.find_unbalanced(parent)
                if unbalanced_node is not None:
                    self.__tree.rebalance(unbalanced_node)



## set intersection given two mutable ordered sequences .
# @see https://docs.python.org/3.0/library/stdtypes.html#mutable-sequence-types
#
def set_intersection(itr1, itr2): #pragma: no cover
    p1 = peekable(itr1)
    p2 = peekable(itr2)
    result = type(itr1)()
    while p1.hasNext() and p2.hasNext():
        i1 = p1.peek()
        i2 = p2.peek()
        if i1 < i2:
            next(p1)
        elif i2 < i1:
            next(p2)
        else:
            result.append(i1)
            next(p1)
            next(p2)
    return result


##
# Set union given two mutable ordered sequences, return a sequence of the same
# type as itr1 containing all elements of itr1 and itr2 that are not duplicates.
#
# @param itr1 mutable ordered sequence
# @param itr2 mutable ordered sequence
# @return mutable ordered sequence of type as itr1

def set_union(itr1, itr2):#pragma: no cover
    p1 = peekable(itr1)
    p2 = peekable(itr2)
    result = type(itr1)()
    while p1.hasNext() or p2.hasNext():
        i1 = p1.peek()
        i2 = p2.peek()

        try:
            if i1 < i2:
                result.append(i1)
                next(p1)
            elif i2 < i1:
                result.append(i2)
                next(p2)
            else:
                result.append(i1)
                next(p1)
                next(p2)
        except TypeError:
            if p1.isLast() and not p2.isLast():
                result.append(i2)
                next(p2)
            elif p2.isLast() and not p1.isLast():
                result.append(i1)
                next(p1)
    return result


##
# Set difference given two mutable ordered sequences, return a sequence of the same
# type as itr1 containing all elements of itr1 that are not on itr2.
#
# @param itr1 mutable ordered sequence
# @param itr2 mutable ordered sequence
# @return mutable ordered sequence of type as itr1
def set_diff(itr1, itr2): #pragma: no cover
    p1 = peekable(itr1)
    result = type(itr1)()
    flag = False

    while p1.hasNext():
        i1 = p1.peek()
        p2 = peekable(itr2)
        flag = False
        while p2.hasNext():
            i2 = p2.peek()
            if i2 == i1:
                flag = True
                break
            else:
                next(p2)

        if not flag:
            result.append(i1)
        next(p1)
    return result


##
#  Main function for testing.
#
#  args not used.
#
def main(args=None):  # pragma: no cover
    if args is None:
        args = sys.argv

    arr1 = [5, 4, 2, 16, 10, 7, 20, 14, 15, 12]
    arr2 = generateRandomArray(15, 500)
    arr3 = generateRandomArray(20, 500)
    arr4 = generateRandomArray(20, 50)
    arr5 = generateRandomArray(20, 90)
    arr6 = [1, 2, 3, 4, 5, 6, 7, 8]
    arr7 = [6, 7, 8, 9, 10, 11, 12]
    arr8 = []


    arr = arr4
    bst = BalancedBSTSet()
    for i in arr:
        bst.add(i)

    print("Original tree: height = %d\n%r" % (bst.height(),bst))

    a = bst.toArray()
    print("toArray:")
    for i in a:
        print("%s, " % i, end="")
    print("\b\b: size = %d, len = %d" % (len(a), len(bst)))

    print("\nKeys in ascending order:")
    print(bst)

    if len(bst) > 3:
        print("\n\nbst[3] = %d" % bst[3])
    nid = 0

    for i in arr:
        bst.remove(i)
        bst.rebalance(bst.root())
        print("%r" % bst)

    bst2 = BalancedBSTSet()
    bst3 = BalancedBSTSet()
    bst4 = BalancedBSTSet()

    for i in arr6:
        bst2.add(i)
    for i in arr7:
        bst3.add(i)
    for i in arr8:
        bst4.add(i)


    print(set_intersection(bst2, bst3))
    # print(set_union(bst2, bst3))
    print(set_diff(bst2, bst3))
    print(set_diff(bst3, bst2))
    print(set_diff(bst3, bst4))

    # bst5 = set_union(bst2, bst3)
    # print('%r' % bst5)


if __name__ == "__main__": #pragma: no cover
    main()
