import os
import sys
import random

fastafn = sys.argv[1]
if "--codenames" in sys.argv:
    codenames = True
else:
    codenames = False
if "--shuffle" in sys.argv:
    shuffle = True
else:
    shuffle = False

# Read
seqs = {}
snames = []
with open(fastafn) as fastaf:
    for line in fastaf:
        if line.startswith(">"):
            sname = line[1:].strip()
            if sname in snames:
                print("ERROR: name {0} is duplicated".format(sname))
                exit(1)
            snames.append(sname)
            seqs[sname] = ""
        else:
            # Does not count insertion columns!
            seqs[sname] += "".join([ x for x in line.strip() if x != "." and x == x.upper()]).replace("U", "C")

# Deletes duplicated sequences
sseqs = set()
snames_new = []
for name in snames:
    if seqs[name] not in sseqs:
        snames_new.append(name)
    sseqs.add(seqs[name])
snames = snames_new

# Activate codenames in case a name is repeated
sset = set()
for name in snames:
    if sname[:10] in sset:
        codenames = True
    sset.add(sname[:10])

# Codenames
cnd = {}
if codenames:
    for iname, name in enumerate(snames):
        cnd[name] = "{0:010d}".format(iname)
    cn_fn = fastafn.replace(".fasta","").replace(".fa","").replace(".afa","") + "_codenames.txt"
    with open(cn_fn, "w") as f:
        for name in snames:
            f.write("{0:10s}\t{1}\n".format(cnd[name], name))
else:
    for name in snames:
        cnd[name] = name

#
delcol = []
for i in range(len(seqs[snames[0]])):
    allgap = True
    for name in snames:
        if seqs[name][i] != "-":
            allgap = False
            break
    if allgap:
        delcol.append(i)
if delcol:
    for name in snames:
        seqs[name] = "".join([c for ic, c in enumerate(seqs[name]) if ic not in sorted(delcol, reverse=True)])

# Convert
if shuffle:
    random.shuffle(snames)
print("{0:4} {1:5}".format(len(snames), len(seqs[snames[0]])))
for sname in snames:
    s = seqs[sname]
    print("{0:11} {1} {2} {3} {4} {5} {6}".format(cnd[sname][:10], s[0:10], s[10:20], s[20:30], s[30:40], s[40:50], s[50:60]))

for i in range(60, len(seqs[snames[0]]), 60):
    print("")
    for sname in snames:
        s = seqs[sname]
        print("            {0} {1} {2} {3} {4} {5}".format(s[i+0:i+10], s[i+10:i+20], s[i+20:i+30], s[i+30:i+40], s[i+40:i+50], s[i+50:i+60]))
