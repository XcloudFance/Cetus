
import nltk
import csv
import os
import re
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
 
#np noun phrase
#pp prepositional phrase
#vp verb phrase
f = open("./holmes/nava.txt",'r')
content = f.read()
f.close()

document = content


class NormalChunks:
    def __init__(self):
        self.grammar = r"""

        NP: {<DT>?<JJ|VBN|VBG>+<NN.*>+}

        PP: {<IN><NP>}   
        AVP: {<RB.*><VB.*>}    

        TV: {<TO|AVP><VB.*>}            
        VNP: {<VB.*><NP|PP|CLAUSE>+$} 
        VP: {<TV|VB.*><NP>}
        AJJ: {<RB.*><JJ>}
        JJIN: {<JJ>.*<IN>}

        RBIN: {<RB.*><IN>}
        VIN: {<IN>+<NN|NNS|VB.*>.*<IN|TO>(<DT>?<NN.*>)*}
        RBINNP: {<RBIN><NN.*|NP>}
        """
        
    def getChunks(self,parsedTree):
        res = []
        donotShow = ['TV']
        for i in parsedTree:
            if type(i) != tuple:
                if i.label() in donotShow:
                    continue
                res.append((i.label(),self.traverse(i).strip()))
        return res
    
    def traverse(self,content):
        ret = ""
        for i in content:
            if type(i) == str:
                return i + " "
            else:
                ret += self.traverse(i)
        return ret



    def preprocess(self,sentences: str):
        sentenceTree = nltk.sent_tokenize(sentences)
        sentenceTree = [nltk.word_tokenize(sent) for sent in sentenceTree]
        sentenceTree = [nltk.pos_tag(sent) for sent in sentenceTree]
        return sentenceTree

    def getCohesion(self, sentence: str,row = 0):

        grammar = r''' #单独匹配
            COM: {<,>?<.+>{2,5}<,>}
        '''
        sentenceTree = self.preprocess(sentence)[row]
        regexp = nltk.RegexpParser(grammar,loop=2)
        parsedTree = regexp.parse(sentenceTree)
        return (parsedTree)


    def normalChunks(self,sentence: str,row = 0):
        try:
            sentenceTree = self.preprocess(sentence)[row]


            cp = nltk.RegexpParser(self.grammar,loop=2)
            res = cp.parse(sentenceTree)
            return self.getChunks(res)
        except:
            return []


class extractFromFiles:
    def __init__(self):
        dirs = os.listdir('./phrases')
        with open('./phrases/'+dirs[4], "r") as f:
            reader = csv.reader(f)
            self.phraseTable = []
            for row in reader:
                self.phraseTable.append(row)
            self.wnl = WordNetLemmatizer()
    def analysisSentence(self,sentence):
        for i in self.phraseTable:
            con = i[0].replace("...",".*")
            con = i[0].replace("be","(be|are|is|was|were|am)")
            con = i[0].replace("one",".+")
            con = i[0].replace("sth.",".*")
            con = i[0].replace("sth",".*")            
            con = i[0].replace("sb.",".*")
            con = i[0].replace("sb",".*")
            con = '.*' + con + '.*'
            ret = re.match(con,sentence,re.IGNORECASE)
            
            if ret != None: 
                print(i[0])





eff1 = extractFromFiles()
normal = NormalChunks()
out = []
for i in content.split('.'):
    res = normal.normalChunks(i)
    if res != []:
        out.append(res)
    
print(out)