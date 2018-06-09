# -*- coding:utf-8 -*-
import jieba
from numpy import *
from pymongo import MongoClient

client = MongoClient('localhost',27017)
db=client.comment
collection=db.labelled

def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords

def seg_sentence(sentence):
    sentence_seged = jieba.cut(sentence.strip())
    stopwords = stopwordslist('stopwords.txt')  # 这里加载停用词的路径
    returnlist = []
    for word in sentence_seged:
        if word not in stopwords:
            returnlist.append(word)
    return returnlist

def createVocabList():
    docList = []
    classList = []
    for item in collection.find():
        wordList = seg_sentence(item.get('comment'))  # 对每个评论分词
        docList.append(wordList)  # 所有评论分词列表
        classList.append(item.get('sentiment'))

    vocabSet = set([])  # create empty set
    for document in docList:
        vocabSet = vocabSet | set(document)  # 生成不重复的单词表
    vocabList = list(vocabSet)
    # print(vocabList.__len__())

    with open("vocab.txt", 'w', encoding='utf-8') as f:
        for vocab in vocabList:
            f.write(vocab+"\n")

    return vocabList,docList,classList

def bagOfWords2VecMN(vocabList, inputSet):
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
    return returnVec

def trainNB0(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory) / float(numTrainDocs)
    p0Num = ones(numWords)
    p1Num = ones(numWords)  # change to ones()
    p0Denom = 2.0
    p1Denom = 2.0  # change to 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vect = p1Num / p1Denom  # change to log()
    p0Vect = p0Num / p0Denom  # change to log()
    return p0Vect, p1Vect, pAbusive

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)  #element-wise mult
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else:
        return 0

if __name__ == "__main__":
    vocabList,docList,classList = createVocabList()
    print("生成词汇表完成！")

    trainMat = []                   #训练集
    trainClasses = []
    demarcation = (int)(collection.count()*0.7) #70%作为测试集

    for i in range(demarcation):
        trainMat.append(bagOfWords2VecMN(vocabList, docList[i]))
        trainClasses.append(classList[i])
    print(trainClasses)
    p0V, p1V, pSpam = trainNB0(array(trainMat), array(trainClasses))  # 训练
    print("训练完毕")

    count = 0
    errorCount = 0

    for i in range(demarcation,collection.count()):
        count += 1
        wordVector = bagOfWords2VecMN(vocabList, docList[i])
        if classifyNB(array(wordVector), p0V, p1V, pSpam) != classList[i]:
            errorCount += 1

    print("错误率：",float(errorCount) / count)