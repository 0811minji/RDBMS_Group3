from tkinter import *

class displayResult:

    def __init__(self, frame, result, columns):
        
        self.frame = frame
        self.result = result
        self.columns = columns

    def knowledge(self):

        k = 0
        for cols in self.columns:
            res_label = Label(
                self.frame, 
                text=cols, 
                font=("Arial", 10, "bold"),  # 굵은 글씨체
                bg="azure",                 # 배경색 추가
                #width=col_widths[k] + 2 
            )
            res_label.grid(row=2, column=k, padx=5, pady=5)  # 패딩 추가
            k += 1
        
        i = 2
        for res in self.result:
            for j in range(len(res)):
                print(res[j])
                if j == len(res)-2:
                    res_label = Label(self.frame, text=res[j].replace('\\n', '\n'), justify="left")
                    res_label.grid(row=i+1, column=j)
                else:
                    res_label = Label(self.frame, text=res[j])
                    res_label.grid(row=i+1, column=j)
            i+=1

    def others(self, idx):
        k = 0
        for cols in self.columns:
            res_label = Label(self.frame, text=cols)
            res_label.grid(row=2, column=k)
            k+=1
        
        i = 10*idx+2
        for res in self.result:
            for j in range(len(res)):
                print(res[j])
                res_label = Label(self.frame, text=res[j])
                res_label.grid(row=i+1, column=j)
            i+=1