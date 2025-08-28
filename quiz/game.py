# quiz/game.py

import random
import itertools
import tkinter as tk

from .config import CATEGORY_COLORS, OPTION_COLORS
from .data import categories
from .utils import clear_window

class QuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Preguntas")
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda e: self.exit_or_menu())

        self.score = 0
        self.question_count = 0
        self.current_question = None
        self.questions = []

        self.category_colors = CATEGORY_COLORS
        self.option_colors   = OPTION_COLORS
        self.categories      = categories

        self.show_menu()

    def exit_or_menu(self):
        if getattr(self, 'in_menu', False):
            self.root.destroy()

    def show_menu(self):
        clear_window(self.root)
        self.in_menu = True
        self.score = 0
        self.question_count = 0

        tk.Label(self.root,
                 text="🎮 Juego de Preguntas 🎮",
                 font=("Arial", 36, "bold"),
                 fg="white",
                 bg="darkblue").pack(fill="x", pady=20)

        tk.Label(self.root,
                 text="Selecciona una categoría",
                 font=("Arial", 24),
                 fg="black").pack(pady=20)

        for category in self.categories:
            tk.Button(self.root,
                      text=category,
                      font=("Arial", 20, "bold"),
                      bg=self.category_colors[category],
                      fg="white",
                      width=20,
                      height=2,
                      command=lambda c=category: self.start_game(c)
                     ).pack(pady=10)

    def start_game(self, category):
        self.in_menu = False
        self.category = category
        self.questions = random.sample(self.categories[category], 5)
        self.question_count = 0
        self.next_question()

    def next_question(self):
        if self.question_count >= len(self.questions):
            return self.show_result()

        self.current_question = self.questions[self.question_count]
        self.question_count += 1
        self.show_question()

    def show_question(self):
        clear_window(self.root)
        question, options, answer = self.current_question
        bg_color = self.category_colors[self.category]
        self.root.config(bg=bg_color)

        tk.Label(self.root,
                 text=f"Categoría: {self.category}",
                 font=("Arial", 18, "italic"),
                 fg="white",
                 bg=bg_color).pack(pady=5)

        tk.Label(self.root,
                 text=f"Pregunta {self.question_count} de {len(self.questions)}",
                 font=("Arial", 18),
                 fg="white",
                 bg=bg_color).pack(pady=5)

        tk.Label(self.root,
                 text=f"Puntos: {self.score}",
                 font=("Arial", 18),
                 fg="white",
                 bg=bg_color).pack(pady=5)

        tk.Label(self.root,
                 text=question,
                 font=("Arial", 28, "bold"),
                 wraplength=1000,
                 fg="white",
                 bg=bg_color).pack(pady=40)

        for i, option in enumerate(options):
            tk.Button(self.root,
                      text=f"{i+1}. {option}",
                      font=("Arial", 20, "bold"),
                      bg=self.option_colors[i % len(self.option_colors)],
                      fg="black",
                      width=30,
                      command=lambda opt=option: self.check_answer(opt)
                     ).pack(pady=10)

        # Atajos de teclado
        for idx in range(len(options)):
            key = str(idx + 1)
            self.root.bind(key, lambda e, opt=options[idx]: self.check_answer(opt))

    def check_answer(self, selected_option):
        _, _, correct_answer = self.current_question
        if selected_option == correct_answer:
            self.score += 1
            self.next_question()
        else:
            clear_window(self.root)
            self.root.config(bg="black")
            tk.Label(self.root,
                     text="❌ ERROR ❌",
                     font=("Arial", 40, "bold"),
                     fg="red",
                     bg="black"
                    ).place(relx=0.5, rely=0.5, anchor="center")
            self.root.after(1000, self.show_menu)

    def show_result(self):
        clear_window(self.root)
        self.root.config(bg="black")
        result_text = f"🎉 Fin del juego 🎉\nPuntaje final: {self.score}/{len(self.questions)}"
        label = tk.Label(self.root,
                         text=result_text,
                         font=("Arial", 32, "bold"),
                         bg="black")
        label.pack(pady=100)

        colors = itertools.cycle(["red", "blue", "green", "orange", "purple", "pink"])
        def animate():
            label.config(fg=next(colors))
            self.root.after(500, animate)
        animate()

        tk.Button(self.root,
                  text="Volver al Menú",
                  font=("Arial", 20),
                  command=self.show_menu).pack(pady=20)
