import tkinter as tk

root = tk.Tk()
root.title("tkinter 테스트")
root.geometry("300x200")

label = tk.Label(root, text="tkinter 정상 작동!", font = ("Arial", 14))
label.pack(pady=20)

root.mainloop()