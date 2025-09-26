import tkinter as tk
from tkinter import scrolledtext

class ModelInfoFrame(tk.LabelFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, text="Model Info", padx=6, pady=6, **kwargs)
        self.text = scrolledtext.ScrolledText(self, width=48, height=10, wrap=tk.WORD)
        self.text.pack(fill="both", expand=True)

    def set_info(self, info: str):
        self.text.configure(state="normal")
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, info or "(No model selected)")
        self.text.configure(state="disabled")