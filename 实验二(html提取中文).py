import tkinter as tk
import requests
import re

root = tk.Tk()
root.title('实验二')

lUrl = tk.Label(root,text='url')
lUrl.grid(row=0,column=0)

eUrl = tk.Entry(root)
eUrl.grid(row=0,column=1)


tHTML = tk.Text(root)
tHTML.grid(row=1,column=0,columnspan=2)

tContent = tk.Text(root)
tContent.grid(row=1,column=2,columnspan=2)

def parseHtml():
    url = eUrl.get()
    r = requests.get(url)
    regex = re.compile('[\u4e00-\u9fa5]')
    tHTML.insert('insert','源码：\n{}'.format(r.content.decode('utf-8')))
    tContent.insert('insert','文字：\n')
    for content in regex.findall(r.content.decode('utf-8')):
        tContent.insert('insert',content)

def clearText():
    tHTML.delete('1.0','end')
    tContent.delete('1.0','end')

bGet = tk.Button(root,text='get',command=parseHtml)
bGet.grid(row=0,column=2)

clear = tk.Button(root,text='clear',command=clearText)
clear.grid(row=0,column=3)

root.mainloop()