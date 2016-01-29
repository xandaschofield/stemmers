#!/home/aks249/anaconda/bin/python
from collections import Counter
from collections import defaultdict
import numpy as np
import os
import sys


STEMMERS = ['krovetz', 'sstemmer', 'lemmatized', 'porter', 'porter2', 'lovins', 'paicehusk', 'trunc5', 'trunc4']
UNSTEMMED_NAME = 'nostemmer'

def sort_by_idf_probability(corpus, topicct, stemmer):
    # get the right file names for the corpus and count
    stemmed_probs = ['wordprobs/' + fname for fname in os.listdir('wordprobs')
            if fname.startswith('{}-{}-{}'.format(corpus, stemmer, topicct))]
    unstemmed_probs = ['wordprobs/' + fname for fname in os.listdir('wordprobs')
            if fname.startswith('{}-{}-{}'.format(corpus, UNSTEMMED_NAME, topicct))]
    unstemmed_corpus_file = 'corpora/{}-train-{}-stopped.txt'.format(corpus, UNSTEMMED_NAME)

    # put together
    # - doc_frequencies, a mapping from word type to number of documents with that word type
    # - full_token_list, a list of every token in the corpus
    # - num_docs, the count of the number of documents in the corpus
    doc_frequencies = Counter()
    full_token_list = []
    num_docs = 0.0
    with open(unstemmed_corpus_file) as f:
        for unstemmed_line in f:
            unstemmed_tokens = unstemmed_line.split()[3:]
            full_token_list += unstemmed_tokens
            for word in set(unstemmed_tokens):
                doc_frequencies[word] += 1
            num_docs += 1

    def idf_prob_per_word(file):
        wordprob_dict = defaultdict(float)
        with open(file) as f:
            # each line corresponds to one token, with the format
            # wordtype probability
            for i, line in enumerate(f):
                logprob = float(line.split()[1])
                word = full_token_list[i]
                wordprob_dict[word] += logprob * np.log(num_docs / doc_frequencies[word])
        return wordprob_dict

    # for each file; for each word; get the wordprobs
    stemmed_idfprobs = defaultdict(list)
    unstemmed_idfprobs = defaultdict(list)
    for file in stemmed_probs:
        wordprob_dict = idf_prob_per_word(file)
        for k, v in wordprob_dict.iteritems():
            stemmed_idfprobs[k].append(v)
    for file in unstemmed_probs:
        wordprob_dict = idf_prob_per_word(file)
        for k, v in wordprob_dict.iteritems():
            unstemmed_idfprobs[k].append(v)

    # compute difference of average entropies
    unstemmed_vocab = unstemmed_idfprobs.keys()
    idfprob_diffs = np.zeros(len(unstemmed_vocab))
    for i, sword in enumerate(unstemmed_vocab):
        idfprob_diffs[i] = np.mean(stemmed_idfprobs[sword]) - np.mean(unstemmed_idfprobs[sword])

    # find top 50 maximum and minimum entropies
    min_indices = np.argpartition(idfprob_diffs, 50)[:50]
    max_indices = np.argpartition(idfprob_diffs, -50)[-50:]
    with open('wordlistsidf/{}-{}-{}.txt'.format(corpus, stemmer, topicct), 'w') as wf:
        wf.write('Lowest prob-idf differences (unstemmed is better)\n')
        for i in min_indices:
            wf.write('{}\t{}\n'.format(idfprob_diffs[i], unstemmed_vocab[i]))
        wf.write('Highest prob-idf differences (stemmer is better)\n')
        for i in max_indices:
            wf.write('{}\t{}\n'.format(idfprob_diffs[i], unstemmed_vocab[i]))


if __name__ == '__main__':
    sort_by_idf_probability(sys.argv[1], sys.argv[2], STEMMERS[int(sys.argv[3]) % 10])
