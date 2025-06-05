from tkinter import Tk, ttk, IntVar, StringVar, Canvas
from tkinter.messagebox import showinfo
import numpy as np
from random import randint

def get_words():
    with open("words.txt", 'r', encoding="windows-1251") as file:
        content = file.read()
        return np.char.upper((content.split("\n")))

def get_word():
    number = randint(0, len_all_words - 1)
    return all_words[number]

def do_grid(frame, count_row, count_column):
    for r in range(count_row): frame.rowconfigure(index=r, weight=1)
    for c in range(count_column): frame.columnconfigure(index=c, weight=1)

def make_new_frame1():
    for widget in frame1.winfo_children():
        widget.destroy()
    do_grid(frame1, 1, n.get())
    for i in range(n.get()):
        current_letter = select_word.get()[i]
        lbl = ttk.Label(frame1, text="_", anchor="center", border=2, relief="sunken")
        lbl.grid(row=0, column=i, sticky="nsew")
        if current_letter in labels:
            labels[current_letter].append(lbl)
        else:
            labels[current_letter] = [lbl]


def check_word(selected_letter):
    btn = buttons[selected_letter]
    if selected_letter in select_word.get():
        btn.config(style="Green.TButton", state="disabled")
        for label in labels[selected_letter]:
            label.configure(text=selected_letter)
            number_of_guessed_letters.set(number_of_guessed_letters.get() + 1)
    else:
        btn.config(style="Red.TButton", state="disabled")
        painting(painting_element.get())
        painting_element.set(painting_element.get() + 1)
    if number_of_guessed_letters.get() == n.get():
        count_win.set(count_win.get() + 1)
        showinfo(title="YOU WIN!!!  :)", message=f'Victories: {count_win.get()}\nLosses: {count_lose.get()}\n'
                                                 f'Word: {select_word.get()}')
        new_game()
    elif painting_element.get() > 10:
        count_lose.set(count_lose.get() + 1)
        showinfo(title="YOU LOSE!  :(", message=f'Victories: {count_win.get()}\nLosses: {count_lose.get()}\n'
                                                 f'Word: {select_word.get()}')
        new_game()


def painting(number):
    match number:
        case 1:
            canvas.create_line(200, 260, 250, 260, width=3)
        case 2:
            canvas.create_line(225, 260, 225, 50, width=3)
        case 3:
            canvas.create_line(225, 50, 350, 50, width=3)
        case 4:
            canvas.create_line(350, 50, 350, 100, width=3)
        case 5:
            canvas.create_oval(330, 100, 370, 140, width=3)
        case 6:
            canvas.create_line(350, 140, 350, 200, width=3)
        case 7:
            canvas.create_line(350, 140, 320, 170, width=3)
        case 8:
            canvas.create_line(350, 140, 380, 170, width=3)
        case 9:
            canvas.create_line(350, 200, 320, 230, width=3)
        case 10:
            canvas.create_line(350, 200, 380, 230, width=3)

def new_game():
    global  labels
    labels = {}

    for i in range(n.get()):
        frame1.columnconfigure(i, weight=0)
        frame1.rowconfigure(i, weight=0)

    select_word.set(get_word())
    n.set(len(select_word.get()))
    number_of_guessed_letters.set(0)
    painting_element.set(1)
    make_new_frame1()
    canvas.delete('all')
    for btn in buttons.values():
        btn.config(style='TButton')
        btn.state(['!disabled'])


root = Tk()
root.geometry("700x700+450+80")
root.title("Виселица")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")
style.map('Red.TButton', background=[('disabled', 'red')],foreground=[('disabled', 'white')])
style.map('Green.TButton', background=[('disabled', 'green')],foreground=[('disabled', 'white')])

# ----------------------------------------Переменные
all_words = get_words()
len_all_words = len(all_words)                               # количество слов в словаре
select_word = StringVar(value=get_word())                    # выбиравем рандомное слово
n = IntVar(value=len(select_word.get()))                     # длина выбранного слова
buttons = {}
labels = {}
number_of_guessed_letters = IntVar(value=0)                  # количество угаданных слов
painting_element = IntVar(value=1)                           # элемент висельника
russian_alphabet = list("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ") # русский алфавит
count_win = IntVar(value=0)
count_lose = IntVar(value=0)

# ----------------------------------------Определение frames
frame1 = ttk.Frame(root)
frame1.place(relx=0.5, rely=0.07, relwidth=0.9, relheight=0.07, anchor="center")

frame2 = ttk.Frame(root)
frame2.place(relx=0.5, rely=0.31, relwidth=0.9, relheight=0.4, anchor="center")

frame3 = ttk.Frame(root)
frame3.place(relx=0.5, rely=0.75, relwidth=0.9, relheight=0.45, anchor="center")

# ----------------------------------------Первый frame1 (загаданное слово)
make_new_frame1()

# ----------------------------------------Второй frame2 (рисунок)
canvas = Canvas(frame2, bg="white", width=620, height=270)
canvas.pack(anchor="center", expand=1)

# ----------------------------------------Третий frame3 (алфавит)
do_grid(frame3, 9, 4)
i = 0
for r in range(8):
    for c in range(4):
        letter = russian_alphabet[i]
        btn_alph = ttk.Button(frame3, text=russian_alphabet[i], command=lambda l=letter: check_word(l))
        btn_alph.grid(row=r, column=c, sticky="nsew", padx=1, pady=1)
        buttons[letter] = btn_alph
        i += 1
letter = russian_alphabet[i]
btn_last = ttk.Button(frame3, text=russian_alphabet[i], command=lambda l=letter: check_word(l))
btn_last.grid(row=8, column=0, sticky="nsew", padx=1, pady=1, columnspan=4)
buttons[letter] = btn_last

root.mainloop()