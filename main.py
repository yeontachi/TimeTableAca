import tkinter as tk
from tkinter import ttk, messagebox, Canvas
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
            open_time_selection_window() # 시간 선택 창으로 이동
        else:
            messagebox.showerror("오류", "모든 선생님 이름을 입력하세요.")

    button = tk.Button(name_window, text="다음", font=("Arial", 12), command=save_names)
    button.pack(pady=10)

    name_window.mainloop()

# 시간표 UI로 이동하는 함수(다음 단계에서 구현)

def open_schedule_window():
    global teacher_schedule  # ✅ 전역 변수 추가
    print(f"DEBUG: open_schedule_window 실행됨, 현재 teacher_schedule → {teacher_schedule}")  # ✅ 디버깅 추가

    schedule_window = tk.Tk()
    schedule_window.title("학원 시간표")
    schedule_window.geometry("900x600")

    label = tk.Label(schedule_window, text="선생님 시간표", font=("Arial", 14))
    label.pack(pady=10)

    # ✅ 캔버스를 사용하여 시간표 표시
    canvas = Canvas(schedule_window, width=850, height=500, bg="white")
    canvas.pack()

    columns = ["시간"] + ["월", "화", "수", "목", "금", "토", "일"]
    times = [f"{hour}:00" for hour in range(10, 23)]
    
    cell_width = 100
    cell_height = 30
    start_x = 50
    start_y = 50

    # ✅ 테이블 헤더 그리기
    for col_idx, col in enumerate(columns):
        canvas.create_rectangle(start_x + col_idx * cell_width, start_y - cell_height, 
                                start_x + (col_idx + 1) * cell_width, start_y, fill="gray")
        canvas.create_text(start_x + col_idx * cell_width + 50, start_y - 15, text=col, font=("Arial", 12), fill="white")

    # ✅ 시간 및 요일 셀 그리기
    for row_idx, time in enumerate(times):
        for col_idx, day in enumerate(columns):
            x1 = start_x + col_idx * cell_width
            y1 = start_y + row_idx * cell_height
            x2 = start_x + (col_idx + 1) * cell_width
            y2 = start_y + (row_idx + 1) * cell_height

            if col_idx == 0:  # ✅ 첫 번째 컬럼(시간)
                canvas.create_rectangle(x1, y1, x2, y2, fill="lightgray")
                canvas.create_text(x1 + 50, y1 + 15, text=time, font=("Arial", 12))
            else:  # ✅ 요일별 데이터
                teachers = []
                for teacher in teacher_schedule:
                    if day in teacher_schedule[teacher] and time in teacher_schedule[teacher][day]:
                        teachers.append(teacher)

                if teachers:
                    canvas.create_rectangle(x1, y1, x2, y2, fill="lightgreen")  # ✅ 가능 시간 초록색
                    canvas.create_text(x1 + 50, y1 + 15, text=", ".join(teachers), font=("Arial", 10))
                else:
                    canvas.create_rectangle(x1, y1, x2, y2, fill="white")
    
    # ✅ 편집 버튼 추가
    edit_button = tk.Button(schedule_window, text="편집", font=("Arial", 12), command=open_time_selection_window)
    edit_button.pack(pady=10)

    schedule_window.mainloop()



# 가능한 시간 선택 UI
def open_time_selection_window():
    global teacher_schedule  # ✅ 전역 변수 사용
    time_window = tk.Tk()
    time_window.title("가능한 시간 선택")
    time_window.geometry("600x500")

    label = tk.Label(time_window, text="가능한 시간을 선택하세요", font=("Arial", 14))
    label.pack(pady=10)

    selected_teacher = tk.StringVar()
    
    # ✅ 드롭다운 추가
    teacher_dropdown = tk.OptionMenu(time_window, selected_teacher, *teacher_names)
    teacher_dropdown.pack(pady=5)

    # ✅ 요일 및 시간 체크박스 저장할 딕셔너리
    checkboxes = {}

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
            checkboxes[day][time] = var  # ✅ 변경된 값이 반영되도록 설정

    # ✅ 선생님 변경 시 체크박스 상태 업데이트
    def update_checkboxes(*args):
        teacher = selected_teacher.get()
        
        # ✅ 모든 체크박스를 초기화
        for day in days:
            for time in times:
                checkboxes[day][time].set(False)

        # ✅ 선택된 선생님의 저장된 가능 시간 반영
        if teacher in teacher_schedule:
            for day in teacher_schedule[teacher]:
                for time in teacher_schedule[teacher][day]:
                    if time in checkboxes[day]:  # ✅ 존재하는 시간만 반영
                        checkboxes[day][time].set(True)

    selected_teacher.trace("w", update_checkboxes)  # ✅ 드롭다운 변경 시 실행

    # ✅ 저장 버튼 (저장만 하고 창 유지)
    def save_schedule():
        global teacher_schedule
        teacher = selected_teacher.get()

        if not teacher:
            messagebox.showerror("오류", "선생님을 선택하세요.")
            return

        if teacher not in teacher_schedule:
            teacher_schedule[teacher] = {day: [] for day in days}

        for day in days:
            teacher_schedule[teacher][day] = []
            for time, var in checkboxes[day].items():
                if var.get():
                    teacher_schedule[teacher][day].append(time)

        print(f"DEBUG: {teacher} 선생님의 가능 시간 → {teacher_schedule[teacher]}")  # ✅ 디버깅 추가
        print(f"DEBUG: 최종 teacher_schedule 데이터 → {teacher_schedule}")  # ✅ 전체 데이터 확인 추가

        messagebox.showinfo("저장 완료", f"{teacher} 선생님의 가능 시간이 저장되었습니다.")

    # ✅ 완료 버튼 (시간표 UI로 이동)
    def finish_and_show_schedule():
        save_schedule()  # ✅ 저장 후 창 닫기
        time_window.destroy()
        open_schedule_window()  # ✅ 시간표 UI로 이동

    save_button = tk.Button(time_window, text="저장", font=("Arial", 12), command=save_schedule)
    save_button.pack(pady=5)

    finish_button = tk.Button(time_window, text="완료", font=("Arial", 12), command=finish_and_show_schedule)
    finish_button.pack(pady=10)

    time_window.mainloop()


# 프로그램 실행
if __name__ == "__main__":
    root = tk.Tk()
    app = ui.TimeTableApp(root)
    root.mainloop()


