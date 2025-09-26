import os
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
from utils.decorators import log_action, guard_ui_errors
from models.text_summarizer import TextSummarizerModel
from models.image_classifier import ImageClassifierModel
from .model_info_frame import ModelInfoFrame
from oop_explanations.explanations import EXPLANATIONS

# --- Mixin demonstrating multiple inheritance + encapsulation of history ---
class HistoryMixin:
    def __init__(self):
        self.__history = []  # private history list

    def _add_history(self, entry: str):
        self.__history.append(entry)

    @property
    def history(self):
        return tuple(self.__history)  # read-only tuple view


class AppWindow(tk.Tk, HistoryMixin):   # multiple inheritance here
    def __init__(self):
        tk.Tk.__init__(self)
        HistoryMixin.__init__(self)
        self.title("HIT137 – Tkinter + HuggingFace (OOP)")
        self.geometry("980x680")

        self._build_models()
        self._build_ui()

    def _build_models(self):
        # Pre-instantiate default models
        self.text_model = TextSummarizerModel()             # NLP
        self.vision_model = ImageClassifierModel()          # Vision

        # model registry for dropdown selection (task_name -> instance)
        self.models_by_task = {
            "Text Summarization": self.text_model,
            "Image Classification": self.vision_model,
        }

    def _build_ui(self):
        # --- Top controls: task selection + model info ---
        top = ttk.Frame(self)
        top.pack(fill="x", padx=8, pady=8)

        ttk.Label(top, text="Task:").pack(side="left")
        self.task_var = tk.StringVar(value="Text Summarization")
        self.task_sel = ttk.Combobox(top, textvariable=self.task_var, state="readonly",
                                     values=list(self.models_by_task.keys()), width=28)
        self.task_sel.pack(side="left", padx=8)
        self.task_sel.bind("<<ComboboxSelected>>", self._on_task_change)

        self.model_info = ModelInfoFrame(self)
        self.model_info.pack(side="right", padx=8, pady=8)

        # --- Input area ---
        mid = ttk.Frame(self)
        mid.pack(fill="both", expand=True, padx=8, pady=4)

        input_box = ttk.LabelFrame(mid, text="Input")
        input_box.pack(side="left", fill="both", expand=True, padx=4, pady=4)

        self.input_type = tk.StringVar(value="Text")
        ttk.Radiobutton(input_box, text="Text", variable=self.input_type, value="Text",
                        command=self._refresh_input).pack(anchor="w")
        ttk.Radiobutton(input_box, text="Image", variable=self.input_type, value="Image",
                        command=self._refresh_input).pack(anchor="w")

        self.text_input = scrolledtext.ScrolledText(input_box, width=60, height=12, wrap=tk.WORD)
        self.text_input.pack(fill="both", expand=True, padx=2, pady=6)

        self.file_frame = ttk.Frame(input_box)  # appears for images
        self.file_path_var = tk.StringVar(value="")
        ttk.Entry(self.file_frame, textvariable=self.file_path_var, width=54).pack(side="left", padx=4)
        ttk.Button(self.file_frame, text="Browse", command=self._browse_img).pack(side="left")

        # --- Output area ---
        out_box = ttk.LabelFrame(mid, text="Output")
        out_box.pack(side="left", fill="both", expand=True, padx=4, pady=4)

        self.output = scrolledtext.ScrolledText(out_box, width=60, height=18, wrap=tk.WORD, state="disabled")
        self.output.pack(fill="both", expand=True, padx=2, pady=6)

        # --- Actions ---
        btns = ttk.Frame(self)
        btns.pack(fill="x", padx=8, pady=8)
        ttk.Button(btns, text="Run Selected Task", command=self._run_selected).pack(side="left")
        ttk.Button(btns, text="Clear Output", command=self._clear_output).pack(side="left", padx=8)

        # --- OOP Explanations ---
        expl = ttk.LabelFrame(self, text="OOP Explanations (Where & Why)")
        expl.pack(fill="both", expand=False, padx=8, pady=8)
        self.expl_text = scrolledtext.ScrolledText(expl, height=10, wrap=tk.WORD, state="normal")
        self.expl_text.insert(tk.END, EXPLANATIONS.strip())
        self.expl_text.configure(state="disabled")
        self._show_current_model_info()

        self._refresh_input()

    def _browse_img(self):
        path = filedialog.askopenfilename(title="Select an image",
                                          filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.webp"), ("All files", "*.*")])
        if path:
            self.file_path_var.set(path)

    def _refresh_input(self):
        # toggle text box vs. file picker
        itype = self.input_type.get()
        if itype == "Text":
            self.file_frame.pack_forget()
            self.text_input.pack(fill="both", expand=True, padx=2, pady=6)
        else:
            self.text_input.pack_forget()
            self.file_frame.pack(fill="x", padx=2, pady=6)

    def _on_task_change(self, _evt=None):
        self._show_current_model_info()

    def _show_current_model_info(self):
        model = self.models_by_task[self.task_var.get()]
        self.model_info.set_info(model.get_info())

    def _write_output(self, text: str):
        self.output.configure(state="normal")
        self.output.insert(tk.END, text + "\n")
        self.output.configure(state="disabled")
        self.output.see(tk.END)

    def _clear_output(self):
        self.output.configure(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.configure(state="disabled")

    # --- Multiple decorators applied to a single handler ---
    @log_action("Run Selected Task")
    @guard_ui_errors(messagebox)
    def _run_selected(self):
        task = self.task_var.get()
        model = self.models_by_task[task]

        if task == "Text Summarization":
            data = self.text_input.get("1.0", tk.END).strip()
            result = model.process(data)    # polymorphic call
            self._write_output(f"[Summary]\n{result}")
            self._add_history("Ran text summarization.")
        else:
            path = self.file_path_var.get().strip()
            if not path or not os.path.exists(path):
                raise FileNotFoundError("Please choose a valid image file.")
            result = model.process(path)    # polymorphic call
            self._write_output(f"[Image Top-3]\n{result}")
            self._add_history("Ran image classification.")