import numpy as np
import tkinter as tk
from scipy import spatial
import math

root = tk.Tk()
root.title('实验四')

eS1 = tk.Entry(root)
eS1.grid(row=0,column=1)

eS2 = tk.Entry(root)
eS2.grid(row=1,column=1)

lS1 = tk.Label(root,text='S1=')
lS1.grid(row=0,column=0)

lS2 = tk.Label(root,text='S2=')
lS2.grid(row=1,column=0)

lS1_TF = tk.Label(root,text='S1 TF')
lS1_TF.grid(row=2,column=0)

lS2_TF = tk.Label(root,text='S2 TF')
lS2_TF.grid(row=2,column=1)

lIDF = tk.Label(root,text='IDF')
lIDF.grid(row=2,column=2)

lS1_TF_IDF = tk.Label(root,text='S1 TF.IDF')
lS1_TF_IDF.grid(row=4,column=0)

lS2_TF_IDF = tk.Label(root,text='S2 TF.IDF')
lS2_TF_IDF.grid(row=4,column=1)

tS1_TF = tk.Text(root,height=10, width=30)
tS1_TF.grid(row=3,column=0)

tS2_TF = tk.Text(root,height=10, width=30)
tS2_TF.grid(row=3,column=1)

tIDF = tk.Text(root,height=10, width=30)
tIDF.grid(row=3,column=2)

tS1_TF_IDF = tk.Text(root,height=10, width=30)
tS1_TF_IDF.grid(row=5,column=0)

tS2_TF_IDF = tk.Text(root,height=10, width=30)
tS2_TF_IDF.grid(row=5,column=1)

def TF_IDF(articles):
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
    s1 = eS1.get()
    s2 = eS2.get()
    articles = [s1,s2]
    temp = TF_IDF(articles)
    tS1_TF.insert('insert',temp[0][0])
    tS2_TF.insert('insert',temp[0][1])
    tIDF.insert('insert',temp[1][0])
    tIDF.insert('insert',temp[1][1])
    tS1_TF_IDF.insert('insert',temp[2][0])
    tS2_TF_IDF.insert('insert',temp[2][1])

def clearText():
    tS1_TF.delete('1.0','end')
    tS2_TF.delete('1.0','end')
    tIDF.delete('1.0','end')
    tS1_TF_IDF.delete('1.0','end')
    tS2_TF_IDF.delete('1.0','end')

calc = tk.Button(root,text='计算',command=calcAll)
calc.grid(row=0,column=2)

clear = tk.Button(root,text='清空',command=clearText)
clear.grid(row=1,column=2)

root.mainloop()