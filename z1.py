import os
import re
import random
import unittest


def count_files(path):
    count: int = 0
    for file in os.scandir(path):
        if os.path.isfile(file):
            count += 1
        else:
            count += count_files(file)
    return count


def print_files(path):
    for file in os.scandir(path):
        if os.path.isfile(file):
            print(file)
        else:
            print_files(file)


def erase_words(words, text):
    for word in words:
        text = re.sub(word, "", text)
    return text


def swap_words(swap, swap_to, text):
    for i in range(len(swap)):
        text = re.sub(swap[i], chr(i), text)
    for i in range(len(swap_to)):
        text = re.sub(chr(i), swap_to[i], text)
    return text


def sort1(numbers):
    for i in range(len(numbers) - 1):
        i = len(numbers) - i - 1
        for n in range(i):
            if numbers[n] > numbers[n + 1]:
                temp = numbers[n]
                numbers[n] = numbers[n + 1]
                numbers[n + 1] = temp
    return numbers


def sort2(numbers):
    ret_numbers = []
    for i in range(len(numbers)):
        i = len(numbers) - i - 1
        maxim = numbers[0]
        for n in range(i):
            n += 1
            if numbers[n] > maxim:
                maxim = numbers[n]
        ret_numbers.append(maxim)
    ret_numbers.reverse()
    return ret_numbers


class Node:
    def __init__(self, value=None):
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __str__(self):
        return f"Node({self.value})"

    def traverse(self):
        nodes = [self]
        for child in self.children:
            nodes.extend(child.traverse())
        return nodes


class Tree:
    def __init__(self, root=None):
        self.root = root

    def __str__(self):
        if not self.root:
            return "Tree is empty"
        return "\n".join(str(node) for node in self.root.traverse())

    def add_node(self, parent, child):
        parent.add_child(child)


class TestTreeStructure(unittest.TestCase):

    def test_node_creation(self):
        node = Node("root")
        self.assertEqual(node.value, "root")
        self.assertEqual(len(node.children), 0)

    def test_add_child(self):
        parent = Node("parent")
        child = Node("child")
        parent.add_child(child)
        self.assertEqual(len(parent.children), 1)
        self.assertEqual(parent.children[0].value, "child")

    def test_traverse(self):
        root = Node("root")
        child1 = Node("child1")
        child2 = Node("child2")
        root.add_child(child1)
        root.add_child(child2)
        child1_1 = Node("child1_1")
        child1.add_child(child1_1)
        tree = Tree(root)
        nodes = tree.root.traverse()
        self.assertEqual([node.value for node in nodes], ["root", "child1", "child1_1", "child2"])

    def test_tree_str(self):
        root = Node("root")
        child1 = Node("child1")
        child2 = Node("child2")
        root.add_child(child1)
        root.add_child(child2)
        tree = Tree(root)
        tree_str = str(tree)
        self.assertIn("Node(root)", tree_str)
        self.assertIn("Node(child1)", tree_str)
        self.assertIn("Node(child2)", tree_str)

    def test_empty_tree_str(self):
        tree = Tree()
        tree_str = str(tree)
        self.assertEqual(tree_str, "Tree is empty")


print_files(r"C:\Users\R\OneDrive\Pulpit\TEST")
print(count_files(r"C:\Users\R\OneDrive\Pulpit\TEST"))
print(erase_words(["cde", "ab"], "ab cde.fg.cde."))
print(swap_words(["cd", "ab"], ["abc", "cd"], "abxxcd"))
numbs = []
for i in range(10):
    numbs.append(random.randint(1, 100))
print(numbs)
if sort1(numbs) == sorted(numbs):
    print("ok 1")
if sort2(numbs) == sorted(numbs):
    print("ok 2")
root = Node("root")
node1 = Node("node1")
node2 = Node("node2")
node11 = Node("node11")
node21 = Node("node21")
node22 = Node("node22")
