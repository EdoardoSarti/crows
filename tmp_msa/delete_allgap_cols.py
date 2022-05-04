import sys

aln_fn = sys.argv[1]
no_insertions = True if "--no-insertions" in sys.argv else False


seqd = {}
namel = []
with open(aln_fn) as f:
    for line in f:
        if not line.strip():
            continue
        if line.startswith(">"):
            name = line.strip()
            if name in namel:
                print("FATAL Repeated name: {0}".format(name))
                exit(1)
        else:
            seq = line.strip()
            if name not in seqd:
                seqd[name] = ''
                namel.append(name)
            seqd[name] += seq

if not namel:
    print("FATAL No sequences detected")
    exit(1)

L = len(seqd[namel[0]])
for name in namel:
    if L != len(seqd[name]):
        print("FATAL The length of this sequence is differente from the first one: {0}".format(name))
        exit(1)

charl = []
delcolset = set()
for i in range(L):
    charl = []
    for name in namel:
        charl.append(seqd[name][i])
    if set(charl) == {'-'} or set(charl) == {'.'}:
        print("WARNING Column {0} (starting from 1) contains only gaps and will be removed".format(i+1), file=sys.stderr)
        delcolset.add(i)
    if no_insertions and '.' in charl:
        print("WARNING Column {0} (starting from 1) contains insertions and will be removed".format(i+1), file=sys.stderr)
        delcolset.add(i)

for name in namel:
    print(name)
    corrseq = ''.join([x for i, x in enumerate(seqd[name]) if i not in delcolset])
    print(corrseq)


