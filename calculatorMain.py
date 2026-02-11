import tkinter as tk
from decimal import Decimal, InvalidOperation, getcontext

getcontext().prec = 15





class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.resizable(False, False)


        self.tokens: list[str] = []        # e.g. ["12", "+", "3", "*", "4"]
        self.entry: str = ""               # current number being typed, e.g. "3.14"
        self.just_evaluated: bool = False  # if last action was "="

        self.display_text = tk.StringVar(value="0")


        container = tk.Frame(self)
        container.pack(padx=15, pady=15)


        display = tk.Label(container, textvariable=self.display_text, anchor="e", font=("Arial", 30), bg="white", relief="sunken", width=16, padx=10, pady=12)
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
            ("x", 3, 3, button_symbol_font),
            ("4", 4, 0, button_font),
            ("5", 4, 1, button_font),
            ("6", 4, 2, button_font),
            ("-", 4, 3, button_symbol_font),
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
                height=1,
                width=4,
                command=lambda value=text: self.on_button_press(value),
            ).grid(row=row, column=column)


        self._render()
        self.center_window()


# ------------------------------- UI helpers -------------------------------


    def center_window(self) -> None:
        self.update_idletasks()  # Ensure size info is correct

        window_width = self.winfo_width()
        window_height = self.winfo_height()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2) - 150

        self.geometry(f"+{x}+{y}")




    def _render(self) -> None:
        # Always show spaces between tokens, and between tokens and the current entry
        parts = []
        parts.extend(self.tokens)
        if self.entry:
            parts.append(self.entry)
        
        text = " ".join(parts).strip()
        self.display_text.set(text if text else "0")


# ------------------------------- Core input logic ------------------------------- 


    def on_button_press(self, value: str) -> None:
        # Map UI "x" to internal "*"
        if value == "x":
            value = "*"

        if value.isdigit():
            self._press_digit(value)
        elif value == ".":
            self._press_decimal()
        elif value in {"+", "-", "*", "/"}:
            self._press_operator(value)
        elif value == "=":
            self._press_equals()
        elif value == "⌫":
            self._press_backspace()
        elif value == "C":
            self._press_clear_all()
        elif value == "CE":
            self._press_clear_entry()
        elif value == "±":
            self._press_toggle_sign()
        elif value == "%":
            self._press_percent()
        elif value == "1/x":
            self._press_unary("inv")
        elif value == "x²":
            self._press_unary("square")
        elif value == "√x":
            self._press_unary("sqrt")
        
        self._render()


# ------------------------------- Button handlers ------------------------------- 


    def _press_digit(self, d: str) -> None:
        if self.just_evaluated and not self.tokens:
            # start fresh after "=" if user types a digit
            self.entry = ""
            self.just_evaluated = False
        

        if self.entry == "0":
            # replace leading 0
            self.entry = d
        else:
            self.entry += d





    def _press_decimal(self) -> None:
        if self.just_evaluated and not self.tokens:
            self.entry = ""
            self.just_evaluated = False

            if not self.entry:
                self.entry = "0."
            elif "." not in self.entry:
                self.entry += "."





    def _press_operator(self, op: str) -> None:
        # If we just evaluated and user hits an operator, continue from result
        if self.just_evaluated:
            self.just_evaluated = False
        
        # If we have a current number, push it
        if self.entry:
            self.tokens.append(self.entry)
            self.entry = ""
        
        # If tokens are empty, allow leading "-" for negative entry #--------------------------------------------check this one to make sure minus doesn't do minus-------------------------------
        if not self.tokens:
            if op == "-":
                self.entry = "-"
            return
        
        # Replace operator if last token is already an operator
        if self.tokens and self._is_operator(self.tokens[-1]):
            self.tokens[-1] = op
            return
        
        self.tokens.append(op)





    def _press_equals(self) -> None:
        if self.entry:
            self.tokens.append(self.entry)
            self.entry = ""
        
        # If expression ends with an operator, drop it
        if self.tokens and self._is_operator(self.tokens[-1]):
            self.tokens.pop()
        
        if not self.tokens:
            return
        
        try:
            result = self._evaluate_tokens(self.tokens)
        except Exception:
            self._error()
            return
        
        self.tokens = []
        self.entry = self._format_decimal(result)
        self.just_evaluated = True





    def _press_backspace(self) -> None:
        if self.just_evaluated:
            # backspace after = edits the result as an entry
            self.just_evaluated = False
        
        if self.entry:
            self.entry = self.entry[:-1]
            # if entry becomes "-" or empty, clear it
            if self.entry in {"", "-"}:
                self.entry = ""
            return
        
        # No entry: step back through tokens
        if not self.tokens:
            return
        
        last = self.tokens.pop()
        if self._is_operator(last):
            return
        
        # Last was a number; bring it into entry and backspace it
        self.entry = last[:-1]
        if self.entry in {"", "-"}:
            self.entry = ""

        



    def _press_clear_all(self) -> None:
        self.tokens = []
        self.entry = ""
        self.just_evaluated = False
    

    def _press_clear_entry(self) -> None:
        self.entry = ""
        self.just_evaluated = False
    




    def _press_toggle_sign(self) -> None:
        if self.just_evaluated and not self.tokens:
            self.just_evaluated = False
        
        if not self.entry:
            # try to pull last number token into entry
            if self.tokens and not self._is_operator(self.tokens[-1]):
                self.entry = self.tokens.pop()
            else:
                self.entry = "0"
        
        if self.entry.startswith("-"):
            self.entry = self.entry[1:]
        else:
            if self.entry != "0":
                self.entry = "-" + self.entry
        
        # Normalize "-0" -> "0"
        if self.entry in {"-0", "-0.0"}:
            self.entry = "0"
    




    def _press_unary(self, kind: str) -> None:
        # Apply to current entry; if empty, apply to last number token or 0
        if not self.entry:
            if self.tokens and not self._is_operator(self.tokens[-1]):
                self.entry = self.tokens.pop()
            else:
                self.entry = "0"
        
        try:
            x = Decimal(self.entry)
            if kind == "inv":
                if x == 0:
                    raise ZeroDivisionError
                y = Decimal(1) / x
            elif kind == "square":
                y = x * x
            elif kind == "sqrt":
                if x < 0:
                    raise ValueError
                y = x.sqrt()
            else:
                return
        except Exception:
            self._error()
            return
        
        self.entry = self._format_decimal(y)
        self.just_evaluated = False
    




    def _press_percent(self) -> None:
        """
        Approximate Windows-style percent:
        - If we have "A op B", then:
        - For + or - : B becomes (A * (B / 100))
        - For * or / : B becomes (B / 100)
        - Otherwise just divide current by 100.
        """
        # Ensure we have an entry to percent-ify
        if not self.entry:
            if self.tokens and not self._is_operator(self.tokens[-1]):
                self.entry = self.tokens.pop()
            else:
                self.entry = "0"
        
        try:
            b = Decimal(self.entry)
        except InvalidOperation:
            self._error()
            return
        
        # Find pattern: [A, op] at the end of tokens
        if len(self.tokens) >= 2 and (not self._is_operator(self.tokens[-2])) and self._is_operator(self.tokens[-1]):
            try:
                a = Decimal(self.tokens[-2])
            except InvalidOperation:
                self._error()
                return
            op = self.tokens[-1]
            if op in {"+", "-"}:
                b = a * b / Decimal(100)
            else:
                b = b / Decimal(100)
        else:
            b = b / Decimal(100)
        
        self.entry = self._format_decimal(b)
        self.just_evaluated = False


    # ------------------------------- Evaluation (safe, no eval) ------------------------------- 
    def _evaluate_tokens(self, tokens: list[str]) -> Decimal:
        """
        Shunting-yard -> RPN -> evaluate with Decimal.
        Supports + - * /
        tokens are like ["12", "+", "3", "*", "4"]
        """
        # Convert display-only "*" ok; already internal
        precedence = {"+": 1, "-": 1, "*": 2, "/": 2}

        output: list[str] = []
        ops: list[str] = []

        for t in tokens:
            if self._is_operator(t):
                while ops and precedence.get(ops[-1], 0) >= precedence[t]:
                    output.append(ops.pop())
                ops.append(t)
            else:
                output.append(t)
        
        while ops:
            output.append(ops.pop())
        
        # Evaluate RPN
        stack: list[Decimal] = []
        for t in output:
            if not self._is_operator(t):
                stack.append(Decimal(t))
                continue

            if len(stack) < 2:
                raise ValueError("Bad expression")
            
            b = stack.pop()
            a = stack.pop()

            if t == "+":
                stack.append(a + b)
            elif t == "-":
                stack.append(a - b)
            elif t == "*":
                stack.append(a * b)
            elif t == "/":
                if b == 0:
                    raise ZeroDivisionError
                stack.append(a / b)
        
        if len(stack) != 1:
            raise ValueError("Bad expression")
        
        return stack[0]
    

# ------------------------------- Utilitied -------------------------------


    def _is_operator(self, t: str) -> bool:
        return t in {"+", "-", "*", "/"}
    
    def _format_decimal(self, x: Decimal) -> str:
        # Avoid scientific notation for typical calculator output
        s = format(x.normalize(), "f")
        if "." in s:
            s = s.rstrip("0").rstrip(".")
        return s if s else "0"
    
    def _error(self) -> None:
        self.tokens = []
        self.entry = ""
        self.just_evaluated = False
        self.display_text.set("Error")





if __name__ == "__main__":
    Calculator().mainloop()
