#coding:utf-8
import sys
import simplejson as json
import re
import jieba
from gensim import models
from modelFiles import modelFilesList
from title_rhythm import TitleRhythmDict
import time
reload(sys)
sys.setdefaultencoding('utf8')

class Learn:
    def __init__(self, sourceFile, rhythmFile):
        self.sourceFile = sourceFile
        self.rhythmFile = rhythmFile

        self._title_pingze_dict = {}
        self._title_delimiter_dict = {}
        self._pingze_rhythm_dict = {}
        self._reverse_rhythm_word_dict = {}
        self._reverse_pingze_word_dict = {}
        self._rhythm_word_dict = {}
        self._pingze_words_dict = {}
        self._word_count_dict = {}
        self._rhythm_count_dict = {}
        self._bigram_count_dict = {}
        self._bigram_word_to_start_dict = {}
        self._bigram_word_to_end_dict = {}

        self._split_sentences = []
        self._word_model = None

        self._sentences = []

    def title_pingze_dict(self):
        for title, content_rhythm in TitleRhythmDict.iteritems():
            sentences = re.findall(r"[0-9]+", content_rhythm)
            new_sentences = []
            for sentence in sentences:
                new_sentence = ""
                for word in sentence:
                    if not int(word):
                        new_sentence += "0"
                    elif not (int(word) % 2):
                        new_sentence += "2"
                    else:
                        new_sentence += "1"
                new_sentences.append(new_sentence)
            self._title_pingze_dict[title.decode()] = new_sentences
            delimiters = []
            for word in content_rhythm:
                if word in [",", ".", "`", "|"]:
                    delimiters.append(word)
            self._title_delimiter_dict[title.decode()] = delimiters

    def build_pingze_rhythm_words_dict(self):
        with open(self.rhythmFile, 'r') as fp_r:
            count = 1
            while 1:
                line = fp_r.readline()
                line = line.strip().decode("utf-8")
                if not line:
                    continue
                if line == "END":
                    break
                if u"：" in line: # Chinese title part
                    #print line
                    #print len(line)
                    next_line = fp_r.readline().strip().decode("utf-8")

                    rhythm_word = line[-2]

                    is_ping = True
                    if u"平" in line: # ping related
                        self._pingze_rhythm_dict.setdefault('1', []).append(rhythm_word)
                        is_ping = True
                    else: # ze related
                        self._pingze_rhythm_dict.setdefault('2', []).append(rhythm_word)
                        is_ping = False

                    # build reverse dict for count later
                    invalid_flag = False
                    invalid_value = []
                    words = []
                    for word in next_line:
                        if word == u"[":
                            invalid_flag = True
                        if invalid_flag:
                            invalid_value.append(word)
                            if word == u"]":
                                invalid_flag = False
                            continue
                        self._reverse_rhythm_word_dict[word] = rhythm_word
                        if is_ping: # ping related
                            self._reverse_pingze_word_dict[word] = '1'
                        else: # ze related
                            self._reverse_pingze_word_dict[word] = '2'
                        words.append(word)

                    self._rhythm_word_dict[rhythm_word] = words

                    if u"平" in line: # ping related
                        self._pingze_words_dict.setdefault('1', []).extend(words)
                    else: # ze related
                        self._pingze_words_dict.setdefault('2', []).extend(words)

    def count_general_rhythm_words(self):
        with open(self.sourceFile, 'r') as fp_r:
            count = 1
            while 1:
                line = fp_r.readline()
                line = line.strip().decode("utf-8")
                if not line:
                    continue
                if line == "END":
                    break
                if (u"，" not in line) and (u"。" not in line): # only use content part for stats
                    continue

                sentences = re.split(u"[，。]", line)
                for sentence in sentences:
                    if sentence:
                        self._sentences.append(sentence)

                        final_word = sentence[-1]
                        #print 'final', final_word
                        if final_word not in self._reverse_rhythm_word_dict:
                            #print 'not exist', final_word
                            continue
                        rhythm_word = self._reverse_rhythm_word_dict[final_word]
                        #print 'rhythm', rhythm_word
                        if final_word not in self._word_count_dict:
                            self._word_count_dict[final_word] = 1
                        else:
                            self._word_count_dict[final_word] += 1
                        if rhythm_word not in self._rhythm_count_dict:
                            self._rhythm_count_dict[rhythm_word] = 1
                        else:
                            self._rhythm_count_dict[rhythm_word] += 1

                        # build 2-gram
                        for idx, word in enumerate(sentence):
                            if idx >= len(sentence) - 1:
                                break
                            first_word = word
                            second_word = sentence[idx+1]
                            if (first_word == u'、') or (second_word == u'、'):
                                continue
                            bigram_key = '__'.join([first_word, second_word])
                            if bigram_key not in self._bigram_count_dict:
                                self._bigram_count_dict[bigram_key] = 1
                            else:
                                self._bigram_count_dict[bigram_key] += 1
                            self._bigram_word_to_start_dict.setdefault(first_word, []).append(bigram_key)
                            self._bigram_word_to_end_dict.setdefault(second_word, []).append(bigram_key)

    def split_words(self):
        """ split words with jieba"""
        with open(self.sourceFile, 'r') as fp_r:
            count = 1
            while 1:
                line = fp_r.readline()
                line = line.strip().decode("utf-8")
                if not line:
                    continue
                if line == "END":
                    break
                if (u"，" not in line) and (u"。" not in line): # only use content part for stats
                    continue

                #print line
                words = jieba.cut(line)
                words = list(words)
                #print '/ '.join(words)
                self._split_sentences.append(words)
                count += 1

    def build_word2vec(self):
        """ build word2vec for words"""
        self._word_model = models.Word2Vec(self._split_sentences, min_count=5)
        self._word_model.save("./model/word_model")

    def saveModel(self):
        for dataFile in modelFilesList:
            fileName = "./model/" + dataFile
            with open(fileName, "w") as f:
                value = getattr(self, "_" + dataFile)
                json.dump(value, f)
                print "finish writing model " + dataFile

    def buildModel(self):
        """ generate title, pingze, rhythm, word relationship"""
     
        self.title_pingze_dict()
        print "finish title_pingze"


        self.build_pingze_rhythm_words_dict()
        print "finish build_pingze_rhythm_words_dict"


        self.count_general_rhythm_words()
        print "finish count_general_rhythm_words"


        self.split_words()
        print "finish split_words"


        self.build_word2vec()
        print "finish build_word2vec"

        self.saveModel()

if __name__ == '__main__':
    # sourceFile = sys.argv[1];
    # rhythmFile = sys.argv[2];
    sourceFile = "./data/qsc.txt"
    rhythmFile = "./data/psy.txt"
    begin = time.time()
    learn = Learn(sourceFile, rhythmFile)
    learn.buildModel()
    end = time.time()
    print "finish building model, using " + str(end - begin) + "seconds"
