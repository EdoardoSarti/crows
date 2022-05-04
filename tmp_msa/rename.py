import sys
import ete3

codenames_fn = sys.argv[1]
tree_fn = sys.argv[2]

code_d = {}
with open(codenames_fn) as f:
    for line in f:
        fields = line.split("\t")
        code_d[fields[0]] = fields[1].split()[0]

t = ete3.Tree(tree_fn)
for l in t.get_leaves():
    l.name = code_d[l.name]

t.write(outfile=tree_fn+".wl.nhx")
