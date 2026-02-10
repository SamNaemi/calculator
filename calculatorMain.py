import tkinter as tk




class calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.resizable(False, False)


        container = tk.Frame(self)
        container.pack(padx=15, pady=15)

        button_font = ("Arial", 24)
        button_symbol_font = ("Arial", 24)

        buttonPercent = tk.Button(container, text="%", font=button_font, height=2, width=4)
        buttonPercent.grid(row=0, column=0)
        buttonCE = tk.Button(container, text="CE", font=button_font, height=2, width=4)
        buttonCE.grid(row=0, column=1)
        buttonC = tk.Button(container, text="C", font=button_font, height=2, width=4)
        buttonC.grid(row=0, column=2)
        buttonBack = tk.Button(container, text="⌫", font=button_symbol_font, height=2, width=4)
        buttonBack.grid(row=0, column=3)

        button1OverX = tk.Button(container, text="1/x", font=button_font, height=2, width=4)
        button1OverX.grid(row=1, column=0)
        buttonXSquared = tk.Button(container, text="x²", font=button_symbol_font, height=2, width=4)
        buttonXSquared.grid(row=1, column=1)
        buttonRadX = tk.Button(container, text="√x", font=button_symbol_font, height=2, width=4)
        buttonRadX.grid(row=1, column=2)
        buttonDivide = tk.Button(container, text="/", font=button_font, height=2, width=4)
        buttonDivide.grid(row=1, column=3)

        button7 = tk.Button(container, text="7", font=button_font, height=2, width=4)
        button7.grid(row=2, column=0)
        button8 = tk.Button(container, text="8", font=button_font, height=2, width=4)
        button8.grid(row=2, column=1)
        button9 = tk.Button(container, text="9", font=button_font, height=2, width=4)
        button9.grid(row=2, column=2)
        buttonMultiply = tk.Button(container, text="×", font=button_symbol_font, height=2, width=4)
        buttonMultiply.grid(row=2, column=3)

        button4 = tk.Button(container, text="4", font=button_font, height=2, width=4)
        button4.grid(row=3, column=0)
        button5 = tk.Button(container, text="5", font=button_font, height=2, width=4)
        button5.grid(row=3, column=1)
        button6 = tk.Button(container, text="6", font=button_font, height=2, width=4)
        button6.grid(row=3, column=2)
        buttonMinus = tk.Button(container, text="−", font=button_symbol_font, height=2, width=4)
        buttonMinus.grid(row=3, column=3)

        button1 = tk.Button(container, text="1", font=button_font, height=2, width=4)
        button1.grid(row=4, column=0)
        button2 = tk.Button(container, text="2", font=button_font, height=2, width=4)
        button2.grid(row=4, column=1)
        button3 = tk.Button(container, text="3", font=button_font, height=2, width=4)
        button3.grid(row=4, column=2)
        buttonPlus = tk.Button(container, text="+", font=button_font, height=2, width=4)
        buttonPlus.grid(row=4, column=3)

        buttonPlusMinus = tk.Button(container, text="±", font=button_symbol_font, height=2, width=4)
        buttonPlusMinus.grid(row=5, column=0)
        button0 = tk.Button(container, text="0", font=button_font, height=2, width=4)
        button0.grid(row=5, column=1)
        buttonDot = tk.Button(container, text=".", font=button_font, height=2, width=4)
        buttonDot.grid(row=5, column=2)
        buttonEquals = tk.Button(container, text="=", font=button_font, height=2, width=4)
        buttonEquals.grid(row=5, column=3)




        self.center_window()

    
    def center_window(self) -> None:
        self.update_idletasks() #Ensure size info is correct

        window_width = self.winfo_width()
        window_height = self.winfo_height()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2) - 150

        self.geometry(f"+{x}+{y}")



if __name__ == "__main__":
    calculator().mainloop()
