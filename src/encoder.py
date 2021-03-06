'''
This class encodes text fed into it to be later used in the scoring algorithm.

It picks random words inside the text and replaces with ${word} this will indicate to the scorer to score this word.

TODO figure out best way to handle text 
'''
import random


class Encoder():

    def __init__(self, seed, probability):
        self.rand = random
        
        self.rand.seed(seed)
        
        self._totalWords = 0
        self._encodedWords = 0
        # probability is a random percent based off of maxEncode * random (random is a number between 0 and 1)
        # self.probability = self.rand.random() * (probability/ 100)
        # print("{0}%".format(round(self.probability*100, 2)))
        self.probability = probability / 100

    def encode(self, text, feed_length = 20):
        ''' Encoded inputted text '''
        encodedText = ""
        feedLst = []
        feed = ""
        useNext = False
        
        text = text.split()
        self._totalWords = len(text)
        count = 0
        for word in text:
            count += 1
            if useNext or self.rand.random() <= self.probability:
                # skip any non letter characters
                if not ('a' <= word.lower() <= 'z'):
                    useNext = True
                    continue

                # gives feed and word to guess
                feedLst.append([feed, word])
                
                # tags the word for GPT to guess later
                word = "${"+self._clean(word)+"}"

                self._encodedWords += 1
                useNext = False
            elif count < feed_length:
                feed = " ".join(text[0:count])
            else:
                feed = " ".join(text[count - feed_length:count])
            
            encodedText += "{} ".format(word)

        return feedLst

    def decode(self):
        pass
    
    def getProbablity(self):
        '''returns probability'''
        return self.probability

    def wordsEncoded(self):
        '''returns tuple of (encodedWords, totalWords)'''
        return (self._totalWords, self._encodedWords)

    def _clean(self, word):
        out = ""
        for c in word:
            if 'a' <= c.lower() <= 'z':
                out += c
        return out
