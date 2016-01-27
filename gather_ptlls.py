from collections import defaultdict
import matplotlib
matplotlib.use('Agg')
from matplotlib import cm
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy
import os


count = {
   'arxiv': 19463144,
   'imdb':  3052551,
   'nyt':   2978288,
   'yelp':  14358387,
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

stemmers = ['nostemmer', 'krovetz', 'sstemmer', 'lemmatized', 'porter', 'porter2', 'lovins', 'paicehusk', 'trunc5', 'trunc4']
corpora = ['arxiv', 'imdb', 'nyt', 'yelp']
topiccts = ('10', '50', '200')
colors = ('0.7', '0.4', '0.1', '0.8', '0.5', '0.2', '0.9', '0.6', '0.3', '1.0')

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
                print regfile, 'empty'
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
stderrs = {}
for corpus, stemmer, topicct in lls.iterkeys():
    normed_ptlls = lls[(corpus, stemmer, topicct)]
    means[(corpus, stemmer, topicct)] = numpy.mean(normed_ptlls)
    stderrs[(corpus, stemmer, topicct)] = numpy.std(normed_ptlls, ddof=1)

# Step 3: plot things
matplotlib.rcParams['figure.figsize'] = 9, 14
matplotlib.rcParams['figure.subplot.bottom'] = 0.1
ind = numpy.arange(3)
width = 0.9 / len(stemmers)

plt.figure(1)
for subp, corpus in enumerate(corpora):
    stemlabels = [stemtokey[stem] for stem in stemmers]
    ax = plt.subplot(410 + subp + 1)
    rects = {}
    ymax = 0
    for i, stemmer in enumerate(stemmers):
        stemmeans = [means[(corpus, stemmer, topicct)] for topicct in topiccts]
        stemstds = [2.58 * stderrs[(corpus, stemmer, topicct)] for topicct in topiccts]
        ymax = max(ymax, max(stemmeans))
        rects[stemmer] = plt.bar(ind + (i * width) + 0.05, stemmeans, width, yerr=stemstds, label=stemlabels, color=colors[i], ecolor='black')
    # plt.ylabel('Negative Topic Coherence')
    plt.ylim(ymin=0.0, ymax=1.2*ymax)
    plt.title('{0}'.format(cname[corpus]))
    xtx = [0.05 + width/2 + (width * j) + i for i in xrange(len(topiccts)) for j in xrange(len(stemmers))]
    plt.xticks(xtx, stemlabels * 3)
    ax.yaxis.grid(True, which='major')
    ax.xaxis.grid(False)
    # Label the raw counts and the percentages below the x-axis...
    bin_centers = ind + 0.5
    for count, x in zip(topiccts, bin_centers):
        # Label the raw counts
        plt.text(x, 1.1*ymax, count + ' topics', va='top', ha='center', fontsize=14)

plt.savefig('llplots.png', bbox_inches='tight')
