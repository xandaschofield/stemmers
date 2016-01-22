#!/home/aks249/anaconda/bin/python
import gzip
import sys

reffilenames = {
        'arxiv': 'arxiv-nostemmer-10-61040123.gz',
        'imdb': 'imdb-nostemmer-10-61040303.gz',
        'nyt': 'nyt-nostemmer-10-61115603.gz',
        'yelp': 'yelp-nostemmer-10-61324123.gz',
}

fname = sys.argv[1]
gname = fname.replace('states', 'modstates')
for c in reffilenames.keys():
    if c in gname:
        corp = c
refname = reffilenames[corp]

r = gzip.open('states/' + refname)
f = gzip.open(fname)
g = gzip.open(gname, 'w')

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
