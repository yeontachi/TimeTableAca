import tkinter as tk
from tkinter import messagebox
import main

class TimeTableApp:
    def __init__(self, root): 
        self.root = root
        self.root.title("TimeTable Aca - 선생님 수 입력")
        self.root.geometry("400x200")

        #라벨
        self.label = tk.Label(root, text="선생님 수를 입력하세요", font=("Arial", 14))
        self.label.pack(pady=10)

        #입력 필드
        self.entry = tk.Entry(root, font=("Arial", 12))
        self.entry.pack(pady=5)

        #확인 버튼
        self.confirm_button = tk.Button(root, text="확인", font=("Arial", 12), command=self.get_teacher_count)
        self.confirm_button.pack(pady=10)

    def get_teacher_count(self):
        count = self.entry.get()
        if count.isdigit() and int(count) > 0:
            main.get_teacher_count = int(count) # 메인 파일에서 전역 변수로 저장
            self.root.destroy()     #현재 창 닫기
            main.open_teacher_name_window # 다음 창 열기
        else: 
            messagebox.showerror("오류", "올바른 숫자를 입력하세요.")