# stemmers
Storing code for running large batches of stemmed topic models and their evaluations
on HTCondor with Mallet.

## Files
### Useful Python scripts

**finddiffs.py**: First writes out the resulting vocabulary size of every stemming
treatment, then prints out examples of short pieces of text that maximize how
different they are between stemmers. Helpful for generating tables for the figure.

**stopwords.py**: With a given corpus and train/test as inputs, aligns all files and
removes stopwords from them based on an unstemmed stoplist (at present, 'en.txt'
stolen from Mallet).

### Condor queue jobs

**import-datasets.[sh,condor]**: Converts existing datasets to Mallet .seq files,
using the training data as the vocabulary source for the test data.

**train.[sh,condor]**: Trains lots of topic models using Mallet. These arguments
allow adaptive hyperparameters with asymmetric alpha and writes out a whole bunch
of types of output for later use, including some diagnostics of topic coherence
(though it's based on the stemmed corpora, so it's not necessarily comparable).
