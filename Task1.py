import tkinter as tk
from tkinter import messagebox

class ArithmeticTool:
    def __init__(self, main_window):
        self.main_window = main_window
        main_window.title("Basic Arithmetic Tool")
        main_window.geometry("350x250")
        main_window.resizable(False, False)

        self.input_section = tk.Frame(main_window, padx=10, pady=10)
        self.input_section.pack(pady=5)

        self.operand1_label = tk.Label(self.input_section, text="Value One:")
        self.operand1_label.grid(row=0, column=0, pady=5, sticky='w')
        self.operand1_entry = tk.Entry(self.input_section, width=20)
        self.operand1_entry.grid(row=0, column=1, pady=5)

        self.operand2_label = tk.Label(self.input_section, text="Value Two:")
        self.operand2_label.grid(row=1, column=0, pady=5, sticky='w')
        self.operand2_entry = tk.Entry(self.input_section, width=20)
        self.operand2_entry.grid(row=1, column=1, pady=5)

        self.operation_buttons_frame = tk.Frame(main_window, padx=10, pady=10)
        self.operation_buttons_frame.pack(pady=5)

        self.perform_addition_btn = tk.Button(self.operation_buttons_frame, text="+", width=5, command=lambda: self.execute_operation('addition'))
        self.perform_addition_btn.grid(row=0, column=0, padx=5, pady=5)

        self.perform_subtraction_btn = tk.Button(self.operation_buttons_frame, text="-", width=5, command=lambda: self.execute_operation('subtraction'))
        self.perform_subtraction_btn.grid(row=0, column=1, padx=5, pady=5)

        self.perform_multiplication_btn = tk.Button(self.operation_buttons_frame, text="*", width=5, command=lambda: self.execute_operation('multiplication'))
        self.perform_multiplication_btn.grid(row=0, column=2, padx=5, pady=5)

        self.perform_division_btn = tk.Button(self.operation_buttons_frame, text="/", width=5, command=lambda: self.execute_operation('division'))
        self.perform_division_btn.grid(row=0, column=3, padx=5, pady=5)

        self.output_display_frame = tk.Frame(main_window, padx=10, pady=10)
        self.output_display_frame.pack(pady=5)

        self.calculation_output_label = tk.Label(self.output_display_frame, text="Outcome: ", font=('Arial', 12, 'bold'))
        self.calculation_output_label.pack()

    def retrieve_operands(self):
        try:
            val1 = float(self.operand1_entry.get())
            val2 = float(self.operand2_entry.get())
            return val1, val2
        except ValueError:
            messagebox.showerror("Input Validation Error", "Kindly input valid numerical values in both fields.")
            return None, None

    def execute_operation(self, chosen_operation):
        val1, val2 = self.retrieve_operands()
        if val1 is None or val2 is None:
            self.calculation_output_label.config(text="Outcome: Invalid Input")
            return

        final_result = None
        if chosen_operation == 'addition':
            final_result = val1 + val2
        elif chosen_operation == 'subtraction':
            final_result = val1 - val2
        elif chosen_operation == 'multiplication':
            final_result = val1 * val2
        elif chosen_operation == 'division':
            if val2 == 0:
                messagebox.showerror("Arithmetic Error", "Division by zero is not permissible.")
                self.calculation_output_label.config(text="Outcome: Division by Zero Error")
                return
            final_result = val1 / val2
        
        self.calculation_output_label.config(text=f"Outcome: {final_result}")

if __name__ == "__main__":
    root_instance = tk.Tk()
    application_instance = ArithmeticTool(root_instance)
    root_instance.mainloop()
