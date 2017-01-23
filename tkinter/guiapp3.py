import tkinter as tk 
from tkinter import scrolledtext as st

def button0():
    pass
def button2():
    pass
def button3():
    pass
def button4():
    pass
def hisdel():
    pass
def saveas():
    pass
class Application:
    def __init__(self):
        self.root=tk.Tk()
        self.root.title("title")
        self.root.protocol("WM_DELETE_WINDOW",self.quit)
        lbl = tk.Label(self.root, text="MyApplication.org", font=('Times', '12'),anchor=tk.E,width=20)
        lbl.grid(row=0,column=1,columnspan=5,sticky=tk.E,padx=5, pady=5)
        #テキストエリア
        text=st.ScrolledText(self.root, font=('Times', '10'))
        text.grid(row=1,column=0,columnspan=5,sticky=tk.W+tk.E,padx=5, pady=5)
        #ラベル（コメント）
        msg="コマンドを入力し、選択した部分を実行します。実行は「F1」、「右クリック」、「実行ボタン」"
        lblm = tk.Label(self.root, text=msg, font=('Times', '10'),anchor=tk.W)
        lblm.grid(row=2,column=0,columnspan=5,sticky=tk.W+tk.E,padx=5, pady=5)
        #テキストエリア（入力用）
        inTex = st.ScrolledText(self.root, font=('Times', '12'),height=10)
        inTex.grid(row=3,column=0,columnspan=5,sticky=tk.W+tk.E,padx=5, pady=5)
        #ボタン1
        btn1 = tk.Button(self.root, text="コマンド実行", font=('Times', '12'),anchor=tk.CENTER,command=button0)
        btn1.grid(row=4,column=0,padx=5, pady=5)

        #ボタン２
        btn2 = tk.Button(self.root, text="表示エリアを削除", font=('Times', '12'),anchor=tk.CENTER,command=button2)
        btn2.grid(row=4,column=1,padx=5, pady=5)

        #ボタン3
        btn3 = tk.Button(self.root, text="コマンドエリアを削除", font=('Times', '12'),anchor=tk.CENTER,command=button3)
        btn3.grid(row=4,column=2,padx=5, pady=5)

        #ボタン4
        btn4 = tk.Button(self.root, text="履歴表示", font=('Times', '12'),anchor=tk.CENTER,command=button4)
        btn4.grid(row=4,column=3,padx=5, pady=5)

        #ボタン5
        btn5 = tk.Button(self.root, text="履歴削除", font=('Times', '12'),anchor=tk.CENTER,command=hisdel)
        btn5.grid(row=4,column=4, padx=5, pady=5)

        #ボタン6
        btn6 = tk.Button(self.root, text="保存", font=('Times', '12'),anchor=tk.CENTER,width=10,command=saveas)
        btn6.grid(row=2,column=1,columnspan=5,sticky=tk.E,padx=5, pady=5)
    def mainloop(self):
        self.root.mainloop()
        self.root.destroy()

    def quit(self):
        self.root.quit()

def main():
    app=Application()
    app.mainloop()


if __name__ == '__main__':
    main()