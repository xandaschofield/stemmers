import sys
from itertools import combinations

corp = sys.argv[1]
ty = sys.argv[2]


stoplist = set([line.strip() for line in open('en.txt')])

stemmers = ['nostemmer', 'trunc4', 'trunc5', 'lovins', 'porter', 'porter2', 'paicehusk', 'sstemmer', 'krovetz', 'lemmatized']
readfiles = [open('{}-{}-{}.txt'.format(corp, ty, stemmer)) for stemmer in stemmers]
writefiles = [open('{}-{}-{}-stopped.txt'.format(corp, ty, stemmer), mode='w') for stemmer in stemmers]
specialfile = open('speciallines.txt', 'w')
with open('{}-{}-nostemmer.txt'.format(corp, ty)) as readref:
    with open('{}-{}-nostemmer.txt'.format(corp, ty)) as writeref:
        for line in readref:
            readlines = [f.readline() for f in readfiles]
            if not any(readlines):
                continue
            try:
                readchunks = [l.split('\t', 2) for l in readlines]
                wordlists = [c[2].split() for c in readchunks]
                for i in range(len(stemmers)):
                    while len(wordlists[i]) == 0:
                        readlines[i] = readfiles[i].readline()
                        readchunks[i] = readlines[i].split('\t', 2)
                        wordlists[i] = readchunks[i][2].split()
            except Exception:
                import ipdb; ipdb.set_trace()
                raise

            # check that all documents are the same length
            for wl in wordlists[1:]:
                if len(wordlists[0]) != len(wl):
                    raise Exception('Misaligned sentences:\n{}\n{}'.format(wordlists[0], wl))

            # Figure out which words to delete from each and delete 'em
            stopwordmask = [len(wd) > 2 and wd not in stoplist for wd in wordlists[0]]
            writelists = [[wd for wd, mask in zip(wl, stopwordmask) if mask] for wl in wordlists]

            # Check if it's interesting enough to report out
            different = True
            for wl1, wl2 in combinations(writelists, 2):
                if wl1 == wl2:
                    different = False

            # Reformat into lines of text and write out
            writelines = ['{}\t{}\t{}\n'.format(rc[0], rc[1], ' '.join(wl)) for rc, wl in zip(readchunks, writelists)]
            for wf, wn in zip(writefiles, writelines):
                wf.write(wn)
                if different:
                    specialfile.write(wn)

for file in readfiles:
    file.close()
for file in writefiles:
    file.close()
specialfile.close()
