import tkinter as tk
from tkinter import messagebox
import ui

teacher_count = 0 # 전역 변수로 선생님 수 저장
teacher_names = [] # 선생님 이름 리스트

# 선생님 이름 입력 UI
def open_teacher_name_window():
    name_window = tk.Tk()
    name_window.title("TimeTableAca - 선생님 이름 입력")
    name_window.geometry("400x300")

    label = tk.Label(name_window, text="선생님 이름을 입력하세요", font=("Arial", 14))
    label.pack(pady=10)

    entry_list = []
    for i in range(teacher_count):
        entry = tk.Entry(name_window, font=("Arial", 12))
        entry.pack(pady=5)
        entry_list.append(entry)

    def save_names():
        global teacher_names
        teacher_names = [entry.get() for entry in entry_list if entry.get()]
        if len(teacher_names) == teacher_count:
            messagebox.showinfo("완료", "선생님 정보가 저장되었습니다.")
            name_window.destroy() # 현재 창 닫기
            open_schedule_window() # 시간표 UI로 이동
        else:
            messagebox.showerror("오류", "모든 선생님 이름을 입력하세요.")

        button = tk.Button(name_window, text="다음", font=("Arial", 12), command=save_names)
        button.pack(pady=10)

        name_window.mainloop()

# 시간표 UI로 이동하는 함수(다음 단계에서 구현)
def open_schedule_window():
    pass #여기에 시간표 UI 구현 예정

# 프로그램 실행
if __name__ == "__main__":
    root = tk.Tk()
    app = ui.TimeTableApp(root)
    root.mainloop()


