import functools
import traceback

def log_action(action_name: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"[LOG] {action_name} started.")
            result = func(*args, **kwargs)
            print(f"[LOG] {action_name} completed.")
            return result
        return wrapper
    return decorator

def guard_ui_errors(messagebox):
    """Catch exceptions and show a Tkinter messagebox, if available."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                traceback.print_exc()
                try:
                    messagebox.showerror("Error", str(e))
                except Exception:
                    # fallback when no messagebox context (e.g., headless)
                    print(f"[ERROR] {e}")
                return None
        return wrapper
    return decorator