import sys

alnseqs = {}
c = 0
names = []
header = True
with open(sys.argv[1]) as f:
    for line in f:
        seq = "".join(line[12:].split())
        if line[:11].strip() and (not header):
            name = line[:11].strip()
            alnseqs[name] = seq
            names.append(name)
        elif not line[:11].strip():
            alnseqs[names[c%len(names)]] += seq
            c += 1
        header = False

print(len(alnseqs))

seqset = set()
new_alnseqs = {}
new_names = []
for name in names:
    if alnseqs[name] not in seqset:
        new_alnseqs[name] = alnseqs[name]
        new_names.append(name)
        seqset.add(alnseqs[name])

print(len(new_alnseqs))

N = len(new_alnseqs)
L = len(new_alnseqs[new_names[0]])
print(N, L)
print(new_alnseqs[new_names[0]])
for name in new_names:
    if len(new_alnseqs[name]) != L:
        print(name, new_alnseqs[name], len(new_alnseqs[name]))
        exit(1)

print(N, L)

l = 0
while l < L:
    for name in new_names:
        if l == 0:
            n = name[:11]
        else:
            n = ""
        print("{0:11} {1}".format(n, " ".join([new_alnseqs[name][i:i+10] for i in range(l,l+60,10)])))
    print("")
    l += 60
