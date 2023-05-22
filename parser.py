from readmdict import MDX, MDD  # pip install readmdict
from pyquery import PyQuery as pq  # pip install pyquery
from bs4 import BeautifulSoup
import re
import copy

'''
# 如果是windows环境，运行提示安装python-lzo，但
> pip install python-lzo
报错“please set LZO_DIR to where the lzo source lives” ，则直接从 https://www.lfd.uci.edu/~gohlke/pythonlibs/#_python-lzo 下载 "python_lzo‑1.12‑你的python版本.whl" 
> pip install xxx.whl 
装上就行了，免去编译的麻烦
'''



class Parser:
    def __init__(self, filename):
        self.headwords = [*MDX(filename)]  # 单词名列表
        self.items = [*MDX(filename).items()]  # 释义html源码列表
        if len(self.headwords) == len(self.items):
            print(f'加载成功：共{len(self.headwords)}条')
        else:
            print(f'【ERROR】加载失败{len(self.headwords)}，{len(self.items)}')

    def searchWord(self, queryWord):
        # 查词，返回单词和html文件
        # print(len(self.headwords))
        if queryWord.encode() not in self.headwords:
            print("not in the list")
            return None, None
        wordIndex = self.headwords.index(queryWord.encode())
        word, html = self.items[wordIndex]
        return word.decode(), html.decode()
        # print(word, html)

    # 从html中提取需要的部分，这里以the litte dict字典为例。到这一步需要根据自己查询的字典html格式，自行调整了。

    def getContentFromHtml(self, html: object, word) -> object:
        soup = BeautifulSoup(html, 'html.parser')

        word_entries = soup.find_all('span', class_='entry')
        # print(len(word_entries))
        exampleList = []
        exampleList_c = []
        for word_entry in word_entries:
            meanings = word_entry.find_all('span', class_='sense newline')
            for meaning in meanings:
                phrases = meaning.find_all('span', class_='gramexa')
                for phrase in phrases:
                    examples = phrase.find_all('span', class_='example')
                    examples_ch = phrase.find_all('span', class_='example_c')
                    for i in range(len(examples)):
                        example = examples[i]
                        example_ch = examples_ch[i]
                        example = re.sub(r"\s+", " ", example.text.replace("\n", "")).strip()
                        example_ch = re.sub(r"\s+", " ", example_ch.text.replace("\n", "")).strip()
                        exampleList.append(example)
                        exampleList_c.append(example_ch)
        return {'word': word, 'exampleList': exampleList, 'exampleList_c': exampleList_c}

    def getContentFromHtmlSimplified(self, html: object, word) -> object:
        soup = BeautifulSoup(html, 'html.parser')

        # print(len(word_entries))
        exampleList = []
        exampleList_c = []

        for meaning in soup.find_all('span', class_='sense newline'):
            examples = meaning.find_all('span', class_='example')
            for example in examples:
                exampleText = re.sub(r"\s+", " ", example.text.replace("\n", "")).strip()

                nextSib = example.next_sibling
                if nextSib is None:
                    continue
                if len(nextSib.text) < 3:
                    continue
                exampleList.append(exampleText)
                example_ch = re.sub(r"\s+", " ", nextSib.text.replace("\n", "")).strip()
                exampleList_c.append(example_ch)
        return {'word': word, 'exampleList': exampleList, 'exampleList_c': exampleList_c}

    def removeTheOriginWord(self, res):
        res_temp = copy.deepcopy(res)
        re1 = re.compile(res_temp['word'][:-1] + r'\w*')
        for i in range(len(res_temp['exampleList'])):
            sentence = res_temp['exampleList'][i]
            sentence_removed = re.sub(re1, '＿＿＿＿＿＿', sentence, flags=0)
            res_temp['exampleList'][i] = sentence_removed
        return res_temp

