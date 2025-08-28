# main.py

import tkinter as tk
from quiz.game import QuizGame

def main():
    root = tk.Tk()
    game = QuizGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
