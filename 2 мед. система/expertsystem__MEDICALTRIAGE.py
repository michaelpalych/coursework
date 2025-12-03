import tkinter as tk
from tkinter import ttk, messagebox

from knowledge_base import infer_urgency_and_text


class MedicalTriageKanrenApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Учебная экспертная система: предварительная мед. оценка (kanren)")
        self.geometry("1000x650")

        # Варианты на русском для пользователя
        self.age_options = ["Младенец", "Ребёнок", "Взрослый", "Пожилой"]
        self.fever_options = ["Нет", "Небольшая (до ~37.5)", "Высокая (38–39)", "Очень высокая (выше 39)"]
        self.pain_options = ["Нет", "Лёгкая", "Умеренная", "Сильная"]

        # Соответствие русских меток внутренним кодам
        self.age_map = {
            "Младенец": "infant",
            "Ребёнок": "child",
            "Взрослый": "adult",
            "Пожилой": "elderly",
        }
        self.fever_map = {
            "Нет": "none",
            "Небольшая (до ~37.5)": "mild",
            "Высокая (38–39)": "high",
            "Очень высокая (выше 39)": "very_high",
        }
        self.pain_map = {
            "Нет": "none",
            "Лёгкая": "mild",
            "Умеренная": "moderate",
            "Сильная": "severe",
        }

        # Переменные формы (то, что видит пользователь — русские строки)
        self.var_age = tk.StringVar(value=self.age_options[2])   # Взрослый
        self.var_fever = tk.StringVar(value=self.fever_options[0])
        self.var_pain = tk.StringVar(value=self.pain_options[0])

        self.var_chest_pain = tk.BooleanVar(value=False)
        self.var_breath = tk.BooleanVar(value=False)
        self.var_confusion = tk.BooleanVar(value=False)
        self.var_dehydration = tk.BooleanVar(value=False)
        self.var_rash = tk.BooleanVar(value=False)
        self.var_abd_pain = tk.BooleanVar(value=False)
        self.var_head_trauma = tk.BooleanVar(value=False)
        self.var_bleeding = tk.BooleanVar(value=False)
        self.var_pregnancy = tk.BooleanVar(value=False)
        self.var_chronic = tk.BooleanVar(value=False)

        self._build_ui()

    def _build_ui(self):
        main = ttk.Frame(self, padding=10)
        main.pack(fill=tk.BOTH, expand=True)

        left = ttk.Frame(main)
        left.pack(side=tk.LEFT, fill=tk.Y)

        right = ttk.Frame(main)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        row = 0

        ttk.Label(left, text="Возрастная группа:").grid(row=row, column=0, sticky="w")
        ttk.Combobox(
            left, textvariable=self.var_age, state="readonly",
            values=self.age_options
        ).grid(row=row, column=1, sticky="ew", pady=2)
        row += 1

        ttk.Label(left, text="Температура:").grid(row=row, column=0, sticky="w")
        ttk.Combobox(
            left, textvariable=self.var_fever, state="readonly",
            values=self.fever_options
        ).grid(row=row, column=1, sticky="ew", pady=2)
        row += 1

        ttk.Label(left, text="Сила боли:").grid(row=row, column=0, sticky="w")
        ttk.Combobox(
            left, textvariable=self.var_pain, state="readonly",
            values=self.pain_options
        ).grid(row=row, column=1, sticky="ew", pady=2)
        row += 1

        ttk.Label(left, text="Симптомы (отметьте, что есть):").grid(
            row=row, column=0, columnspan=2, sticky="w", pady=(8, 2)
        )
        row += 1

        ttk.Checkbutton(left, text="Боль / давление в груди", variable=self.var_chest_pain).grid(
            row=row, column=0, columnspan=2, sticky="w"
        )
        row += 1
        ttk.Checkbutton(left, text="Затруднённое дыхание / одышка", variable=self.var_breath).grid(
            row=row, column=0, columnspan=2, sticky="w"
        )
        row += 1
        ttk.Checkbutton(left, text="Спутанность сознания, дезориентация", variable=self.var_confusion).grid(
            row=row, column=0, columnspan=2, sticky="w"
        )
        row += 1
        ttk.Checkbutton(left, text="Признаки обезвоживания (сухость, мало мочи)", variable=self.var_dehydration).grid(
            row=row, column=0, columnspan=2, sticky="w"
        )
        row += 1
        ttk.Checkbutton(left, text="Высыпания на коже", variable=self.var_rash).grid(
            row=row, column=0, columnspan=2, sticky="w"
        )
        row += 1
        ttk.Checkbutton(left, text="Сильная боль в животе", variable=self.var_abd_pain).grid(
            row=row, column=0, columnspan=2, sticky="w"
        )
        row += 1
        ttk.Checkbutton(left, text="Травма головы / недавний удар", variable=self.var_head_trauma).grid(
            row=row, column=0, columnspan=2, sticky="w"
        )
        row += 1
        ttk.Checkbutton(left, text="Сильное кровотечение", variable=self.var_bleeding).grid(
            row=row, column=0, columnspan=2, sticky="w"
        )
        row += 1
        ttk.Checkbutton(left, text="Беременность", variable=self.var_pregnancy).grid(
            row=row, column=0, columnspan=2, sticky="w"
        )
        row += 1
        ttk.Checkbutton(left, text="Серьёзные хронические болезни", variable=self.var_chronic).grid(
            row=row, column=0, columnspan=2, sticky="w"
        )
        row += 1

        ttk.Button(left, text="Оценить срочность", command=self.on_evaluate).grid(
            row=row, column=0, columnspan=2, sticky="ew", pady=10
        )
        row += 1

        for c in range(2):
            left.grid_columnconfigure(c, weight=1)

        ttk.Label(right, text="Результат (уровень срочности):", font=("TkDefaultFont", 10, "bold")).pack(anchor="w")
        self.result_text = tk.Text(right, height=4, wrap="word")
        self.result_text.pack(fill=tk.X, pady=4)

        ttk.Label(right, text="Комментарий системы:", font=("TkDefaultFont", 10, "bold")).pack(anchor="w")
        self.comment_text = tk.Text(right, height=12, wrap="word")
        self.comment_text.pack(fill=tk.BOTH, expand=True, pady=4)

        disclaimer = (
            "Важное замечание:\n"
            "Эта программа является УЧЕБНЫМ примером работы логической системы (kanren).\n"
            "Она НЕ заменяет консультацию врача и НЕ предназначена для постановки диагнозов.\n"
            "При любых сомнениях, тяжёлых или нарастающих симптомах немедленно обращайтесь за "
            "медицинской помощью.\n"
        )
        ttk.Label(right, text="Дисклеймер:", font=("TkDefaultFont", 10, "bold")).pack(anchor="w", pady=(8, 0))
        self.disclaimer_text = tk.Text(right, height=6, wrap="word")
        self.disclaimer_text.pack(fill=tk.X, pady=(2, 0))
        self.disclaimer_text.insert(tk.END, disclaimer)
        self.disclaimer_text.configure(state="disabled")

    def on_evaluate(self):
        try:
            age_code = self.age_map[self.var_age.get()]
            fever_code = self.fever_map[self.var_fever.get()]
            pain_code = self.pain_map[self.var_pain.get()]

            symptoms = {
                "age": age_code,
                "fever": fever_code,
                "pain": pain_code,
                "chest_pain": bool(self.var_chest_pain.get()),
                "breath": bool(self.var_breath.get()),
                "confusion": bool(self.var_confusion.get()),
                "dehydration": bool(self.var_dehydration.get()),
                "rash": bool(self.var_rash.get()),
                "abd_pain": bool(self.var_abd_pain.get()),
                "head_trauma": bool(self.var_head_trauma.get()),
                "bleeding": bool(self.var_bleeding.get()),
                "pregnancy": bool(self.var_pregnancy.get()),
                "chronic": bool(self.var_chronic.get()),
            }

            urgency, text = infer_urgency_and_text(symptoms)

            level_map = {
                'emergency': "Экстренная ситуация",
                'urgent': "Срочно (в ближайшие часы)",
                'doctor': "Плановая консультация врача",
                'home': "Наблюдение дома (низкая срочность)",
            }
            level_human = level_map.get(urgency, urgency)

            self.result_text.delete("1.0", tk.END)
            self.comment_text.delete("1.0", tk.END)

            self.result_text.insert(tk.END, f"Оценка срочности: {level_human}\n(категория: {urgency})\n")
            self.comment_text.insert(tk.END, text + "\n")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при оценке: {e}")


if __name__ == "__main__":
    app = MedicalTriageKanrenApp()
    app.mainloop()
