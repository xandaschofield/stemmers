#!/bin/python
from abstractstemmer import AbstractStemmer
import subprocess
import sys


class KrovetzStemmer(AbstractStemmer):

    def __init__(self, ):
        super(KrovetzStemmer, self).__init__()
        self.basename = 'krovetz'

    def process(self, words):
        new_words = []
        while len(words) > 1000:
            new_words += subprocess.check_output(
                    ['java', '-jar', 'kstem-3.4.jar', '-w', ' '.join(words[:1000])]
            ).split()
            words = words[1000:]
        new_words += subprocess.check_output(
                'java -jar kstem-3.4.jar -w ' + ' '.join(words),
                shell=True,
        ).split()
        return new_words


if __name__ == '__main__':
    stemmer = KrovetzStemmer()
    stemmer.stem(sys.argv[1:])
