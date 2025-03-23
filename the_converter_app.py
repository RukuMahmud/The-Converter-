
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pyperclip

root = tk.Tk()
root.title("The Converter")
root.geometry("800x500")
root.configure(bg="#f8f8f2")  # Off-white sci-fi theme

FONT = ("Calibri", 14)
ENTRY_WIDTH = 15

# === Global Unit Dictionaries ===
length_units = {
    'millimeter': 0.001,
    'centimeter': 0.01,
    'decimeter': 0.1,
    'meter': 1,
    'inch': 0.0254,
    'foot': 0.3048,
    'pixel': 0.000264583,
    'point': 0.000352778,
    'kilometer': 1000,
    'mile': 1609.34,
    'nautical mile': 1852
}

weight_units = {
    'milligram': 0.001,
    'gram': 1,
    'kilogram': 1000,
    'ounce': 28.3495,
    'pound': 453.592,
    'ton': 1_000_000
}

# === Dynamic Variables ===
entry_widgets = {}
current_mode = 'length'

# === Clear Widgets ===
def clear_widgets():
    for widget in root.winfo_children():
        widget.destroy()

# === Conversion Logic ===
def on_value_change(event, changed_unit, unit_dict):
    try:
        value = float(entry_widgets[changed_unit].get())
        base_value = value * unit_dict[changed_unit]

        for unit, factor in unit_dict.items():
            if unit != changed_unit:
                result = base_value / factor
                entry_widgets[unit].delete(0, tk.END)
                entry_widgets[unit].insert(0, f"{result:.6f}")
    except ValueError:
        pass

# === Copy to Clipboard ===
def copy_to_clipboard():
    copied_values = []
    for unit, entry in entry_widgets.items():
        copied_values.append(f"{unit}: {entry.get()}")
    pyperclip.copy("\n".join(copied_values))
    messagebox.showinfo("Copied!", "Converted values copied to clipboard.")

# === Create Unit Converter ===
def create_converter(unit_dict):
    clear_widgets()
    global entry_widgets
    entry_widgets = {}

    row = 0
    for unit in unit_dict:
        tk.Label(root, text=unit.title(), font=FONT, bg="#f8f8f2").grid(row=row, column=0, padx=10, pady=5, sticky="e")
        entry = tk.Entry(root, font=FONT, width=ENTRY_WIDTH, justify='right')
        entry.grid(row=row, column=1, padx=10, pady=5)
        entry_widgets[unit] = entry

        entry.bind('<KeyRelease>', lambda e, u=unit: on_value_change(e, u, unit_dict))
        row += 1

    copy_btn = tk.Button(root, text="Copy", font=FONT, bg="orange", command=copy_to_clipboard)
    copy_btn.grid(row=row, column=1, pady=10)

# === Switch Mode ===
def activate_length():
    global current_mode
    current_mode = 'length'
    create_converter(length_units)

def activate_weight():
    global current_mode
    current_mode = 'weight'
    create_converter(weight_units)

# === Initial Buttons ===
style = ttk.Style()
style.configure("TButton", font=FONT, padding=10)

length_btn = tk.Button(root, text="Length Converter", font=FONT, bg="orange", command=activate_length)
length_btn.pack(pady=20)

weight_btn = tk.Button(root, text="Weight Converter", font=FONT, bg="orange", command=activate_weight)
weight_btn.pack(pady=10)

root.mainloop()
