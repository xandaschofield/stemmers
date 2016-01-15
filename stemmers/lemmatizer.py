from abstractstemmer import AbstractStemmer
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tag import StanfordPOSTagger
import sys

class Lemmatizer(AbstractStemmer):

    def __init__(self, ):
        super(Lemmatizer, self).__init__()
        self.basename = 'lemmatized'
        self.pos_tagger = StanfordPOSTagger('english-left3words-distsim.tagger', java_options='-mx1024m')
        self.lemmatizer = WordNetLemmatizer()
        self.max_length = 500

    def process(self, words):
        current_sentence = []
        pos_words = []
        for word in words:
            current_sentence.append(word)
            if word in '.!?' and len(current_sentence) > self.max_length:
                try:
                    pos_words += self.pos_tagger.tag(current_sentence)
                except Exception:
                    print 'Broke on', current_sentence
                    raise
                current_sentence = []
        for i in range(len(current_sentence) / self.max_length):
            try:
                pos_words += self.pos_tagger.tag(current_sentence[:self.max_length])
            except Exception:
                print 'Broke on', current_sentence[:self.max_length]
                raise
            current_sentence = current_sentence[self.max_length:]
        try:
            pos_words += self.pos_tagger.tag(current_sentence)
        except Exception:
            print 'Broke on', current_sentence
            raise
        processed_words = [self.lemmatizer.lemmatize(wd, pos=self.get_wn_pos(ps)) for wd, ps in pos_words]
        return processed_words

    # from http://stackoverflow.com/questions/15586721
    def get_wn_pos(self, treebank_tag):
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN


if __name__ == '__main__':
    stemmer = Lemmatizer()
    stemmer.stem(sys.argv[1:])
