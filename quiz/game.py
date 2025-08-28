# quiz/game.py

import random
import itertools
import tkinter as tk
import tkinter.messagebox as mb

from .config import CATEGORY_COLORS, OPTION_COLORS, NUM_QUESTIONS_PER_GAME
from .data import categories
from .utils import clear_window

class QuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Preguntas")
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda e: self.exit_or_menu())

        self.score            = 0
        self.question_count   = 0
        self.current_question = None
        self.questions        = []

        self.category_colors = CATEGORY_COLORS
        self.option_colors   = OPTION_COLORS
        self.categories      = categories

        self.show_menu()

    def exit_or_menu(self):
        if getattr(self, 'in_menu', False):
            self.root.destroy()

    def show_menu(self):
        # Cancela cualquier animación pendiente para evitar callbacks
        if hasattr(self, '_after_id'):
            self.root.after_cancel(self._after_id)

        clear_window(self.root)
        self.in_menu        = True
        self.score          = 0
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

        preguntas_disponibles = self.categories.get(category, [])
        num_a_mostrar         = min(len(preguntas_disponibles),
                                    NUM_QUESTIONS_PER_GAME)

        if num_a_mostrar == 0:
            mb.showerror("Sin preguntas",
                         f"No hay preguntas disponibles para “{category}”.")
            self.show_menu()
            return

        self.questions      = random.sample(preguntas_disponibles, num_a_mostrar)
        self.question_count = 0
        self.score          = 0
        self.next_question()

    def next_question(self):
        if self.question_count >= len(self.questions):
            return self.show_result()

        self.current_question = self.questions[self.question_count]
        self.question_count  += 1
        self.show_question()

    def show_question(self):
        clear_window(self.root)
        pregunta, opciones, respuesta = self.current_question
        bg_color                     = self.category_colors[self.category]
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
                 text=pregunta,
                 font=("Arial", 28, "bold"),
                 wraplength=1000,
                 fg="white",
                 bg=bg_color).pack(pady=40)

        for i, opción in enumerate(opciones):
            tk.Button(self.root,
                      text=f"{i+1}. {opción}",
                      font=("Arial", 20, "bold"),
                      bg=self.option_colors[i % len(self.option_colors)],
                      fg="black",
                      width=30,
                      command=lambda opt=opción: self.check_answer(opt)
                     ).pack(pady=10)

        # Atajos de teclado para las opciones
        # Primero, limpamos cualquier bind previo de teclas 1–4
        for key in ("1", "2", "3", "4"):
            self.root.unbind(key)

        for idx in range(len(opciones)):
            tecla = str(idx + 1)
            self.root.bind(tecla,
                           lambda e, opt=opciones[idx]: self.check_answer(opt))

    def check_answer(self, selected_option):
        _, _, correcta = self.current_question
        if selected_option == correcta:
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
        resultado = f"🎉 Fin del juego 🎉\nPuntaje final: {self.score}/{len(self.questions)}"
        label = tk.Label(self.root,
                         text=resultado,
                         font=("Arial", 32, "bold"),
                         bg="black")
        label.pack(pady=100)

        colores = itertools.cycle([
            "red", "blue", "green", "orange", "purple", "pink"
        ])

        def animar():
            # Si el widget ya no existe, cortamos la animación
            if not label.winfo_exists():
                return
            label.config(fg=next(colores))
            # guardamos el after_id para poder cancelarlo al volver al menú
            self._after_id = self.root.after(500, animar)

        animar()

        tk.Button(self.root,
                  text="Volver al Menú",
                  font=("Arial", 20),
                  command=self.show_menu).pack(pady=20)
