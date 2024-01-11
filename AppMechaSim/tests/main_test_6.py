import tkinter as tk

def update_buttons():
    search_text = search_var.get().lower()
    for button in buttons:
        text = button.cget("text").lower()
        button.pack_forget()
        if search_text in text:
            button.pack()

root = tk.Tk()

search_var = tk.StringVar()

search_entry = tk.Entry(root, textvariable=search_var)
search_entry.pack()

search_button = tk.Button(root, text="Search", command=update_buttons)
search_button.pack()

buttons = [tk.Button(root, text=f"Button {i}") for i in range(10)]
for button in buttons:
    button.pack()

root.mainloop()