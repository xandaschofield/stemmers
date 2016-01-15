from collections import defaultdict
import matplotlib
matplotlib.use('Agg')
from matplotlib import cm
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy
import os


count = {
   'arxiv': 43592980 - (2 * 5710),
   'nyt':   6352224 - (2 * 9788),
   'imdb':  5963149 - (2 * 28215),
   'yelp':  37323903 - (2 * 281349),
}

stemtokey = {
    'trunc4': 'T4',
    'trunc5': 'T5',
    'paicehusk': 'PH',
    'lovins': 'LO',
    'porter': 'P1',
    'porter2': 'P2',
    'sstemmer': 'SS',
    'lemmatized': 'WL',
    'krovetz': 'KR',
    'nostemmer': 'US',
}

cname = {
   'arxiv': 'ArXiv',
   'nyt':   'NYT',
   'imdb':  'IMDb',
   'yelp':  'Yelp',
}

stemmers = ['nostemmer', 'trunc4', 'trunc5', 'lovins', 'porter', 'porter2', 'paicehusk', 'sstemmer', 'krovetz'] # lemmatized
corpuses = ['arxiv', 'nyt', 'imdb', 'yelp']
topiccts = ('10', '50', '200')
patterns = ('/', '-', '++', 'x', '\\', '*', 'o', 'O', '.', '||')

# Step 1: get log likelihoods
lls = defaultdict(list)
for root, subdirs, files in os.walk('outprobs/'):
    for fname in files:
        if fname.endswith('.outprob'):
            regfile = os.path.join(root, fname)
            singletopicfile = regfile.replace('outprobs', 'oneoutprobs').replace('.outprob', '-ones.outprob')
            if not os.path.exists(singletopicfile):
                print singletopicfile, 'absent'
                continue
            f = open(regfile, 'r')
            lltext = f.readline()
            if not lltext:
                print singletopicfile, 'empty'
                continue
            ll = float(lltext)
            f.close()
            corpus, stemmer, topicct, idetc = fname.split('-')
            ptll = ll / count[corpus]
            try:
                g = open(singletopicfile, 'r')
            except Exception:
                continue
            line = g.readline()
            single_ptll = float(line) / count[corpus]
            g.close()
            lls[(corpus, stemmer, topicct)] += [ptll - single_ptll]

# Step 2: compute normalized per token log likelihoods
means = {}
stdevs = {}
for corpus, stemmer, topicct in lls.iterkeys():
    normed_ptlls = lls[(corpus, stemmer, topicct)]
    means[(corpus, stemmer, topicct)] = numpy.mean(normed_ptlls)
    stdevs[(corpus, stemmer, topicct)] = numpy.std(normed_ptlls, ddof=1)

# Step 3: plot things
matplotlib.rcParams['figure.figsize'] = 9, 14
matplotlib.rcParams['figure.subplot.bottom'] = 0.1
ind = numpy.arange(3)
width = 0.9 / len(stemmers)

plt.figure(1)
for subp, corpus in enumerate(corpuses):
    stemlabels = [stemtokey[stem] for stem in stemmers]
    plt.subplot(410 + subp + 1)
    rects = {}
    ymax = 0
    for i, stemmer in enumerate(stemmers):
        stemmeans = [means[(corpus, stemmer, topicct)] for topicct in topiccts]
        stemstds = [1.96 * stdevs[(corpus, stemmer, topicct)] for topicct in topiccts]
        ymax = max(ymax, max(stemmeans))
        rects[stemmer] = plt.bar(ind + (i * width) + 0.05, stemmeans, width, yerr=stemstds, label=stemlabels, color='white', ecolor='black', hatch=patterns[i])
    plt.ylabel('Normalized LL')
    plt.ylim(ymin=0.0, ymax=ymax + 0.15)
    plt.title('Normalized LL for {0}'.format(cname[corpus]))
    xtx = [0.05 + width/2 + (width * j) + i for i in xrange(len(topiccts)) for j in xrange(len(stemmers))]
    plt.xticks(xtx, stemlabels * 3)
    plt.grid(b=True, which='major', color='.5', linestyle='--') 
    # Label the raw counts and the percentages below the x-axis...
    bin_centers = ind + 0.5
    for count, x in zip(topiccts, bin_centers):
        # Label the raw counts
        plt.text(x, ymax + 0.1, count + ' topics', va='top', ha='center', fontsize=14)


plt.savefig('llplots.png', bbox_inches='tight')
