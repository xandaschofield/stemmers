from collections import defaultdict
from itertools import izip
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
import os


matplotlib.rcParams['figure.figsize'] = 12, 16
fig = plt.figure()

stemtokey = {
    'trunc4': 'T4',
    'trunc5': 'T5',
    'paicehusk': 'PH',
    'lovins': 'LO',
    'porter': 'P1',
    'porter2': 'P2',
    'sstemmer': 'SS',
    'lemmatized': 'WL',
    'nostemmer': 'NS',
    'krovetz': 'KR',
}

cname = {
   'nyt': 'NYT',
   'imdb': 'IMDb',
   'arxiv': 'ArXiv',
   'yelp': 'Yelp',
}

ymin = {
    '10': 2.3,
    '50': 4.3,
    '200': 5.6,
}
ymax = {
    '10': 3.6,
    '50': 5.8,
    '200': 7.6,
}

nstemmers = 10
validfiles = set(['states/' + file for file in os.listdir('states')])


def show_values(pc, fmt="%.2f", **kw):
    """Taken from HYRY's anwer at
    http://stackoverflow.com/questions/25071968/heatmap-with-text-in-each-cell-with-matplotlibs-pyplot
    """
    pc.update_scalarmappable()
    ax = pc.get_axes()
    for p, color, value in izip(pc.get_paths(), pc.get_facecolors(), pc.get_array()):
        x, y = p.vertices[:-2, :].mean(0)
        if np.all(color[:3] > 0.5):
            color = (0.0, 0.0, 0.0)
        else:
            color = (1.0, 1.0, 1.0)
        ax.text(x, y, fmt % value, ha="center", va="center", color=color, fontsize=9, **kw)

for plotx, corp in enumerate(('arxiv', 'imdb', 'nyt', 'yelp')):
    vois = {}
    voierrs = {}
    voislists = {}
    for i in ('10', '50', '200'):
        voislists[i] = defaultdict(list)
        vois[i] = np.zeros((nstemmers, nstemmers))
        voierrs[i] = np.zeros((nstemmers, nstemmers))

        stemmers = set()

        voifile = open('vois/{0}-{1}.voi'.format(corp, i), 'r')
        currentline = ''
        seen = set()
        # Not the most elegant output - sometimes the output got multilined.
        for line in voifile:
            if line != '':
                splitline = line.split()
                try:
                    leftfile, rightfile, voi = splitline
                except:
                    continue
                if (leftfile, rightfile) in seen or (rightfile, leftfile) in seen:
                    continue
                if leftfile not in validfiles:
                    print "Missing file:", leftfile
                    continue
                if rightfile not in validfiles:
                    print "Missing file:", rightfile
                    continue
                try:
                    _, stemmer1, topics, id1 = leftfile.split('/')[-1].split('-', 3)
                except:
                    continue
                _, stemmer2, topics, id2 = rightfile.split('/')[-1].split('-', 3)
                if stemmer1 != stemmer2 or id1 != id2:
                    voislists[topics][(stemmer1, stemmer2)] += [float(voi)]
                    voislists[topics][(stemmer2, stemmer1)] += [float(voi)]
                stemmers.add(stemmer1)
                stemmers.add(stemmer2)
                currentline = line
                seen.add((leftfile, rightfile))
        voifile.close()

        # Processing the leftover line
        splitline = currentline.split()
        leftfile, rightfile, voi = splitline
        _, stemmer1, topics, id1 = leftfile.split('/')[-1].split('-', 3)
        _, stemmer2, _, id2 = rightfile.split('/')[-1].split('-', 3)
        if stemmer1 != stemmer2 or id1 != id2:
            voislists[topics][(stemmer1, stemmer2)] += [min(float(voi), 0.0)]


    for ploty, topics in enumerate(('10', '50', '200')):
        ax = fig.add_subplot(4, 3, plotx * 3 + ploty + 1)
        sortedstemmers = sorted(stemmers, key=lambda x : 0 if x=='nostemmer' else (sum(voislists[topics][('nostemmer', x)]))/len(voislists[topics][('nostemmer', x)]))
        stemmerlabels = [stemtokey[stem] for stem in sortedstemmers]
        for i in range(len(sortedstemmers)):
            stemmer1 = sortedstemmers[i]
            voisum = sum(voislists[topics][(stemmer1, stemmer1)])
            voict = len(voislists[topics][(stemmer1, stemmer1)])
            voival = voisum / voict
            stdev = np.std(voislists[topics][(stemmer1, stemmer1)], ddof=1)
            voierrs[topics][i][i] = stdev
            vois[topics][i][i] = voival

            for j in range(i + 1, len(sortedstemmers)):
                stemmer2 = sortedstemmers[j]
                current_voilist = voislists[topics][(stemmer1, stemmer2)] + voislists[topics][(stemmer2, stemmer1)]
                voisum = sum(current_voilist)
                voict = len(current_voilist)
                voival = voisum / voict

                stdev = np.std(current_voilist, ddof=1)
                voierrs[topics][i][j] = stdev
                voierrs[topics][j][i] = stdev
                vois[topics][i][j] = voival
                vois[topics][j][i] = voival

        sigval = np.max(np.diagonal(voierrs[topics]))*2.58

        ax.set_title('{0}, {1} topics\np=0.05 significance at {2:.1}'.format(cname[corp], topics, sigval))
        heatmap = ax.pcolor(vois[topics], cmap='gray') # vmin=ymin[topics], vmax=ymax[topics])
        ax.set_aspect('equal')
        ax.set_xticks(np.arange(0, nstemmers) + 0.5)
        ax.set_xticklabels(stemmerlabels)
        ax.set_yticks(np.arange(0, nstemmers) + 0.5)
        ax.set_yticklabels(stemmerlabels)
        show_values(heatmap)
plt.tight_layout()
plt.savefig('vois_all.png'.format(corp, topics), )
