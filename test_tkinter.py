import tkinter as tk
from tkinter import filedialog as fd
import handler


def choose_file():
    filetypes = (("XML", "*.xml"),
                 ("Любой", "*"))
    filename = fd.askopenfilename(title="Открыть файл", initialdir="/",
                                  filetypes=filetypes)
    label['text'] = filename


win = tk.Tk()
win.title('Handler')
win.config(bg='red')
win.geometry('500x500+100+100')
win.resizable(False, False)

label = tk.Label(win, text="Hello, QA")
button_1 = tk.Button(win, text='Получить путь к XML', command=choose_file)
button_2 = tk.Button(win, text='Запустить процесс генерации XML', command=lambda: handler.bag(label['text']))

label.pack()
button_1.pack()
button_2.pack()

if __name__ == "__main__":
    win.mainloop()
