import tkinter as tk
from tkinter import messagebox
from free_dictionary import fetch_free_dict_definition
from merriam_webster import fetch_merriam_definition
from comparer import measure_response_time, compare_results


# Основное приложение
root = tk.Tk()
root.title("Word Definition App")

# Переменные
language = tk.StringVar(value='en')
word_input = tk.StringVar()

# Обработчик кнопки "Start"
def start_fetching():
    word = word_input.get()
    lang = language.get()

    if not word:
        messagebox.showerror("Input Error", "Please enter a word.")
        return

    # Measure response times
    free_dict_definition, time_free_dict = measure_response_time(fetch_free_dict_definition, word, lang)
    merriam_definition, time_merriam = measure_response_time(fetch_merriam_definition, word)

    # Display API results
    free_dict_text.delete(1.0, tk.END)
    free_dict_text.insert(tk.END, free_dict_definition)

    merriam_text.delete(1.0, tk.END)
    merriam_text.insert(tk.END, merriam_definition)

    # Compare results
    comparison_result = compare_results(free_dict_definition, merriam_definition, time_free_dict, time_merriam)
    comparison_text.delete(1.0, tk.END)
    comparison_text.insert(tk.END, comparison_result)


# Интерфейс
tk.Label(root, text="Enter a word:").pack()
tk.Entry(root, textvariable=word_input).pack()

tk.Label(root, text="Free Dictionary API Result:").pack()
free_dict_text = tk.Text(root, height=5, width=70)
free_dict_text.pack()

tk.Label(root, text="Merriam-Webster API Result:").pack()
merriam_text = tk.Text(root, height=5, width=70)
merriam_text.pack()

tk.Button(root, text="Start", command=start_fetching).pack()

tk.Label(root, text="Comparison Result:").pack()
comparison_text = tk.Text(root, height=5, width=71)
comparison_text.pack()

root.mainloop()
