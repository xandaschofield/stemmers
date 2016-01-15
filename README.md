# stemmers
Storing code for running large batches of stemmed topic models and their
evaluations on HTCondor with Mallet.

## Files ### Useful scripts

**finddiffs.py**: First writes out the resulting vocabulary size of every
stemming treatment, then prints out examples of short pieces of text that
maximize how different they are between stemmers. Helpful for generating tables
for the figure.

**stopwords.py**: With a given corpus and train/test as inputs, aligns all files
and removes stopwords from them based on an unstemmed stoplist (at present,
'en.txt' stolen from Mallet).

**VariationOfInformation.java**: Written by David Mimno. Compares two state
files and uses assignments of words to topics to compute variation of
information (VOI), a distance metric between clusterings (Meila, 2003).

### Condor queue jobs

**import-datasets.[sh,condor]**: Converts existing datasets to Mallet .seq
files, using the training data as the vocabulary source for the test data.

**train.[sh,condor]**: Trains lots of topic models using Mallet. These arguments
allow adaptive hyperparameters with asymmetric alpha and writes out a whole
bunch of types of output for later use, including some diagnostics of topic
coherence (though it's based on the stemmed corpora, so it's not necessarily
comparable).

**pull_out_betas.[py,condor]**: Finds the probability on the test set of a
single-topic training set, useful for normalizing across different corpora when
looking at held-out likelihood.

**runevals.[sh,condor]**: Computes the held-out likelihood of each topic model
on a test set with Mallet using left-to-right estimation (Wallach, 2009). This
includes total likelihoods as well as per-document and per-token likelihoods.

**VOI.[sh,condor]**: Uses the VariationOfInformation script to compute pairwise
variations of information across all stemmers for each choice of topic count and
corpus.
