# quiz/utils.py

def clear_window(root):
    """
    Elimina todos los widgets hijos de la ventana Tk.
    """
    for widget in root.winfo_children():
        widget.destroy()
