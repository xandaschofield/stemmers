#!/home/aks249/anaconda/bin/python
import gzip
import sys

reffilenames = {
        'arxiv': 'arxiv-nostemmer-10-58334123.gz',
        'imdb': 'imdb-nostemmer-10-58334303.gz',
        'nyt': 'nyt-nostemmer-10-58334603.gz',
        'yelp': 'yelp-nostemmer-10-583341023.gz',
}

fname = sys.argv[1]
gname = fname.replace('states', 'modstates')
for c in reffilenames.keys():
    if c in gname:
        corp = c
refname = reffilenames[corp]

f = gzip.open(fname)
g = gzip.open(gname, 'w')
r = gzip.open('states/' + refname)

for line in f:
    linechunks = line.split()
    refline = r.readline().split()
    if line.startswith('#'):
        g.write(line)
        continue
    refline[5] = linechunks[5]
    g.write(' '.join(refline) + '\n')

f.close()
g.close()
r.close()
