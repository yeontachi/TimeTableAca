import tkinter as tk
from tkinter import ttk, messagebox
import ui

teacher_count = 0 # 전역 변수로 선생님 수 저장
teacher_names = [] # 선생님 이름 리스트
entry_list = [] # 전역 변수로 관리

teacher_schedule = {} # {이름: {요일: [가능한 시간 리스트]}} 형태로 저장

# 선생님 이름 입력 UI
def open_teacher_name_window():
    global entry_list, teacher_count # 전역 변수 선언
    name_window = tk.Tk()
    name_window.title("TimeTableAca - 선생님 이름 입력")
    name_window.geometry("400x300")

    label = tk.Label(name_window, text="선생님 이름을 입력하세요", font=("Arial", 14))
    label.pack(pady=10)

    # 기존 entry_list 초기화
    entry_list.clear()

    for i in range(teacher_count):
        entry = tk.Entry(name_window, font=("Arial", 12))
        entry.pack(pady=5, fill="x", expand=True, padx=20)
        entry_list.append(entry)

    print("Entry 리스트 길이 : ", len(entry_list)) # 디버깅 코드
    
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
    schedule_window = tk.Tk()
    schedule_window.title("학원 시간표")
    schedule_window.geometry("800x500")

    label = tk.Label(schedule_window, text="선생님 시간표", font=("Arial", 14))
    label.pack(pady=10)

    # 시간표 테이블
    columns = ["시간"] + ["월", "화", "수", "목", "금", "토", "일"]
    tree = ttk.Treeview(schedule_window, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    # 데이터 삽입
    times = [f"{hour}:00" for hour in range(10, 23)]

    for time in times:
        row_data = [time]
        for day in columns[1:]: #요일별 데이터
            teachers = []
            for teacher in teacher_schedule:
                if time in teacher_schedule[teacher][day]:
                    teachers.append(teacher)
            row_data.append(", ".join(teachers) if teachers else "")
        tree.insert("", "end", values=row_data)

    tree.pack(expand=True, fill="both")

    # 편집 버튼
    edit_button = tk.Button(schedule_window, text="편집", font=("Arial", 12), command = open_time_selection_window)
    edit_button.pack(pady=10)

    schedule_window.mainloop()

# 가능한 시간 선택 UI
def open_time_selection_window():
    time_window = tk.Tk()
    time_window.title("가능한 시간 선택")
    time_window.geometry("600x500")

    label = tk.Label(time_window, text="가능한 시간을 선택하세요", font=("Arial", 14))
    label.pack(pady=10)

    selected_teacher = tk.StringVar()

    #선생님 선택 드롭다운
    teacher_dropdown = tk.OptionMenu(time_window, selected_teacher, *teacher_names)
    teacher_dropdown.pack(pady=5)

    # 요일 및 시간 체크박스 저장할 딕셔너리
    checkboxes = {}

    # 요일 및 시간 ㅕㅑ
    days = ["월", "화", "수", "목", "금", "토", "일"]
    times = [f"{hour}:00" for hour in range(10, 23)]

    for day in days:
        frame = tk.LabelFrame(time_window, text=day, padx=5, pady=5)
        frame.pack(padx=5, pady=5, fill="both")

        checkboxes[day] = {}
        for time in times:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(frame, text=time, variable=var)
            cb.pack(side="left")
            checkboxes[day][time] = var

    # 데이터 저장 함수
    def save_schedule():
        teacher = selected_teacher.get()
        if not teacher:
            messagebox.showerror("오류", "선생님을 선택하세요.")
            return
        
        teacher_schedule[teacher] = {day: [] for day in days}
        for day in days:
            for time in times:
                if checkboxes[day][time].get():
                    teacher_schedule[teacher][day].append(time)

        messagebox.showinfo("완료", f"{teacher} 선생님의 가능 시간이 저장되었습니다.")
        print(teacher_schedule) # 콘솔 출력(디버깅용)
        time_window.destroy()


    # 저장 버튼
    save_button = tk.Button(time_window, text="저장", font=("Arial", 12), command=save_schedule)
    save_button.pack(pady=10)

    time_window.mainloop()

# 프로그램 실행
if __name__ == "__main__":
    root = tk.Tk()
    app = ui.TimeTableApp(root)
    root.mainloop()


