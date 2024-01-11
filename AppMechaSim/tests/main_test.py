import tkinter as tk

def main():
    root = tk.Tk()
    root.geometry('300x300')  # Set initial window size

    # Create a canvas inside a frame (to attach the scrollbar)
    frame = tk.Frame(root, width=300, bg="blue")
    frame.pack(side='left', fill='y')  # Removed expand=True

    canvas = tk.Canvas(frame, width=60)
    canvas.pack(side='left', fill='y', expand=True)

    # Create a scrollbar and attach it to the canvas
    scrollbar = tk.Scrollbar(frame, orient='vertical', command=canvas.yview)
    scrollbar.pack(side='left', fill='y')
    canvas.config(scrollregion=canvas.bbox("all"))

    # Add a frame inside the canvas to hold the buttons
    button_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=button_frame, anchor='nw')

    # Add buttons to the button frame
    for i in range(100):
        button = tk.Button(button_frame, text=f"Button {i + 1}")
        button.pack()

    # Update the scrollregion of the canvas to fit its contents
    button_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox('all'))

    root.mainloop()


if __name__ == '__main__':
    main()

    # btn1 = tk.Button(frame, text="Button 1", command=create_buttons)
    # btn1.pack(side="top", fill="x")
