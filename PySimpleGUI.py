"""Tiny PySimpleGUI compatibility layer for this project.

This implements only the subset used by Multiverse.py and CA_Multiverse.py.
It exists because the public PyPI PySimpleGUI package is now a redirect stub.
"""

import tkinter as tk
from tkinter import ttk


WINDOW_CLOSED = "__WINDOW_CLOSED__"


class _Element:
    def __init__(self, key=None):
        self.key = key
        self.widget = None
        self.var = None

    def update(self, value=None, values=None, **kwargs):
        if values is not None and hasattr(self.widget, "configure"):
            try:
                self.widget.configure(values=[str(item) for item in values])
            except tk.TclError:
                pass
        if value is not None:
            self.set(value)

    def get(self):
        if self.var is None:
            return None
        return self.var.get()

    def set(self, value):
        if self.var is not None:
            self.var.set(value)

    def build(self, parent, window):
        raise NotImplementedError


class Text(_Element):
    def __init__(self, text="", tooltip=None, **kwargs):
        super().__init__(kwargs.get("key"))
        self.text = text
        self.tooltip = tooltip

    def build(self, parent, window):
        self.widget = ttk.Label(parent, text=self.text)
        return self.widget


class Input(_Element):
    def __init__(self, default_text="", key=None, **kwargs):
        super().__init__(key)
        self.default_text = default_text

    def build(self, parent, window):
        self.var = tk.StringVar(value=str(self.default_text))
        self.widget = ttk.Entry(parent, textvariable=self.var, width=18)
        return self.widget


class Checkbox(_Element):
    def __init__(self, text="", default=False, key=None, tooltip=None, **kwargs):
        super().__init__(key)
        self.text = text
        self.default = bool(default)

    def build(self, parent, window):
        self.var = tk.BooleanVar(value=self.default)
        self.widget = ttk.Checkbutton(parent, text=self.text, variable=self.var)
        return self.widget


class Combo(_Element):
    def __init__(self, values=(), default_value="", size=None, enable_events=False, key=None, **kwargs):
        super().__init__(key)
        self.values = list(values)
        self.default_value = default_value
        self.enable_events = enable_events
        self.size = size

    def build(self, parent, window):
        self.var = tk.StringVar(value=str(self.default_value))
        width = self.size[0] if self.size else 24
        self.widget = ttk.Combobox(parent, textvariable=self.var, values=[str(item) for item in self.values], width=width)
        if self.enable_events and self.key is not None:
            self.widget.bind("<<ComboboxSelected>>", lambda event: window._push_event(self.key))
        return self.widget


class Button(_Element):
    def __init__(self, button_text="", key=None, **kwargs):
        super().__init__(key or button_text)
        self.button_text = button_text

    def build(self, parent, window):
        self.widget = ttk.Button(parent, text=self.button_text, command=lambda: window._push_event(self.key))
        return self.widget


class Slider(_Element):
    def __init__(self, range=(0, 100), default_value=0, resolution=1, orientation="h", key=None, size=None, **kwargs):
        super().__init__(key)
        self.range = range
        self.default_value = default_value
        self.resolution = resolution
        self.orientation = orientation
        self.size = size

    def build(self, parent, window):
        self.var = tk.DoubleVar(value=float(self.default_value))
        orient = tk.HORIZONTAL if self.orientation.lower().startswith("h") else tk.VERTICAL
        length = 260 if not self.size else max(120, self.size[0] * 4)
        self.widget = ttk.Scale(parent, from_=self.range[0], to=self.range[1], orient=orient, variable=self.var, length=length)
        return self.widget


class Spin(_Element):
    def __init__(self, values=(), initial_value=None, key=None, tooltip=None, **kwargs):
        super().__init__(key)
        self.values = list(values)
        self.initial_value = initial_value if initial_value is not None else (self.values[0] if self.values else "")

    def build(self, parent, window):
        self.var = tk.StringVar(value=str(self.initial_value))
        self.widget = ttk.Spinbox(parent, values=[str(item) for item in self.values], textvariable=self.var, width=8)
        return self.widget


class Window:
    def __init__(self, title, layout, **kwargs):
        self.title = title
        self.layout = layout
        self.elements = {}
        self._event = None
        self.root = tk.Tk()
        self.root.title(title)
        self.root.protocol("WM_DELETE_WINDOW", lambda: self._push_event(WINDOW_CLOSED))

        outer = ttk.Frame(self.root)
        outer.pack(fill="both", expand=True)
        canvas = tk.Canvas(outer, highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        self.frame = ttk.Frame(canvas)
        self.frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for row_index, row in enumerate(layout):
            for col_index, element in enumerate(row):
                if isinstance(element, str):
                    element = Text(element)
                widget = element.build(self.frame, self)
                widget.grid(row=row_index, column=col_index, padx=4, pady=3, sticky="w")
                if element.key is not None:
                    self.elements[element.key] = element

    def __getitem__(self, key):
        return self.elements[key]

    def _push_event(self, event):
        self._event = event
        self.root.quit()

    def _values(self):
        return {key: element.get() for key, element in self.elements.items() if element.var is not None}

    def Read(self):
        self._event = None
        self.root.mainloop()
        return self._event, self._values()

    read = Read

    def close(self):
        try:
            self.root.destroy()
        except tk.TclError:
            pass

