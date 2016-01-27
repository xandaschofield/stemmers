import sys
from itertools import combinations

corp = sys.argv[1]
ty = sys.argv[2]

stemmers = ['nostemmer', 'krovetz', 'sstemmer', 'lemmatized', 'porter', 'porter2', 'lovins', 'paicehusk', 'trunc5', 'trunc4']
readfiles = [open('corpora/{}-{}-{}-stopped.txt'.format(corp, ty, stemmer)) for stemmer in stemmers]
specialfile = open('corpora/{}-tables.txt'.format(corp), 'w')
vocabs = [set() for stemmer in stemmers]
different_lines = []
max_different = 0
with open('corpora/{}-{}-nostemmer-stopped.txt'.format(corp, ty)) as readref:
    for line in readref:
        readlines = [f.readline() for f in readfiles]
        if not any(readlines):
            continue
        readchunks = [l.split('\t', 2) for l in readlines]
        wordlists = [c[2].split() for c in readchunks]
        for wl, v in zip(wordlists, vocabs):
            v.update(wl)

        if len(wordlists[0]) > 15:
            continue
        # Check if it's interesting enough to report out
        different = len(set([' '.join(wl) for wl in wordlists]))
        if different > max_different:
            max_different = different
            different_lines = [wordlists]
        elif different == max_different:
            different_lines.append(wordlists)

# Reformat into lines of text and write out
for st, v in zip(stemmers, vocabs):
    specialfile.write('{}: {}\n'.format(st, len(v)))
for i, wls in enumerate(different_lines):
    specialfile.write('Example {}\n'.format(i))
    for st, wl in zip(stemmers, wls):
        specialfile.write('{} & {} \\\\ \n'.format(st, ' & '.join(wl)))

for file in readfiles:
    file.close()
specialfile.close()
