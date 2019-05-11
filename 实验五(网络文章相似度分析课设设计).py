#!/usr/bin/ python3
#encoding=utf-8

'''
@Author: xxlin
@LastEditors: xxlin
@Date: 2019-05-09 22:43:03
@LastEditTime: 2019-05-11 08:18:38
'''

import math
import tkinter as tk
import re

import jieba
import jieba.analyse
import numpy as np
import requests
from lxml import etree
from scipy import spatial

root = tk.Tk()
root.title('课程设计')

eURL1 = tk.Entry(root)
eURL1.grid(row=0,column=1)

eURL2 = tk.Entry(root)
eURL2.grid(row=1,column=1)

eCosine = tk.Entry(root,text='')
eCosine.grid(row=0,column=3)

lURL1 = tk.Label(root,text='URL1=')
lURL1.grid(row=0,column=0)

lURL2 = tk.Label(root,text='URL2=')
lURL2.grid(row=1,column=0)

lArticle1 = tk.Label(root,text='文章1')
lArticle1.grid(row=2,column=0,columnspan=2)

lArticle2 = tk.Label(root,text='文章2')
lArticle2.grid(row=2,column=2,columnspan=2)

lArticle1_TF_IDF = tk.Label(root,text='文章1 TF.IDF向量')
lArticle1_TF_IDF.grid(row=4,column=0,columnspan=2)

lArticle2_TF_IDF = tk.Label(root,text='文章2 TF.IDF向量')
lArticle2_TF_IDF.grid(row=4,column=2,columnspan=2)

lCosine = tk.Label(root,text='余弦相似度')
lCosine.grid(row=0,column=2)

tArticle1 = tk.Text(root,height=20, width=60)
tArticle1.grid(row=3,column=0,columnspan=2)

tArticle2 = tk.Text(root,height=20, width=60)
tArticle2.grid(row=3,column=2,columnspan=2)

tArticle1_TF_IDF = tk.Text(root,height=20, width=60)
tArticle1_TF_IDF.grid(row=5,column=0,columnspan=2)

tArticle2_TF_IDF = tk.Text(root,height=20, width=60)
tArticle2_TF_IDF.grid(row=5,column=2,columnspan=2)

def parseHtml(url):
    '''
    @description: 解析html页面，获取文章标题内容
    @param {type} 
    @return: 
    '''
    r = requests.get(url)
    html = etree.HTML(r.content.decode('utf-8'))
    '''
    title = html.xpath('//*[@id="module_3001_SG_connBody"]/h1')[0].text
    content = html.xpath('//*[@id="sina_keyword_ad_area2"]')[0].xpath('string(.)')
    '''
    #编译正则表达式
    regex = re.compile('[\u4e00-\u9fa5]')
    #使用该表达式匹配字符串
    temp = ''
    for each_part in regex.findall(r.content.decode('utf-8')):
        temp += each_part
    #return title+content
    return temp

def words2vec(words1=None, words2=None):
    '''
    @description: 文章分词，并转换成向量
    @param {type} 
    @return: 
    '''
    v1 = []
    v2 = []
    tag1 = jieba.analyse.extract_tags(words1, withWeight=True)
    tag2 = jieba.analyse.extract_tags(words2, withWeight=True)
    tag_dict1 = {i[0]: i[1] for i in tag1}
    tag_dict2 = {i[0]: i[1] for i in tag2}
    merged_tag = set(tag_dict1.keys()) | set(tag_dict2.keys())
    for i in merged_tag:
        if i in tag_dict1:
            v1.append(tag_dict1[i])
        else:
            v1.append(0)
        if i in tag_dict2:
            v2.append(tag_dict2[i])
        else:
            v2.append(0)
    return v1, v2

def cosineSimilarity(vector1, vector2):
    '''
    @description: 计算余弦相似度
    @param {type} 
    @return: 
    '''
    dot_product = 0.0
    normA = 0.0
    normB = 0.0
    for a, b in zip(vector1, vector2):
        dot_product += a * b
        normA += a ** 2
        normB += b ** 2
    if normA == 0.0 or normB == 0.0:
        return 0
    else:
        return round(dot_product / ((normA**0.5)*(normB**0.5)) * 100, 2)
     
def cosine(str1, str2):
    '''
    @description: 封装计算余弦相似度
    @param {type} 
    @return: 
    '''
    vec1, vec2 = words2vec(str1, str2)
    return cosineSimilarity(vec1, vec2)

def segmentation(text):
    '''
    @description: 中文分词
    @param {type} 
    @return: 
    '''
    seg_list = jieba.cut(text, cut_all=True)
    temp = []
    for i in seg_list:
        temp.append(i)
    return temp

def TF_IDF(articles):
    '''
    @description: 计算TF-IDF
    @param {type} 
    @return: 
    '''
    tf_idf = []
    idf = []
    tf = []
    articles_nums = len(articles)
    article_len = []
    #计算每篇文章长度
    for article in articles:
        article_len.append(len(article))

    #初始化tf
    for i in range(articles_nums):
        tf.append({})
        for j in articles[i]:
            tf[i][j] = 0

    #TF
    for i in range(articles_nums):
        for j in articles[i]:
            for key in tf[i].keys():
                if key == j:
                    tf[i][key] += 1
    for i in range(articles_nums):
        for key in tf[i].keys():
            tf[i][key] /= article_len[i]

    #初始化tf_idf，idf
    for i in range(articles_nums):
        idf.append({})
        tf_idf.append({})
        for key in tf[i].keys():
            idf[i][key] = 0
            tf_idf[i][key] = 0

    #IDF，计算包含该词文档数
    for i in range(articles_nums):
        for key in tf[i].keys():
            #FIXME:这里硬编码选取两篇文章计数
            if key in articles[0]:
                idf[i][key] += 1
            if key in articles[1]:
                idf[i][key] += 1

    for i in range(articles_nums):
        for key,value in idf[i].items():
            idf[i][key] = math.log10(articles_nums/value)

    #TF_IDF
    for i in range(articles_nums):
        for key in tf_idf[i].keys():
            tf_idf[i][key] = tf[i][key] * idf[i][key]

    return tf,idf,tf_idf

def calcAll():
    '''
    @description: 获取所有结果，并插入结果到文本控件中
    @param {type} 
    @return: 
    '''
    url1 = eURL1.get()
    url2 = eURL2.get()
    eCosine.insert(0,cosine(parseHtml(url1),parseHtml(url2)))
    tArticle1.insert('insert',parseHtml(url1))
    tArticle2.insert('insert',parseHtml(url2))
    articles = [segmentation(parseHtml(url1)),segmentation(parseHtml(url2))]
    temp = TF_IDF(articles)
    for key,value in temp[2][0].items():
        tArticle1_TF_IDF.insert('insert','{}={}\n'.format(key,value))
    for key,value in temp[2][1].items():
        tArticle2_TF_IDF.insert('insert','{}={}\n'.format(key,value))

def clearText():
    '''
    @description: 清空文本框
    @param {type} 
    @return: 
    '''
    eCosine.delete('1.0','end')
    tArticle1.delete('1.0','end')
    tArticle2.delete('1.0','end')
    tArticle1_TF_IDF.delete('1.0','end')
    tArticle2_TF_IDF.delete('1.0','end')

calc = tk.Button(root,text='计算',command=calcAll)
calc.grid(row=1,column=2)

clear = tk.Button(root,text='清空',command=clearText)
clear.grid(row=1,column=3)

root.mainloop()
