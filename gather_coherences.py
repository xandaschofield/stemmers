from bs4 import BeautifulSoup
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')
from matplotlib import cm
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
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
    'nostemmer': 'NS',
}

cname = {
   'arxiv': 'ArXiv',
   'nyt':   'NYT',
   'imdb':  'IMDb',
   'yelp':  'Yelp',
}

stemmers = ['nostemmer', 'trunc4', 'trunc5', 'lovins', 'porter', 'porter2', 'paicehusk', 'sstemmer', 'krovetz', 'lemmatized']
corpora = ['arxiv', 'imdb', 'nyt', 'yelp']
topiccts = ('10', '50', '200')
colors = ('0.7', '0.4', '0.1', '0.8', '0.5', '0.2', '0.9', '0.6', '0.3', '1.0')

# Step 1: get coherences and average for each topic model
chs = defaultdict(list)
maxchs = defaultdict(list)
for root, subdirs, files in os.walk('coherences/'):
    for fname in files:
        if fname.endswith('.xml'):
            corpus, stemmer, topicct, idetc = fname.split('-')
            with open(os.path.join(root, fname), 'r') as f:
                coherence_text = f.read()
            bs = BeautifulSoup(coherence_text)
            coherences = [float(t.get('coherence')) for t in bs.find_all('topic')]
            chs[(corpus, stemmer, topicct)] += coherences
            maxchs[(corpus, stemmer, topicct)] += [np.average(coherences)]

# Step 2: compute average coherences per treatment
means = {}
stderrs = {}
for corpus, stemmer, topicct in chs.iterkeys():
    current_chs = maxchs[(corpus, stemmer, topicct)]
    means[(corpus, stemmer, topicct)] = np.mean(current_chs)
    stderrs[(corpus, stemmer, topicct)] = np.std(current_chs, ddof=1)

# Step 3: plot things
matplotlib.rcParams['figure.figsize'] = 9, 14
matplotlib.rcParams['figure.subplot.bottom'] = 0.1
ind = np.arange(3)
width = 0.9 / len(stemmers)

plt.figure(1)
for subp, corpus in enumerate(corpora):
    stemlabels = [stemtokey[stem] for stem in stemmers]
    ax = plt.subplot(410 + subp + 1)
    rects = {}
    ymax = 0
    for i, stemmer in enumerate(stemmers):
        stemmeans = [-means[(corpus, stemmer, topicct)] for topicct in topiccts]
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


plt.savefig('diagnostics.png', bbox_inches='tight')
