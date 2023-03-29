import nltk

grammar = """S -> NP VP
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
NN -> show | book
PRP -> I
VBP -> am
VBG -> watching
DT -> a
DT -> the
MD -> will"""

# so that I don't use the strings anymore
CFG = nltk.grammar.CFG.fromstring(grammar)

# normalise the grammar to have max 2 nodes in each production
CNG_GRAMMAR = CFG.chomsky_normal_form()
# this would remove the words, so we still use the grammar

def get_depth(nonterminal, trees):
    return [tree for tree in trees if tree.label() == nonterminal]

def compute_lhs(nt_list1, nt_list2, tree_up, tree_down):
    nt_list, trees = [], []
    for nt in nt_list1:
        prods = CNG_GRAMMAR.productions(rhs = nt)
        for prod in prods:
            if prod.rhs()[1] in nt_list2:
                nt_list.append(prod.lhs())

                left = get_depth(nt, tree_up)
                right = get_depth(prod.rhs()[1], tree_down)

                for l_node in left:
                    for r_node in right:
                        x = nltk.Tree(prod.lhs(), [l_node, r_node])
                        if x not in trees:
                            trees.append(x)
    return nt_list, trees

def parse(sentence):
    n = len(sentence)

    chart = [[ set() for i in range(n+1)] for i in range(n+1)]
    nodes = [[[] for i in range(n+1)] for i in range(n+1)]

    # populate the chart with diagonals
    for i in range(n):
        for prod in CFG.productions(rhs=nltk.Nonterminal(sentence[i])):
            chart[i][i+1].add(prod.lhs())
            nodes[i][i+1].append(nltk.Tree(prod.lhs(), [prod.rhs()[0]]))

    # compute the chart
    for w in range(2, n + 1):
        for i in range(0, n - w + 1):
            for j in range(1, w):
                prods, trees = compute_lhs(chart[i][i + j], chart[i + j][i + w],
                                           nodes[i][i + j], nodes[i + j][i + w])

                for prod in prods:
                    chart[i][i + w].add(prod)   
                for tree in trees:
                    nodes[i][i + w].append(tree)

    return chart, nodes

def print_trees(trees):
    n = len(trees)
    count = 1
    for tree in trees:
        if count < n:
            print(tree[count])
            count += 1

    
def checkparser(sentence):
    chart, nodes = parse(sentence)
    print_trees(nodes)

def main():
    sentence = "I am watching a show".split()
    checkparser(sentence)

if __name__ == "__main__":
    main()
