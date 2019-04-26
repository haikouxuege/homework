import numpy as np
import tkinter as tk
from scipy import spatial

root = tk.Tk()
root.title('实验三')

lV1 = tk.Label(root,text='V1=')
lV1.grid(row=0,column=0)

lV2 = tk.Label(root,text='V2=')
lV2.grid(row=1,column=0)

eV1 = tk.Entry(root)
eV1.grid(row=0,column=1)

eV2 = tk.Entry(root)
eV2.grid(row=1,column=1)

tResult = tk.Text(root)
tResult.grid(row=3,column=0,columnspan=3)

def cosineSimilarity():
    x=eval(eV1.get())
    y=eval(eV2.get())

    result = 1 - spatial.distance.cosine(x, y)
    
    tResult.insert('insert','V1={}\n'.format(str(x)))
    tResult.insert('insert','V2={}\n'.format(str(y)))
    tResult.insert('insert','余弦相似度={}\n\n'.format(str(result)))

def clearText():
    tResult.delete('1.0','end')

pasre = tk.Button(root,text='计算',command=cosineSimilarity)
pasre.grid(row=2,column=0)

clear = tk.Button(root,text='清空',command=clearText)
clear.grid(row=2,column=1)

root.mainloop()