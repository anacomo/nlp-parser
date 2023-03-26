# imports
from tabulate import tabulate
import copy
import re

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

# * main function
def main():
    # * calculate the left corner table
    TABLE = create_left_corner_table(PRODUCTIONS)
    show_table(TABLE)

if __name__ == "__main__":
    main()
