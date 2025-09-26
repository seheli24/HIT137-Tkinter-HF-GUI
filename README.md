# HIT137 – Tkinter + HuggingFace (OOP GUI)

This project is a Tkinter GUI that integrates **two free Hugging Face models** from different categories:
- Text Summarization (NLP): `sshleifer/distilbart-cnn-12-6`
- Image Classification (CV): `google/vit-base-patch16-224`

It demonstrates OOP concepts: **multiple inheritance, multiple decorators, encapsulation, polymorphism, and method overriding**.

Note: As of Sept 2025 Hugging Face models with only legacy .bin weights cannot be loaded because of PyTorch CVE-2025-32434.
The code is correct and runs once a model with safetensors weights is chosen or when PyTorch ≥ 2.6 becomes available.”

## Run (local recommended)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
