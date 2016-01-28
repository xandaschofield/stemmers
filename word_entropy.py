#!/home/aks249/anaconda/bin/python
from collections import defaultdict
import numpy as np
import os
import sys


STEMMERS = ['sstemmer', 'porter', 'porter2', 'lovins', 'paicehusk', 'trunc5', 'trunc4']
UNSTEMMED_NAME = 'nostemmer'

def sort_by_relative_entropy(corpus, topicct, stemmer):
    # get the right file names for the corpus and count
    stemmed_weights = ['wordweights/' + fname for fname in os.listdir('wordweights')
            if fname.startswith('{}-{}-{}'.format(corpus, stemmer, topicct))]
    unstemmed_weights = ['wordweights/' + fname for fname in os.listdir('wordweights')
            if fname.startswith('{}-{}-{}'.format(corpus, UNSTEMMED_NAME, topicct))]
    stemmed_corpus_file = 'corpora/{}-train-{}-stopped.txt'.format(corpus, stemmer)
    unstemmed_corpus_file = 'corpora/{}-train-{}-stopped.txt'.format(corpus, UNSTEMMED_NAME)

    # get the mapping from unstemmed to stemmed words
    stemmed_to_unstemmed = defaultdict(set)
    with open(stemmed_corpus_file) as f, open(unstemmed_corpus_file) as g:
        for stemmed_line in f:
            stemmed_words = stemmed_line.split()[3:]
            unstemmed_words = g.readline().split()[3:]
            assert(len(stemmed_words) == len(unstemmed_words))
            for uword, sword in zip(unstemmed_words, stemmed_words):
                stemmed_to_unstemmed[sword].add(uword)

    # for each file; for each word; get the entropy
    stemmed_entropies = defaultdict(list)
    unstemmed_entropies = defaultdict(list)
    for file in stemmed_weights:
        entropy_dict = get_entropy_per_word(file)
        for k, v in entropy_dict.iteritems():
            stemmed_entropies[k].append(v)
    for file in unstemmed_weights:
        entropy_dict = get_entropy_per_word(file)
        for k, v in entropy_dict.iteritems():
            unstemmed_entropies[k].append(v)

    # compute difference of average entropies
    stemmed_vocab = stemmed_to_unstemmed.keys()
    entropy_diffs = np.zeros(len(stemmed_vocab))
    for i, sword in enumerate(stemmed_vocab):
        entropy_diffs[i] = (np.mean(stemmed_entropies[sword]) - sum([
                np.mean(unstemmed_entropies[uword])
                for uword
                in stemmed_to_unstemmed[sword]
            ])
        )

    # find top 50 maximum and minimum entropies
    min_indices = np.argpartition(entropy_diffs, 50)[:50]
    max_indices = np.argpartition(entropy_diffs, -50)[-50:]
    with open('wordlists/{}-{}-{}.txt'.format(corpus, stemmer, topicct), 'w') as wf:
        wf.write('Lowest entropy differences (stemmer is better)\n')
        for i in min_indices:
            wf.write('{}\t{}\t{}\n'.format(entropy_diffs[i], stemmed_vocab[i], ' '.join(stemmed_to_unstemmed[stemmed_vocab[i]])))
        wf.write('Highest entropy differences (unstemmed is better)\n')
        for i in max_indices:
            wf.write('{}\t{}\t{}\n'.format(entropy_diffs[i], stemmed_vocab[i], ' '.join(stemmed_to_unstemmed[stemmed_vocab[i]])))


def get_entropy_per_word(file):
    entropy_dict = {}
    with open(file) as f:
        # each line corresponds to one word, with the format
        # wid word t1:ct1 t2:ct2...
        # for each topic ti and associated count ci that is greater than zero
        for line in f:
            frequency_chunks = line.split()
            word_type = frequency_chunks[1]
            # we actually don't care which topics we assigned to, just how many
            # outcomes there were
            topic_frequencies = [float(chunk.split(':')[1]) for chunk in frequency_chunks[2:]]
            total_count = sum(topic_frequencies)
            topic_probs = [tf/total_count for tf in topic_frequencies]
            # we're using Shannon entropy with a maximum likelihood estimate of probability
            entropy = sum([tp * np.log2(tp) for tp in topic_probs])
            entropy_dict[word_type] = entropy
    return entropy_dict

if __name__ == '__main__':
    sort_by_relative_entropy(sys.argv[1], sys.argv[2], STEMMERS[int(sys.argv[3]) % 7])
