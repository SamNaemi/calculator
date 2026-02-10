import tkinter as tk


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.resizable(False, False)

        self.display_text = tk.StringVar(value="0")

        container = tk.Frame(self)
        container.pack(padx=15, pady=15)

        display = tk.Label(
            container,
            textvariable=self.display_text,
            anchor="e",
            font=("Arial", 30),
            bg="white",
            relief="sunken",
            width=16,
            padx=10,
            pady=12,
        )
        display.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(0, 10))

        button_font = ("Arial", 24)
        button_symbol_font = ("Arial", 24)

        buttons = [
            ("%", 1, 0, button_font),
            ("CE", 1, 1, button_font),
            ("C", 1, 2, button_font),
            ("⌫", 1, 3, button_symbol_font),
            ("1/x", 2, 0, button_font),
            ("x²", 2, 1, button_symbol_font),
            ("√x", 2, 2, button_symbol_font),
            ("/", 2, 3, button_font),
            ("7", 3, 0, button_font),
            ("8", 3, 1, button_font),
            ("9", 3, 2, button_font),
            ("×", 3, 3, button_symbol_font),
            ("4", 4, 0, button_font),
            ("5", 4, 1, button_font),
            ("6", 4, 2, button_font),
            ("−", 4, 3, button_symbol_font),
            ("1", 5, 0, button_font),
            ("2", 5, 1, button_font),
            ("3", 5, 2, button_font),
            ("+", 5, 3, button_font),
            ("±", 6, 0, button_symbol_font),
            ("0", 6, 1, button_font),
            (".", 6, 2, button_font),
            ("=", 6, 3, button_font),
        ]

        for text, row, column, font in buttons:
            tk.Button(
                container,
                text=text,
                font=font,
                height=2,
                width=4,
                command=lambda value=text: self.on_button_press(value),
            ).grid(row=row, column=column)

        self.center_window()

    def on_button_press(self, value: str) -> None:
        current = self.display_text.get()

        if value in {"C", "CE"}:
            self.display_text.set("0")
            return

        if value == "⌫":
            next_value = current[:-1] if current and current != "0" else ""
            self.display_text.set(next_value if next_value else "0")
            return

        if value == "=":
            return

        if current == "0":
            self.display_text.set(value)
            return

        self.display_text.set(f"{current}{value}")

    def center_window(self) -> None:
        self.update_idletasks()  # Ensure size info is correct

        window_width = self.winfo_width()
        window_height = self.winfo_height()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2) - 150

        self.geometry(f"+{x}+{y}")


if __name__ == "__main__":
    Calculator().mainloop()
