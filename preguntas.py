import tkinter as tk
import random
import itertools

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

        # Colores para cada categoría
        self.category_colors = {
            "Historia": "#FF8C61",
            "Ciencia": "#61FF8C",
            "Deportes": "#618CFF",
            "Arte": "#FF61C3",
            "Tecnología": "#FFC361",
            "Sistemas": "#61FFF3"
        }

        # Colores para los botones
        self.option_colors = ["#FFB347", "#47FFB3", "#B347FF", "#FF4747"]

        # Preguntas por categoría 
        self.categories = {
            "Historia": [
                ("¿Quién fue el primer presidente de Argentina?", ["Rivadavia", "Belgrano", "San Martín", "Sarmiento"], "Rivadavia"),
                ("¿En qué año llegó Cristóbal Colón a América?", ["1492", "1500", "1453", "1520"], "1492"),
                ("¿Qué imperio construyó las pirámides?", ["Egipto", "Roma", "China", "Inca"], "Egipto"),
                ("¿Quién cruzó los Andes con su ejército?", ["San Martín", "Belgrano", "Artigas", "Bolívar"], "San Martín"),
                ("¿Dónde nació Napoleón Bonaparte?", ["Córcega", "París", "Roma", "Madrid"], "Córcega"),
                ("¿Qué guerra terminó en 1945?", ["Primera Guerra Mundial", "Guerra de Vietnam", "Segunda Guerra Mundial", "Guerra Fría"], "Segunda Guerra Mundial"),
                ("¿Qué civilización inventó la escritura cuneiforme?", ["Egipcios", "Fenicios", "Sumerios", "Mayas"], "Sumerios"),
                ("¿Quién fue Eva Perón?", ["Primera dama", "Presidenta", "Docente", "Escritora"], "Primera dama"),
                ("¿Qué país fue descubierto por Vasco da Gama?", ["India", "Brasil", "México", "Chile"], "India"),
                ("¿Qué muralla es visible desde el espacio?", ["Muralla China", "Murallas de Ávila", "Muralla de Adriano", "Ninguna"], "Muralla China")
            ],
            "Ciencia": [
                ("¿Cuál es el planeta más grande del sistema solar?", ["Tierra", "Marte", "Júpiter", "Saturno"], "Júpiter"),
                ("¿Qué gas respiramos para vivir?", ["Oxígeno", "Nitrógeno", "Hidrógeno", "Dióxido de carbono"], "Oxígeno"),
                ("¿Cuál es el metal más liviano?", ["Oro", "Plata", "Litio", "Hierro"], "Litio"),
                ("¿Qué estudia la biología?", ["Animales", "La vida", "El espacio", "Los átomos"], "La vida"),
                ("¿Qué científico propuso la teoría de la relatividad?", ["Newton", "Einstein", "Tesla", "Darwin"], "Einstein"),
                ("¿Qué parte del cuerpo bombea la sangre?", ["Pulmones", "Corazón", "Hígado", "Cerebro"], "Corazón"),
                ("¿Cuál es el hueso más largo del cuerpo?", ["Fémur", "Húmero", "Radio", "Tibia"], "Fémur"),
                ("¿Qué planeta es conocido como el planeta rojo?", ["Venus", "Júpiter", "Marte", "Saturno"], "Marte"),
                ("¿Cuál es el órgano encargado de filtrar la sangre?", ["Riñones", "Pulmones", "Hígado", "Corazón"], "Riñones"),
                ("¿Qué animal pone huevos?", ["Perro", "Vaca", "Gallina", "Gato"], "Gallina")
            ],
            "Deportes": [
                ("¿Cuántos jugadores hay en un equipo de fútbol?", ["9", "10", "11", "12"], "11"),
                ("¿En qué deporte se usa una raqueta?", ["Básquet", "Tenis", "Fútbol", "Boxeo"], "Tenis"),
                ("¿Dónde se originaron los Juegos Olímpicos?", ["Roma", "Atenas", "París", "Berlín"], "Atenas"),
                ("¿Qué selección ganó el mundial 2022?", ["Brasil", "Argentina", "Francia", "Alemania"], "Argentina"),
                ("¿Qué deporte practicaba Michael Jordan?", ["Básquet", "Tenis", "Fútbol", "Boxeo"], "Básquet"),
                ("¿Qué país inventó el judo?", ["China", "Japón", "Corea", "India"], "Japón"),
                ("¿Cuántos sets necesita ganar un jugador de tenis para llevarse un partido (hombres Grand Slam)?", ["2", "3", "4", "5"], "3"),
                ("¿Qué deporte se juega en Wimbledon?", ["Tenis", "Golf", "Críquet", "Hockey"], "Tenis"),
                ("¿Qué selección ganó el mundial de 2010?", ["España", "Italia", "Francia", "Argentina"], "España"),
                ("¿Qué deporte se practica en la NBA?", ["Tenis", "Básquet", "Fútbol", "Vóley"], "Básquet")
            ],
            "Arte": [
                ("¿Quién pintó la Mona Lisa?", ["Picasso", "Da Vinci", "Van Gogh", "Miguel Ángel"], "Da Vinci"),
                ("¿Qué instrumento musical tiene teclas blancas y negras?", ["Piano", "Violín", "Guitarra", "Flauta"], "Piano"),
                ("¿Qué famoso pintor se cortó una oreja?", ["Van Gogh", "Dalí", "Rembrandt", "Goya"], "Van Gogh"),
                ("¿En qué país nació Pablo Picasso?", ["Italia", "Francia", "España", "Alemania"], "España"),
                ("¿Qué arte se relaciona con Shakespeare?", ["Pintura", "Música", "Teatro", "Escultura"], "Teatro"),
                ("¿Cuál es el baile típico de Argentina?", ["Tango", "Samba", "Cueca", "Flamenco"], "Tango"),
                ("¿Qué estilo artístico es Salvador Dalí?", ["Surrealismo", "Cubismo", "Impresionismo", "Realismo"], "Surrealismo"),
                ("¿Qué instrumento tocaba Mozart?", ["Piano", "Guitarra", "Violín", "Batería"], "Piano"),
                ("¿Qué escultura famosa está en Río de Janeiro?", ["David", "Cristo Redentor", "Venus", "Moái"], "Cristo Redentor"),
                ("¿Qué pintor pintó 'La noche estrellada'?", ["Da Vinci", "Van Gogh", "Picasso", "Goya"], "Van Gogh")
            ],
            "Tecnología": [
                ("¿Qué significa CPU?", ["Central Processing Unit", "Computer Personal Unit", "Control Program Utility", "Central Power Unit"], "Central Processing Unit"),
                ("¿Qué empresa creó Windows?", ["Apple", "Microsoft", "Google", "IBM"], "Microsoft"),
                ("¿Qué lenguaje se usa para páginas web?", ["Python", "C++", "HTML", "Java"], "HTML"),
                ("¿Qué es un byte?", ["8 bits", "4 bits", "2 bits", "16 bits"], "8 bits"),
                ("Cuál es el sistema operativo de Apple?", ["Linux", "iOS", "Windows", "Android"], "iOS"),
                ("¿Qué es la nube en informática?", ["Un satélite", "Un disco duro", "Almacenamiento en internet", "Una red local"], "Almacenamiento en internet"),
                ("¿Qué significa URL?", ["Universal Resource Locator", "Uniform Resource Locator", "United Resource Locator", "User Random Link"], "Uniform Resource Locator"),
                ("¿Qué empresa creó el buscador Chrome?", ["Yahoo", "Google", "Bing", "Microsoft"], "Google"),
                ("¿Qué es un algoritmo?", ["Un programa", "Un conjunto de instrucciones", "Un lenguaje", "Un chip"], "Un conjunto de instrucciones"),
                ("¿Qué significa RAM?", ["Read Access Memory", "Random Access Memory", "Run Access Module", "Random Active Memory"], "Random Access Memory")
            ],
            "Sistemas": [
                ("¿Qué es un algoritmo?", ["Un programa", "Un conjunto de pasos", "Un lenguaje", "Un virus"], "Un conjunto de pasos"),
                ("¿Qué significa POO?", ["Programación Orientada a Objetos", "Programa Operativo Online", "Proceso Ordenado Óptimo", "Programación Original Ofuscada"], "Programación Orientada a Objetos"),
                ("¿Qué es un diagrama de flujo?", ["Un gráfico de datos", "Un esquema de pasos", "Una tabla", "Un dibujo libre"], "Un esquema de pasos"),
                ("¿Qué significa UML?", ["Unified Modeling Language", "Universal Machine Logic", "Unidad Modular de Lenguaje", "User Modeling Line"], "Unified Modeling Language"),
                ("¿Qué es un bug en programación?", ["Un error", "Un virus", "Un archivo", "Un compilador"], "Un error"),
                ("¿Qué es un compilador?", ["Un editor de texto", "Un programa que traduce código", "Un virus", "Una base de datos"], "Un programa que traduce código"),
                ("¿Qué es un ciclo for?", ["Un bucle", "Una variable", "Una función", "Un error"], "Un bucle"),
                ("¿Qué significa SQL?", ["Structured Query Language", "Simple Query Line", "System Query Logic", "Server Queue Language"], "Structured Query Language"),
                ("¿Qué es un sistema operativo?", ["Un software", "Un hardware", "Un virus", "Un periférico"], "Un software"),
                ("¿Qué significa CASE?", ["Computer Aided Software Engineering", "Central Automated System Engineering", "Computer Advanced Server Edition", "Code And Script Editor"], "Computer Aided Software Engineering")
            ]
        }

        self.show_menu()

    def exit_or_menu(self):
        if hasattr(self, 'in_menu') and self.in_menu:
            self.root.destroy()

    def show_menu(self):
        self.clear_window()
        self.in_menu = True
        self.score = 0
        self.question_count = 0

        tk.Label(self.root, text="🎮 Juego de Preguntas 🎮", font=("Arial", 36, "bold"), fg="white", bg="darkblue").pack(fill="x", pady=20)
        tk.Label(self.root, text="Selecciona una categoría", font=("Arial", 24), fg="black").pack(pady=20)

        for category in self.categories.keys():
            tk.Button(self.root, text=category, font=("Arial", 20, "bold"),
                      bg=self.category_colors[category], fg="white", width=20, height=2,
                      command=lambda c=category: self.start_game(c)).pack(pady=10)

    def start_game(self, category):
        self.in_menu = False
        self.category = category
        self.questions = random.sample(self.categories[category], 5)
        self.question_count = 0
        self.next_question()

    def next_question(self):
        if self.question_count >= len(self.questions):
            self.show_result()
            return

        self.current_question = self.questions[self.question_count]
        self.question_count += 1
        self.show_question()

    def show_question(self):
        self.clear_window()
        question, options, answer = self.current_question

        # Fondo colorido según categoría
        self.root.config(bg=self.category_colors[self.category])

        tk.Label(self.root, text=f"Categoría: {self.category}", font=("Arial", 18, "italic"), fg="white", bg=self.category_colors[self.category]).pack(pady=5)
        tk.Label(self.root, text=f"Pregunta {self.question_count} de {len(self.questions)}", font=("Arial", 18), fg="white", bg=self.category_colors[self.category]).pack(pady=5)
        tk.Label(self.root, text=f"Puntos: {self.score}", font=("Arial", 18), fg="white", bg=self.category_colors[self.category]).pack(pady=5)

        tk.Label(self.root, text=question, font=("Arial", 28, "bold"), wraplength=1000, fg="white", bg=self.category_colors[self.category]).pack(pady=40)

        for i, option in enumerate(options):
            btn = tk.Button(self.root, text=f"{i+1}. {option}", font=("Arial", 20, "bold"),
                            bg=self.option_colors[i % len(self.option_colors)], fg="black", width=30,
                            command=lambda opt=option: self.check_answer(opt))
            btn.pack(pady=10)

        self.root.bind("1", lambda e: self.check_answer(options[0]))
        self.root.bind("2", lambda e: self.check_answer(options[1]))
        self.root.bind("3", lambda e: self.check_answer(options[2]))
        self.root.bind("4", lambda e: self.check_answer(options[3]))

    def check_answer(self, selected_option):
        _, _, correct_answer = self.current_question
        if selected_option == correct_answer:
            self.score += 1
            self.next_question()
        else:
            # ERROR y volver al menú
            self.clear_window()
            self.root.config(bg="black")
            error_label = tk.Label(self.root, text="❌ ERROR ❌", font=("Arial", 40, "bold"), fg="red", bg="black")
            error_label.place(relx=0.5, rely=0.5, anchor="center")
            self.root.after(1000, self.show_menu)

    def show_result(self):
        self.clear_window()
        self.root.config(bg="black")
        result_text = f"🎉 Fin del juego 🎉\nPuntaje final: {self.score}/{len(self.questions)}"
        label = tk.Label(self.root, text=result_text, font=("Arial", 32, "bold"), bg="black")
        label.pack(pady=100)

        colors = itertools.cycle(["red", "blue", "green", "orange", "purple", "pink"])
        def animate():
            label.config(fg=next(colors))
            self.root.after(500, animate)
        animate()

        tk.Button(self.root, text="Volver al Menú", font=("Arial", 20), command=self.show_menu).pack(pady=20)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    game = QuizGame(root)
    root.mainloop()
