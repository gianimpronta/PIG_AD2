import unittest
from BalancedBSTSet import BalancedBSTSet, peekable


class BalancedBSTSetTest(unittest.TestCase):

    def test_empty_tree(self):
        bst = BalancedBSTSet()
        self.assertEqual(bst.root(), None)
        self.assertTrue(bst.isEmpty())
        self.assertEqual(len(bst), 0)
        self.assertEqual(bst.height(), -1)

    def test_balanced_unbalanced_tree(self):
        un_bst = BalancedBSTSet()
        self.assertFalse(un_bst.self_balancing)
        bal_bst = BalancedBSTSet(True)
        self.assertTrue(bal_bst.self_balancing)

    def test_top_bottom_tree(self):
        bst  = BalancedBSTSet(top=2, bottom=3)
        self.assertEqual(bst.top, 2)
        self.assertEqual(bst.bottom, 3)


    def test_find_entry(self):
        bst = BalancedBSTSet(True, top=2, bottom=3)
        bst.add(5)
        self.assertFalse(bst.findEntry(1))
        self.assertFalse(bst.findEntry(6))
        self.assertTrue(bst.findEntry(5))

    def test_indexing(self):
        bst = BalancedBSTSet(True, top=2, bottom=3)
        bst.add(5)
        self.assertEqual(bst[0], 5)
        with self.assertRaises(IndexError):
            a = bst[1]

    def test_add_nodes(self):
        # not self balancing tree
        nodes = [4, 3, 2, 5, 6, 1]
        bst = BalancedBSTSet()
        for node in nodes:
            bst.add(node)
        # add duplicate number
        bst.add(1)
        self.assertEqual(len(bst), 6)

        # self balancing tree
        nodes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        bst = BalancedBSTSet(True)
        for node in nodes:
            bst.add(node)
        # add duplicate number
        self.assertEqual(len(bst), 10)

    def test_string_repr(self):
        nodes = [1, 2, 3, 4, 5, 6]
        bst = BalancedBSTSet(False)
        self.assertEqual(f'{bst}', '')
        for node in nodes:
            bst.add(node)
        self.assertEqual(f'{bst}', '1 2 3 4 5 6 ')
        self.assertEqual(f'{bst!r}',
'''+ 1
  -
  + 2
    -
    + 3
      -
      + 4
        -
        + 5
          -
          - 6
''')

    def test_get_height(self):
        nodes = [1, 2, 3, 4, 5, 6]
        bst = BalancedBSTSet(False)
        for node in nodes:
            bst.add(node)
        self.assertEqual(bst.getHeight(bst.root()), 5)

    def test_smallestValue(self):
        nodes = [1, 2, 3, 4, 5, 6]
        bst = BalancedBSTSet(False)
        for node in nodes:
            bst.add(node)
        self.assertEqual(min(bst), 1)
        bst = BalancedBSTSet(True)
        for node in nodes:
            bst.add(node)
        self.assertEqual(min(bst), 1)


    def test_remove_nodes(self):
        nodes = [1, 2, 3, 4, 5, 6]
        bst = BalancedBSTSet(False)
        for node in nodes:
            bst.add(node)
        self.assertEqual(len(bst), 6)
        bst.remove(3)
        self.assertEqual(len(bst), 5)
        bst.remove(3)
        self.assertEqual(len(bst), 5)
        bst.remove(1)
        self.assertEqual(len(bst), 4)
        nodes = [1, 2, 3, 4, 5, 6]
        bst = BalancedBSTSet(True)
        for node in nodes:
            bst.add(node)
        self.assertEqual(len(bst), 6)
        bst.remove(4)
        self.assertEqual(len(bst), 5)
        bst.remove(4)
        self.assertEqual(len(bst), 5)
        bst.remove(1)
        self.assertEqual(len(bst), 4)

    def test_isbalanced(self):
        bst = BalancedBSTSet()
        self.assertTrue(bst.is_balanced(bst.root()))


    def test_rebalance(self):
        bst = BalancedBSTSet()
        bst.rebalance(bst.root())
        self.assertEqual(f'{bst}', '')
        nodes = [1, 2, 3, 4, 5, 6]
        for node in nodes:
            bst.add(node)
        self.assertEqual(f'{bst}', '1 2 3 4 5 6 ')
        bst.rebalance(bst.root())
        self.assertEqual(f'{bst}', '1 2 3 4 5 6 ')
        bst = BalancedBSTSet()
        nodes = [6, 5, 4, 3, 2, 1]
        for node in nodes:
            bst.add(node)
        bst.rebalance(bst.root())
        self.assertEqual(f'{bst}', '1 2 3 4 5 6 ')
        bst = BalancedBSTSet(True)
        nodes = [6, 5, 4, 3, 2, 1]
        for node in nodes:
            bst.add(node)
        bst.rebalance(bst.root())
        self.assertEqual(f'{bst}', '1 2 3 4 5 6 ')
        # self.fail(f'{bst!r}')

    def test_iterator(self):
        bst = BalancedBSTSet(True)
        nodes = [6, 5, 4, 3, 2, 1]
        p1 = peekable(bst)
        self.assertIsNone(p1.peek())
        for node in nodes:
            bst.add(node)
        p1 = peekable(bst)
        self.assertEqual(p1.peek(), 1)
        next(p1)
        next(p1)
        self.assertEqual(p1.peek(), 3)
        next(p1)
        p1.remove()
        next(p1)
        self.assertEqual(p1.peek(), 5)
        next(p1)
        self.assertEqual(p1.peek(), 6)



if __name__ == '__main__':
    unittest.main()