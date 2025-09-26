from transformers import pipeline
from PIL import Image
from .base import BaseModel

class ImageClassifierModel(BaseModel):
    def __init__(self, model_id: str = "google/vit-base-patch16-224"):
        super().__init__(task_name="image-classification", model_id=model_id)
        self._pipe = pipeline("image-classification", model=model_id)

    def process(self, data: str):
        # data is image path
        img = Image.open(data).convert("RGB")
        preds = self._pipe(img)
        # return top-3 friendly string
        top = preds[:3]
        lines = [f"{i+1}. {p['label']} ({p['score']:.3f})" for i, p in enumerate(top)]
        return "\n".join(lines)

    def get_info(self) -> str:
        base = super().get_info()
        return base + (
            "Category: CV (Vision)\n"
            "Description: Predicts classes for an input image.\n"
            "Input: Image file path\nOutput: Top predictions with scores\n"
        )