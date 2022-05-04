import sys
import numpy as np

def seqid(seq1, seq2):
    L = len(seq1)
    p, n = 0, 0
    for i in range(L):
        if seq1[i] == "-" or seq2[i] == "-":
            continue
        if seq1[i] == seq2[i]:
            p += 1
        n += 1
    if not n:
        return 0
    else:
        return p/n


names = []
seqs = {}
fastafn = sys.argv[1]
with open(fastafn) as f:
    for line in f:
        if line.startswith(">"):
            name = line[1:].strip()
            names.append(name)
            seqs[name] = ""
        else:
            seqs[name] += line.strip()
for name in names:
    if "." in seqs[name] or seqs[name].upper() != seqs[name]:
        print("No insertions!")
        exit(1)


N = len(names)
seqid_mtx = np.ones((N,N))
for iname1, name1 in enumerate(names):
    for iname2, name2 in [(i,x) for i,x in enumerate(names) if i>iname1]:
        seqid_mtx[iname1, iname2] = seqid_mtx[iname2, iname1] = seqid(seqs[name1], seqs[name2])

cnd = {}
for iname, name in enumerate(names):
    cnd[name] = "{0:010d}".format(iname)
cn_fn = fastafn.replace(".fasta","").replace(".fa","").replace(".afa","") + "_codenames.txt"
with open(cn_fn, "w") as f:
    for name in names:
        f.write("{0:10s}\t{1}\n".format(cnd[name], name))

print(N)
for iname, name in enumerate(names):
    print("{0} {1}".format(cnd[name], " ".join(["{0:6.4f}".format(x) for x in seqid_mtx[iname,:].tolist()])))
