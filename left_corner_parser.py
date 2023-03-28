# imports
from tabulate import tabulate
import copy
import re

# grammar text - pefferably do not use |
PRODUCTIONS = """S -> NP VP
S -> VP
NP -> DT NN
NP -> DT JJ NN
NP -> PRP
VP -> VBP VP
VP -> VBP NP
VP -> VBG NP
VP -> TO VP
VP -> VB
VP -> VB NP
NN -> 'show' | 'book'
PRP -> 'I'
VBP -> 'am'
VBG -> 'watching'
VB -> 'show'
DT -> 'a'
DT -> 'the'
MD -> 'will'""".split('\n')

SENTENCE = "I am watching a show".split()

# util functions for creating and printing the left corner table
def create_left_corner_table(prods: list) -> dict:
    left_corner_table = {}

    for prod in prods:
        nonterminal, sequence = prod.split(' -> ')

        # check if it is non-terminal
        if nonterminal not in left_corner_table.keys():
            left_corner_table[nonterminal] = list()
        seqs = sequence.split('|')
        for s in seqs:
            first_symbol = re.sub('\'', '', s.split()[0])
            if first_symbol not in left_corner_table[nonterminal]:
                left_corner_table[nonterminal].append(first_symbol)

    return left_corner_table


def show_table(table: dict) -> None:
    show = [[S, ', '.join(table[S])] for S in table]
    print(tabulate(show, headers=['Symbol', 'Left corner'],
                   tablefmt='simple_outline'))


# * calculate the left corner table
TABLE = create_left_corner_table(PRODUCTIONS)

class TreeNode:
    def __init__(self, symbol: str, parent: str, children: list):
        self.symbol = symbol
        self.parent = parent
        self.children = children

    def __str__(self) -> str:
        return ' (' + self.symbol + \
            ''.join([str(c) for c in self.children]) + ')'

# bottom up search
def get_parent_chain(symbol: str):
    chain = [parent for parent in TABLE if symbol in TABLE[parent]]
    return list(set(chain))


def compute_sequence(parent:str, node_string:str):
    for production in PRODUCTIONS:
        nonterminal, sequence = production.split(' -> ')

        if nonterminal == parent:
            sequences = sequence.split('|')
            for seq in sequences:
                s = re.sub('\'', '', seq).split()
                if node_string == s[0]:
                    return s


def search(word: str, root: TreeNode, nonterminals_stack: list):
    word_node = TreeNode(word, None, [])

    # bottom up search until we find S
    if word == root.symbol:
        return [root]

    parent_chain: list(str) = get_parent_chain(word)
    parsed = []

    for parent in parent_chain:
        parent_nodes = search(parent, root, nonterminals_stack)
        for parent_node in parent_nodes:
            n1 = copy.deepcopy(word_node)
            n1.parent = parent_node
            parent_node.children.append(n1)
            sequence = compute_sequence(parent, word)

            for nonterminal in sequence[1:]:
                n2 = TreeNode(nonterminal, parent_node, [])
                parent_node.children.append(n2)
                nonterminals_stack.append(n2)
            parsed.append(n1)

    return parsed

def parse():
    i = 0
    # start with sentence
    S = TreeNode('S', None, [])
    nonterminals_stack = [S]
    while nonterminals_stack and i < len(SENTENCE):
        node = nonterminals_stack.pop(0)
        # search for word
        search(SENTENCE[i], node, nonterminals_stack)
        i += 1
    # print the sentence
    print(S)


# * main function
def main():
    show_table(TABLE)
    parse()

if __name__ == "__main__":
    main()
