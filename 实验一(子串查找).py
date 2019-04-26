import tkinter as tk

root = tk.Tk()
root.title('实验一')

l = tk.Label(root,text='串x=')
l.grid(row=0,column=0)

e = tk.Entry(root)
e.grid(row=0,column=1)

def parseString():
    myStr = e.get()
    prefix = []
    suffix = []
    substring = []
    t.insert('insert','x的所有前缀：\n')
    for i in range(1,len(myStr)+1):
        prefix.append(myStr[:i])
        t.insert('insert',myStr[:i]+'\n')
    t.insert('insert','∅\n')
    t.insert('insert','x所有前缀的个数：{}\n'.format(len(myStr)+1))
    t.insert('insert','x的所有后缀：\n')
    for i in range(len(myStr)-1,-1,-1):
        suffix.append(myStr[i:])
        t.insert('insert',myStr[i:]+'\n')
    t.insert('insert','∅\n')
    t.insert('insert','x所有后缀的个数：{}\n'.format(len(myStr)+1))
    t.insert('insert','x除前后缀的所有子串：\n')
    substring = [myStr[i:i + x + 1] for x in range(len(myStr)) for i in range(len(myStr) - x)]
    substring = set(substring)-set(prefix)-set(suffix)
    for i in substring:
        t.insert('insert',i+'\n')
    t.insert('insert','x除前后缀的所有子串的个数：\n{}'.format(len(substring)))

def clearText():
    t.delete('1.0','end')

pasre = tk.Button(root,text='解析',command=parseString)
pasre.grid(row=1,column=0)

clear = tk.Button(root,text='清空',command=clearText)
clear.grid(row=1,column=1)

t = tk.Text(root)
t.grid(row=2,column=0,columnspan=2)

root.mainloop()