#!/home/aks249/anaconda/bin/python
import os
import sys

stemmers = ('trunc4', 'trunc5', 'paicehusk', 'lovins', 'porter2', 'porter', 'sstemmer', 'lemmatized', 'nostemmer', 'krovetz')

for root, dirs, files in os.walk("outs/"):
    for fname in files:
        if stemmers[int(sys.argv[1])] in fname and fname.endswith('out.txt'):
            regfile = os.path.join(root, fname)
            singletopicfile = regfile.replace('outs', 'oneoutprobs').replace('out.txt', 'ones.outprob')
            if os.path.exists(singletopicfile):
                continue
            f = open(regfile)
            for line in f:
                if line.startswith('[beta:'):
                    beta = float(line.split()[-1][:-1])
            corpus, stemmer, topic, number, _ = fname.split('-')
            print corpus, stemmer, topic, number
            os.system("~/Mallet/bin/mallet train-topics --input ~/stemstopped/corpora/{1}-train-{0}.seq --num-topics 1 --evaluator-filename ~/stemstopped/oneevaluators/{1}-{0}-{4}-{2}.ones.evaluator --num-iterations 1 --beta {3} &> ~/stemstopped/ones/{1}-{0}-{4}-{2}-ones.txt".format(stemmer, corpus, number, beta, topic))
            os.system("~/Mallet/bin/mallet evaluate-topics --input ~/stemstopped/corpora/{1}-test-{0}.seq --evaluator ~/stemstopped/oneevaluators/{1}-{0}-{3}-{2}.ones.evaluator --output-prob ~/stemstopped/oneoutprobs/{1}-{0}-{3}-{2}-ones.outprob".format(stemmer, corpus, number, topic))
