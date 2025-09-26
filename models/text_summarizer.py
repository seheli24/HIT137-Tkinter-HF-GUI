from transformers import pipeline
from .base import BaseModel

class TextSummarizerModel(BaseModel):
    def __init__(self, model_id: str = "sshleifer/distilbart-cnn-12-6"):
        super().__init__(task_name="summarization", model_id=model_id)
        # lazy init is fine; for simplicity, load here
        self._pipe = pipeline("summarization", model=model_id)

    def process(self, data: str) -> str:
        if not isinstance(data, str) or not data.strip():
            raise ValueError("Expected non-empty text for summarization.")
        out = self._pipe(data, max_length=80, min_length=25, do_sample=False)
        return out[0]["summary_text"]

    def get_info(self) -> str:
        base = super().get_info()
        return base + (
            "Category: NLP (Text)\n"
            "Description: Summarizes long text into concise form.\n"
            "Input: Plain text\nOutput: Summary text\n"
        )