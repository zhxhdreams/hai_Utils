#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Author: hai  
# @Date: 2017-06-03 10:21:48

__author__ = 'hai'


class WordNode(object):

    def __init__(self, value):
        self.value = value
        self.next = []
        self.isWord = False
        self.type = []

    def find(self, value):
        for item in self.next:
            if item.value == value:
                return item
        return None

    def add(self, value):
        temp = self.find(value)
        if not temp:
            temp = WordNode(value)
            self.next.append(temp)
        return temp


class WordTree(object):

    def __init__(self):
        self.wordTree = []

    def find(self, char):
        for node in self.wordTree:
            if node.value == char:
                return node
        return None

    def addWordtoTree(self, word, wtype):
        length = len(word)
        parrent = None
        for i, ch in enumerate(word):
            if not parrent:
                parrent = self.find(ch)
                if not parrent:
                    parrent = WordNode(ch)
                    self.wordTree.append(parrent)
            else:
                parrent = parrent.add(ch)
            if i == (length - 1):
                parrent.isWord = True
                if wtype not in parrent.type:
                    parrent.type.append(wtype)


if __name__ == '__main__':
    print('The Module WordTree~')
