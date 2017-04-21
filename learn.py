# coding:utf-8
import re
import sys
import time
import operator
from gensim import models
import simplejson as json
from modelFiles import modelFilesList

reload(sys)
sys.setdefaultencoding('utf8')

title2rhythm = {
    u"蝶恋花": "0201122,0211`02112.0201122,0102112.|0201122,0211`02112.0201122,0102112.",
    u"浣溪沙": "0201021,0102211.0102211.|0201122,0102211.0102211.",
    u"菩萨蛮": "0102112,0102112.02211,01021.|01122,02012.02211,01021.",
    u"南乡子": "02211,0211221.0201122,11.0211221.|02211,0211221.0201122,11.0211221.",
    u"醉花阴": "0201122,02112.02211,0211,02112.|0102112,22112.02211,0211,02112.",
    u"鹧鸪天": "0211021,0112211.0102112,0211021.|022,211,0112211.0102112,0211021.",
    u"临江仙": "0201122,010211.0102211,01122,02211.|0201122,010211.0102211,01122,02211.",
    u"虞美人": "0102112,02112.0102211,020102211.|0102112,02112.0102211,020102211.",
    u"水调歌头": "02012,02211.010212,02211.020102,020102,02211.02012,02211.|000,002,011.0102,0202211.020102,020102,02211,02012,02211.",
    u"念奴娇": "0102,210`020112.0201122,020112.0211,0102,22112.0102,011212.|020211,0112,02112.0201122,020112.0211,0102,02112.0102,011212.",
    u"满江红": "0211,102`0102.002`0112,2102.0201122,0102112.201`02211,112.|002,102.122,112.21102,2122.0201122,0102112.201`02211,112.",
    u"点绛唇": "0211,0102112.0102,02112.|0201,02112.002.0102,02112.",
    u"清平乐": "0002,02112.0201102,020102.|020211,000201.020102,000211.",
    u"减字木兰花": "0102,0201122.0211,0211021.|0102,0201122.0211,0211021.",
    u"满庭芳": "0211,0102,201211.2112,12211.021122,002`0211.112,0102,02211.|11,122,1122,0211.21211,0211.020122,002`0211.112,0102,02211.",
    u"朝中措": "0102211,02211.020102,010211.|0102,0102,0211.020102,010211.",
    u"卜算子": "02211,02112.0211221,02112.|02211,02112.0211221,02112.",
    u"谒金门": "002,020102.0201122,00102.|020102,020102.0201122,00102.",
    u"浪淘沙": "02211,0211.0102211.0201122,0211.|02211,0211.0102211.0201122,0211.",
    u"踏莎行": "2211,1122,0102112.0102211,0102112.|2211,1122,0102112.0102211,0102112.",
    u"渔家傲": "0201122,0102112.0201122.102,0102112.|0201122,0102112.0201122.102,0102112.",
    u"青玉案": "0102112,202`112.0201122.0102,0112,02112.|0102112,0211212.0201122.0102,0102,02112.",
    u"柳梢青": "0211,0102,2211.0211,0102,0211.|010211,202`1121.0211,0102,0211.",
    u"生查子": "00000,02112.00201,02112.|00001,02112.02211,00012.",
    u"醉落魄": "0102,0102112,0102112.2211,02112.|0201122,1102112,2102112.2211,22112.",
    u"蓦山溪": "1102,02112.02211,200`1102.2112,02211,122.122,02112.|1102,02112.02211,200`1102.2112,02211,122,122.02112.",
    u"小重山": "0211021.01122,211.0102211.102,02211.|02211.01122,211.0102211.102,02211.",
    u"诉衷情": "0102211,02211.010212,02211.|122`211,211.0102,0211,2211.",
    u"江城子": "0102211.211,211.0201,02211.0201122,122,211.|0102211.211,211.0201,02211.0201122,122,211.",
    u"瑞鹤仙": "21122,122`221122.11212,21112,1112.1122.221`1222.21122,1221,2212.|221122,2211,2112.1122.112,212.21122,1112,111222.21122.122122.",
    u"阮郎归": "0102211,11221.0102211,11221.|122,211.122,211,11221.0102211,11221.",
    u"玉楼春": "0102112,0201122.0102211,0201122.|0102112,0201122.0102211,0201122.",
    u"摸鱼儿": "211`2112,111212.0112112,122112.122,212,0102112.0102.22211,0102,02212.|112,021122.111212.0102112,020112.122,212,0102112.0102.22211,0102,02212.",
    u"感皇恩": "02211,0102,0211212.0102,020112.01122,112.|0201,0102,0211212.2102,020112.01021,002.",
    u"眼儿媚": "0102211,02211.0102,0102,2211.|0102112,02211.0102,0102,2211.",
    u"醉蓬莱": "21122,2211,2112.2211,21112.2211,2112,22112.2211,1122,2112.|2211,2112,2211,2112.1211,22112.2211,2212,22112.2211,1112,2112.",
    u"一剪梅": "0211221.0211,0211.0102211.0211,0211.|0211021.0211,0211.0102211.0211,0211.",
    u"声声慢": "0102,0211,100121.0211,100211.012022,201`0211.002,20102,0211.|021102,20102,0211.0211,100211.012022,201`0211.002,200`1221.",
    u"少年游": "0102211,02211.0102,0102,02211.|0102112,02211.0211,0102,02211.",
    u"千秋岁": "2112,02112.122,112.11122,12112.122,2122112.|22112,12112.122,112.21122,22112.122,2122112.",
    u"霜天晓角": "0102,02112.122112,002`112.|01122,01122.122112,002`112.",
    u"喜迁莺": "0112,20201,1112.0211,0102,022112.022112,121112.202,21102,0112.|12,121,1221,02112.0211,0100,022112.022112,020112.212,21102,0112.",
    u"永遇乐": "2211,2112,1212.2211,1122,22112.1112,1112,222112.211,1122,212212.|1122,1112,221122.2211,1122,22112.1122,1122,221122.112`1122,2122.",
    u"行香子": "0211,0211.010`0211.0102,0211.2010,012,011.|0102,0211.010`0211.0102,0211.2010,012,211.",
    u"祝英台近": "211,122,12212.0211,02212.010211,0102,212`0112.|212,001211,01212.0211,00212.010211,0102,212`0112.",
    u"采桑子": "0102112,0211.0211,0211221.|0102112,0211.0211,0211221.",
    u"汉宫春": "0211,20102,0211.0102,200211.1122,211`0211.122`1102,010211.|020112,21122,0211.112122,0211.112122,0211.1122,211`0211.122`1102,010211.",
    u"风入松": "0102211,02211.0102112,010`0211.021112,010211.|0102211,02211.0102112,010`0211.021112,010211.",
    u"定风波": "0211021,0102211.0201102,02,0102211.|0201122.02,0102211.0201122,02,0102211.",
}

class Learn:
    def __init__(self, sourceFile, rhythmFile):
        self.sourceFile = sourceFile
        self.rhythmFile = rhythmFile

        self.title2pingze = {}
        self.title2delimiter = {}
        self.word2rhythm = {}
        self.word2pingze = {}
        self.bigramCount = {}
        self.bigramWord2VecModel = None
        self.trigramWord2VecModel = None

    def buildTitle2Pingze(self):
        for CiPaiMing, PingZeSentence in title2rhythm.iteritems():
            self.title2pingze[CiPaiMing] = re.findall(r"[0-9]+", PingZeSentence)

            delimiters = []
            for word in PingZeSentence:
                if word in [",", ".", "`", "|"]:
                    delimiters.append(word)
            self.title2delimiter[CiPaiMing] = delimiters

    def pingzeRhythm2words(self):
        with open(self.rhythmFile, 'r') as f:
            line1 = f.readline().strip().decode("utf-8")
            while line1 != "END":
                line2 = f.readline().strip().decode("utf-8")
                rhythmWord = line1[1]
                isPing = True
                if line1[0] == "平":
                    isPing = True
                else:
                    isPing = False

                for word in line2:
                    self.word2rhythm[word] = rhythmWord
                    if isPing:
                        self.word2pingze[word] = '1'
                    else:
                        self.word2pingze[word] = '2'
                    #words.append(word)
                line1 = f.readline().strip().decode("utf-8")

    def countRhyth(self):
        with open(self.sourceFile, 'r') as f:
            line = f.readline().strip().decode("utf-8")
            while line != "END":
                if line == "" or ((u"，" not in line) and (u"。" not in line)):
                    line = f.readline().strip().decode("utf-8")
                    continue
                sentences = re.split(u"[，。、]", line)
                for sentence in sentences:
                    if sentence:
                        sentenceLen = len(sentence)
                        if sentenceLen == 4:
                            self.buildBigram(sentence[0], sentence[1])
                            self.buildBigram(sentence[2], sentence[3])
                        elif sentenceLen == 5:
                            self.buildBigram(sentence[0], sentence[1])
                        elif sentenceLen == 6:
                            self.buildBigram(sentence[0], sentence[1])
                            self.buildBigram(sentence[2], sentence[3])
                            self.buildBigram(sentence[4], sentence[5])
                        elif sentenceLen == 7:
                            self.buildBigram(sentence[0], sentence[1])
                            self.buildBigram(sentence[2], sentence[3])
                        elif sentenceLen == 9:
                            self.buildBigram(sentence[0], sentence[1])
                            self.buildBigram(sentence[2], sentence[3])
                            self.buildBigram(sentence[4], sentence[5])
                line = f.readline().strip().decode("utf-8")
            self.bigramCount = sorted(self.bigramCount.items(), key=operator.itemgetter(1), reverse=True)

    def buildBigram(self, firstWord, lastWord):
        bigram_key = firstWord + lastWord
        if bigram_key not in self.bigramCount:
            self.bigramCount[bigram_key] = 1
        else:
            self.bigramCount[bigram_key] += 1

    def sentenceSegment(self, line):
        sentences = re.split(u"[，。、]", line)
        bigramRes = []
        trigramRes = []
        for sentence in sentences:
            length = len(sentence)
            if length == 2:
                bigramRes.append(sentence)
            elif length == 3:
                trigramRes.append(sentence)
            elif length == 4:
                bigramRes.append(sentence[0:2])
                bigramRes.append(sentence[2:])
            elif length == 5:
                bigramRes.append(sentence[0:2])
                trigramRes.append(sentence[0:2])
                trigramRes.append(sentence[2:])
            elif length == 6:
                bigramRes.append(sentence[0:2])
                bigramRes.append(sentence[2:4])
                bigramRes.append(sentence[4:])
            elif length == 7:
                bigramRes.append(sentence[0:2])
                bigramRes.append(sentence[2:4])
                trigramRes.append(sentence[2:4])
                trigramRes.append(sentence[4:])
        return bigramRes, trigramRes

    def word2vec(self):
        bigramRes = []
        trigramRes = []
        with open(self.sourceFile, 'r') as f:
            line = f.readline().strip().decode("utf-8")
            while line != "END":
                if line == "" or ((u"，" not in line) and (u"。" not in line)):
                    line = f.readline().strip().decode("utf-8")
                    continue
                biTmp, triTmp = self.sentenceSegment(line)
                if len(biTmp) > 0:
                    bigramRes.append(biTmp)
                if len(triTmp) > 0:
                    trigramRes.append(triTmp)
                line = f.readline().strip().decode("utf-8")
        self.bigramWord2VecModel = models.Word2Vec(bigramRes, min_count=5)
        self.bigramWord2VecModel.save("./model/bigramWordModel")

        self.trigramWord2VecModel = models.Word2Vec(trigramRes, min_count=2)
        self.trigramWord2VecModel.save("./model/trigramWordModel")

    def saveModel(self):
        for dataFile in modelFilesList:
            fileName = "./model/" + dataFile
            with open(fileName, "w") as f:
                value = getattr(self, dataFile)
                json.dump(value, f)
                print "finish writing model " + dataFile

    def buildModel(self):
        self.buildTitle2Pingze()
        print "finish title_pingze"

        self.pingzeRhythm2words()
        print "finish pingzeRhythm2words"

        self.countRhyth()
        print "finish countRhyth"

        self.word2vec()
        print "finish build_word2vec"

        self.saveModel()

if __name__ == '__main__':
    # sourceFile = sys.argv[1];
    # rhythmFile = sys.argv[2];
    sourceFile = "./data/training_data.txt"
    rhythmFile = "./data/pingze.txt"
    begin = time.time()
    learn = Learn(sourceFile, rhythmFile)
    learn.buildModel()
    end = time.time()
    print "finish building model, using " + str(end - begin) + "seconds"
