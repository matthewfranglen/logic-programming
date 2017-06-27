import unittest

from lib.family_tree import MARRIAGE, FATHER, MOTHER, make_family_tree

class TestTreeGeneration(unittest.TestCase):

    def test_no_ancestors(self):
        self.assertEqual(0, len(make_family_tree(0, 0)))
        self.assertEqual(0, len(make_family_tree(0, 10)))

    def test_small_tree(self):
        family_tree = make_family_tree(25, 25)

        self.assertLessEqual(5, len(family_tree))

    def test_large_tree(self):
        family_tree = make_family_tree(25, 25)

        self.assertLessEqual(25, len(family_tree))

        self.assertTrue(any(person.is_male() for person in family_tree))
        self.assertTrue(any(person.is_female() for person in family_tree))

        self.assertTrue(any(edge[2] == MARRIAGE for edge in family_tree.edges(keys=True)))
        self.assertTrue(any(edge[2] == FATHER for edge in family_tree.edges(keys=True)))
        self.assertTrue(any(edge[2] == MOTHER for edge in family_tree.edges(keys=True)))

if __name__ == '__main__':
    unittest.main()
