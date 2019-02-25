#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Author: hai
# @Created Date: 2017-06-03 10:21:48

__author__ = 'hai'


class WordNode(object):

    def __init__(self, value):
        # 当前字符值
        self.__value = value
        # 存放下一字符值的列表
        self.__next = []
        # 从根节点到当前节点值连起来的串是否是一个单词
        self.__isWord = False
        # 从根节点到当前节点值连起来的串是一个单词，存放当前单词的词性
        self.__type = []

    # 寻找value是否在当前字符的下一字符列表中
    def find(self, value):
        for item in self.__next:
            if item.getValue().encode('UTF-8') == value.encode('UTF-8'):
                return item
        return None

    # 添加value到当前字符的下一字符列表中
    def addValue(self, value):
        temp = self.find(value)
        if not temp:
            temp = WordNode(value)
            self.__next.append(temp)
        return temp

    # 从根节点到当前节点值连起来的串是一个单词，添加词性到词性列表中
    def addType(self, wtype):
        if wtype not in self.__type:
            self.__type.append(wtype)

    # 从根节点到当前节点值连起来的串是一个单词，设置当前节点标志，是否为一个词
    def setIsWord(self, isWord):
        self.__isWord = isWord

    # 获取当前节点标志，是否为一个词
    def getIsWord(self):
        return self.__isWord

    # 获取当前节点字符值
    def getValue(self):
        return self.__value

    # 从根节点到当前节点值连起来的串是一个单词，获取单词的词性列表
    def getType(self):
        return self.__type

    # 获取下一字符值的列表
    def getNext(self):
        return self.__next


class WordTree(object):

    def __init__(self):
        self.wordTree = []

    # 从树的根列表中寻找某一字符的节点
    def __find(self, ch):
        for node in self.wordTree:
            if node.getValue().encode('UTF-8') == ch.encode('UTF-8'):
                return node
        return None

    # 寻找代表单词的节点
    def findWord(self, word):
        if len(word) == 0:
            return None
        elif len(word) == 1:
            return self.__find(word[0])
        else:
            currNode = None
            for i, ch in enumerate(word):
                if not currNode:
                    currNode = self.__find(ch)
                else:
                    currNode = currNode.find(ch)
                if not currNode:
                    break
            return currNode

    # 添加单词到树中
    def addWord(self, word, wtype):
        parrent = None
        for i, ch in enumerate(word):
            if not parrent:
                parrent = self.__find(ch)
                if not parrent:
                    parrent = WordNode(ch)
                    self.wordTree.append(parrent)
            else:
                # 不用判断是否已存在，addValue函数里有判断
                parrent = parrent.addValue(ch)
        if parrent:
            parrent.setIsWord(True)
            # 不用判断是否已存在，addType函数里有判断
            parrent.addType(wtype)

    # 获取所有节点数量
    def getNodeCount(self):
        count = len(self.wordTree)
        for item in self.wordTree:
            count = count + self.__getNodeCount(item)
        return count

    # 获取单词数量
    def getWordCount(self):
        count = 0
        for item in self.wordTree:
            if item.getIsWord():
                count += 1
            count = count + self.__getNodeCount(item, isWordFilter=True)
        return count

    def __getNodeCount(self, node, isWordFilter=False):
        count = 0
        if isWordFilter:
            if node.getIsWord():
                count += 1
        else:
            count = len(node.getNext())
        for item in node.getNext():
            count = count + self.__getNodeCount(item, isWordFilter)
        return count


if __name__ == '__main__':
    print('The Module WordTree~')
