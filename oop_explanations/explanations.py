EXPLANATIONS = """
OOP Concepts Used (Where & Why)

1) Multiple Inheritance:
   - AppWindow inherits from both tkinter.Tk and HistoryMixin.
   - Reason: Combine GUI window behavior (Tk) with shared history features (Mixin) cleanly.

2) Multiple Decorators:
   - Actions (Run buttons) are decorated with @log_action and @guard_ui_errors.
   - Reason: Separation of concerns for logging and error handling without cluttering core logic.

3) Encapsulation:
   - BaseModel keeps its model_id private via a double-underscore and exposes it via a read-only property.
   - Reason: Control access to internal state and provide a stable interface.

4) Polymorphism:
   - BaseModel defines a common interface (process, get_info).
   - TextSummarizerModel and ImageClassifierModel override process/get_info with task-specific behavior.
   - Reason: GUI calls model.process(data) without knowing the concrete model type.

5) Method Overriding:
   - Child models override BaseModel.get_info() to provide richer, model-specific details.
   - Reason: Customize behavior per subclass while keeping a shared contract.
"""