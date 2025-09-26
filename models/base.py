from abc import ABC, abstractmethod

class BaseModel(ABC):
    """Common interface for all models; demonstrates polymorphism via process()."""

    def __init__(self, task_name: str, model_id: str):
        self._task_name = task_name           # encapsulation (protected-ish)
        self.__model_id = model_id            # encapsulation (private)

    @property
    def model_id(self) -> str:
        # read-only property as an example of encapsulation
        return self.__model_id

    @abstractmethod
    def process(self, data):
        """Run inference on the input data and return output."""
        raise NotImplementedError

    def get_info(self) -> str:
        """Method intended to be overridden by subclasses."""
        return f"Task: {self._task_name}\nModel: {self.__model_id}\n"