# stemmers
Storing code for running large batches of stemmed topic models and their
evaluations on HTCondor with Mallet.

## Files

### Stemmers

Stemmers/conflation treatments are included in the stemmers/ directory
for the following:

1. nostemmer (just tokenization),
2. krovetz (Krovetz stemmer),
3. lemmatizer (WordNet Lemmatizer with Stanford POS tagging),
4. lovins (Lovins stemmer),
5. paicehusk (Paice/Husk or Lancaster stemmer),
6. porter (Porter stemmer),
7. porter2 (Porter2/Snowball stemmer),
8. sstemmer (Harman's S-stemmer),
9. trunc4 (4-truncation), and
10. trunc5 (5-truncation).

These will output files with the path
    '[original file basename]-[stemmer].txt]'
with each line having the Mallet one-document-per-line three-column format.
To change this format or general behavior of all lemmatizers, modify
stemmers/abstractstemmer.py; to modify any of the actual stemmers, edit
stemmers/[stemmer].py.

### Useful scripts

**prepdirs.sh**: Creates all the useful output directories necessary for the
different types of output and evaluation these scripts produce.

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

**combine_states.py**: Takes a state file from the normal states and rewrites
it to have the unstemmed tokens again. This allows the production of more
comparable coherence measures with new PMI scores via Mallet (via Newman
and Mimno).

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

**redo_states.[sh,condor]**: Uses the combine_states script to create unstemmed
versions of all state files one by one. Unlike other setups, where one would
submit one condor job, redo_states.sh creates and submits a separate job for
each state file, recreating a condor file from redo_states.condor and extra
lines in special.condor. This hinders job tracking but makes choosing the file
for each job easier.

### Charts

**gather_ptlls.py**: Looks through the evaluator outputs and the single-topic
evaluator outputs to compute normalized per-token log likelihoods for every
state file, then aggregating them into bar charts split by corpus and topic
count.
