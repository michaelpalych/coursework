from experta import Fact, Field, KnowledgeEngine, Rule, MATCH, TEST, W
import tkinter as tk
from tkinter import ttk, messagebox


# ==========================
#   МОДЕЛЬ ДАННЫХ (ФАКТЫ)
# ==========================


class Project(Fact):
    kind = Field(str, mandatory=True)
    scale = Field(str, mandatory=True)
    deadline = Field(str, mandatory=True)
    team_skill = Field(str, mandatory=True)
    realtime = Field(bool, mandatory=True)
    admin_panel = Field(bool, mandatory=True)
    mobile_needed = Field(bool, mandatory=True)
    seo_critical = Field(bool, mandatory=True)
    analytics_needed = Field(bool, mandatory=True)
    budget = Field(str, mandatory=True)
    long_lived = Field(bool, mandatory=True)


class Backend(Fact):
    name = Field(str, mandatory=True)


class Frontend(Fact):
    name = Field(str, mandatory=True)


class Database(Fact):
    name = Field(str, mandatory=True)


class Infra(Fact):
    description = Field(str, mandatory=True)


class Extra(Fact):
    note = Field(str, mandatory=True)


class Recommendation(Fact):
    backend = Field(str, mandatory=True)
    frontend = Field(str, mandatory=True)
    database = Field(str, mandatory=True)
    infra = Field(str, mandatory=True)


# ==========================
#   ДВИЖОК ВЫВОДА
# ==========================


class TechStackEngine(KnowledgeEngine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.explanations = []

    def explain(self, text: str):
        self.explanations.append(text)

    # --- Backend rules ---
    @Rule(Project(kind='landing', seo_critical=True, team_skill=MATCH.skill),
          TEST(lambda skill: skill in ('mostly_python', 'python_and_js', 'mixed')))
    def backend_landing_seo(self, skill):
        self.declare(Backend(name='Django (server-side templates)'))
        self.explain("SEO-лендинг, команда с Python → Django с шаблонами.")

    @Rule(Project(kind='landing', seo_critical=True, team_skill='strong_frontend'))
    def backend_landing_frontend(self):
        self.declare(Backend(name='Django/FastAPI как headless API'))
        self.explain("SEO-лендинг, сильный фронт → headless API.")

    @Rule(Project(kind='shop', admin_panel=True))
    def backend_shop(self):
        self.declare(Backend(name='Django + Django REST Framework'))
        self.explain("Магазин с админкой → Django + DRF.")

    @Rule(Project(kind='saas', realtime=True))
    def backend_saas_rt(self):
        self.declare(Backend(name='FastAPI (async + WebSocket)'))
        self.explain("SaaS с real-time → FastAPI.")

    @Rule(Project(kind='saas', realtime=False))
    def backend_saas_simple(self):
        self.declare(Backend(name='Django + DRF'))
        self.explain("SaaS без real-time → Django + DRF.")

    @Rule(Project(kind='api', realtime=False))
    def backend_api_simple(self):
        self.declare(Backend(name='FastAPI или DRF'))
        self.explain("REST API без real-time → FastAPI/DRF.")

    @Rule(Project(kind='api', realtime=True))
    def backend_api_rt(self):
        self.declare(Backend(name='FastAPI (async)'))
        self.explain("API с real-time → FastAPI.")

    @Rule(Project(kind='internal_tool'))
    def backend_internal(self):
        self.declare(Backend(name='Django (admin)'))
        self.explain("Внутренний тул → Django admin.")

    @Rule(Project(kind=MATCH.kind),
          ~Backend(name=W()), salience=-5)
    def backend_fallback(self, kind):
        self.declare(Backend(name='Django (по умолчанию)'))
        self.explain(f"Тип проекта {kind} → универсальный выбор Django.")

    @Rule(Project(kind='landing', seo_critical=True, team_skill=MATCH.skill),
          TEST(lambda skill: skill != 'strong_frontend'))
    def frontend_landing_simple(self, skill):
        self.declare(Frontend(name='Server-side HTML + немного JS'))
        self.explain("SEO-лендинг, нет сильного фронта → серверный HTML.")

    @Rule(Project(kind='landing', seo_critical=True, team_skill='strong_frontend'))
    def frontend_landing_spa(self):
        self.declare(Frontend(name='React/Vue с SSR'))
        self.explain("SEO-лендинг, сильный фронт → React/Vue с SSR.")

    @Rule(Project(kind='shop', scale='startup'))
    def frontend_shop_startup(self):
        self.declare(Frontend(name='Готовая тема + JS'))
        self.explain("Магазин-стартап → готовая тема.")

    @Rule(Project(kind='shop', scale='enterprise'))
    def frontend_shop_enterprise(self):
        self.declare(Frontend(name='SPA (React/Vue)'))
        self.explain("Крупный магазин → SPA.")

    @Rule(Project(kind='internal_tool'))
    def frontend_internal(self):
        self.declare(Frontend(name='Django admin / простые формы'))
        self.explain("Внутренний тул → admin/простые формы.")

    @Rule(Project(kind=MATCH.kind),
          ~Frontend(name=W()), salience=-5)
    def frontend_fallback(self, kind):
        self.declare(Frontend(name='Базовый HTML/CSS + немного JS'))
        self.explain(f"Нет особых требований к фронту ({kind}) → простой HTML.")

    # --- Database rules ---
    @Rule(Project(scale='pet'))
    def db_pet(self):
        self.declare(Database(name='SQLite'))
        self.explain("Pet-проект → SQLite достаточно.")

    @Rule(Project(scale='startup'))
    def db_startup(self):
        self.declare(Database(name='PostgreSQL'))
        self.explain("Startup → PostgreSQL.")

    @Rule(Project(scale='enterprise'))
    def db_enterprise(self):
        self.declare(Database(name='PostgreSQL/Oracle/MySQL'))
        self.explain("Enterprise → промышленная SQL-БД.")

    @Rule(Project(kind=MATCH.kind),
          ~Database(name=W()), salience=-5)
    def db_fallback(self, kind):
        self.declare(Database(name='PostgreSQL'))
        self.explain(f"База по умолчанию для {kind} → PostgreSQL.")

    # --- Infra / Extra ---
    @Rule(Project(scale='pet', deadline='urgent'))
    def infra_pet_urgent(self):
        self.declare(Infra(description='1 VPS, простое логирование.'))
        self.explain("Pet + жёсткий дедлайн → 1 VPS, минимум инфраструктуры.")

    @Rule(Project(scale='startup'))
    def infra_startup(self):
        self.declare(Infra(description='Docker + простой CI/CD.'))
        self.explain("Startup → Docker + CI/CD.")

    @Rule(Project(scale='enterprise'))
    def infra_enterprise(self):
        self.declare(Infra(description='Kubernetes, полноценный CI/CD, мониторинг.'))
        self.explain("Enterprise → Kubernetes и продвинутый мониторинг.")

    @Rule(Project(realtime=True))
    def extra_realtime(self):
        self.declare(Extra(note='Нужны WebSocket/long-polling и Redis/pub-sub.'))
        self.explain("Real-time → WebSocket и Redis/pub-sub.")

    @Rule(Project(long_lived=True))
    def extra_long_lived(self):
        self.declare(Extra(note='Закладывать миграции БД, версионирование API, мониторинг SLA.'))
        self.explain("Долгоживущий проект → миграции, версии API, SLA.")

    @Rule(Project(kind=MATCH.kind),
          ~Infra(description=W()), salience=-5)
    def infra_fallback(self, kind):
        self.declare(Infra(description='1 VPS или PaaS, базовый мониторинг.'))
        self.explain(f"Инфраструктура по умолчанию для {kind} → 1 VPS/PaaS.")

    # --- Final recommendation ---
    @Rule(Backend(name=MATCH.backend),
          Frontend(name=MATCH.frontend),
          Database(name=MATCH.database),
          Infra(description=MATCH.infra),
          salience=-20)
    def gather_recommendation(self, backend, frontend, database, infra):
        self.declare(Recommendation(
            backend=backend,
            frontend=frontend,
            database=database,
            infra=infra
        ))


# ==========================
#   GUI НА TKINTER
# ==========================


class TechStackApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Экспертная система выбора стека технологий")
        self.geometry("900x600")

        # Переменные
        self.var_kind = tk.StringVar(value='landing')
        self.var_scale = tk.StringVar(value='startup')
        self.var_deadline = tk.StringVar(value='normal')
        self.var_team_skill = tk.StringVar(value='python_and_js')
        self.var_budget = tk.StringVar(value='medium')

        self.var_realtime = tk.BooleanVar(value=False)
        self.var_admin_panel = tk.BooleanVar(value=True)
        self.var_mobile_needed = tk.BooleanVar(value=False)
        self.var_seo_critical = tk.BooleanVar(value=True)
        self.var_analytics_needed = tk.BooleanVar(value=False)
        self.var_long_lived = tk.BooleanVar(value=True)

        self._build_widgets()

    def _build_widgets(self):
        main = ttk.Frame(self, padding=10)
        main.pack(fill=tk.BOTH, expand=True)

        left = ttk.Frame(main)
        left.pack(side=tk.LEFT, fill=tk.Y)

        right = ttk.Frame(main)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        row = 0

        ttk.Label(left, text="Тип проекта:").grid(row=row, column=0, sticky="w")
        kind_cb = ttk.Combobox(left, textvariable=self.var_kind, state="readonly",
                               values=['landing', 'shop', 'saas', 'api', 'bot', 'analytics', 'ml_service', 'internal_tool'])
        kind_cb.grid(row=row, column=1, sticky="ew", pady=2)
        row += 1

        ttk.Label(left, text="Масштаб:").grid(row=row, column=0, sticky="w")
        scale_cb = ttk.Combobox(left, textvariable=self.var_scale, state="readonly",
                                values=['pet', 'startup', 'enterprise'])
        scale_cb.grid(row=row, column=1, sticky="ew", pady=2)
        row += 1

        ttk.Label(left, text="Дедлайн:").grid(row=row, column=0, sticky="w")
        deadline_cb = ttk.Combobox(left, textvariable=self.var_deadline, state="readonly",
                                   values=['urgent', 'normal', 'relaxed'])
        deadline_cb.grid(row=row, column=1, sticky="ew", pady=2)
        row += 1

        ttk.Label(left, text="Навык команды:").grid(row=row, column=0, sticky="w")
        team_cb = ttk.Combobox(
            left,
            textvariable=self.var_team_skill,
            state="readonly",
            values=['mostly_python', 'python_and_js', 'strong_frontend', 'mixed', 'unknown']
        )
        team_cb.grid(row=row, column=1, sticky="ew", pady=2)
        row += 1

        ttk.Label(left, text="Бюджет:").grid(row=row, column=0, sticky="w")
        budget_cb = ttk.Combobox(left, textvariable=self.var_budget, state="readonly",
                                 values=['low', 'medium', 'high'])
        budget_cb.grid(row=row, column=1, sticky="ew", pady=2)
        row += 1

        ttk.Checkbutton(left, text="Real-time", variable=self.var_realtime).grid(row=row, column=0, columnspan=2, sticky="w")
        row += 1
        ttk.Checkbutton(left, text="Нужна админ-панель", variable=self.var_admin_panel).grid(row=row, column=0, columnspan=2, sticky="w")
        row += 1
        ttk.Checkbutton(left, text="Нужны mobile-клиенты", variable=self.var_mobile_needed).grid(row=row, column=0, columnspan=2, sticky="w")
        row += 1
        ttk.Checkbutton(left, text="SEO критично", variable=self.var_seo_critical).grid(row=row, column=0, columnspan=2, sticky="w")
        row += 1
        ttk.Checkbutton(left, text="Нужна аналитика/отчёты", variable=self.var_analytics_needed).grid(row=row, column=0, columnspan=2, sticky="w")
        row += 1
        ttk.Checkbutton(left, text="Долгоживущий проект", variable=self.var_long_lived).grid(row=row, column=0, columnspan=2, sticky="w")
        row += 1

        ttk.Button(left, text="Рассчитать стек", command=self.run_engine).grid(row=row, column=0, columnspan=2, pady=10, sticky="ew")
        row += 1

        for c in range(2):
            left.grid_columnconfigure(c, weight=1)

        ttk.Label(right, text="Результат:", font=("TkDefaultFont", 10, "bold")).pack(anchor="w")
        self.result_text = tk.Text(right, height=10, wrap="word")
        self.result_text.pack(fill=tk.X, pady=5)

        ttk.Label(right, text="Объяснения:", font=("TkDefaultFont", 10, "bold")).pack(anchor="w")
        self.explain_text = tk.Text(right, height=15, wrap="word")
        self.explain_text.pack(fill=tk.BOTH, expand=True, pady=5)

    def run_engine(self):
        try:
            engine = TechStackEngine()
            engine.reset()

            project_fact = Project(
                kind=self.var_kind.get(),
                scale=self.var_scale.get(),
                deadline=self.var_deadline.get(),
                team_skill=self.var_team_skill.get(),
                realtime=self.var_realtime.get(),
                admin_panel=self.var_admin_panel.get(),
                mobile_needed=self.var_mobile_needed.get(),
                seo_critical=self.var_seo_critical.get(),
                analytics_needed=self.var_analytics_needed.get(),
                budget=self.var_budget.get(),
                long_lived=self.var_long_lived.get(),
            )
            engine.declare(project_fact)
            engine.run()

            recs = [f for f in engine.facts.values() if isinstance(f, Recommendation)]
            extras = [f for f in engine.facts.values() if isinstance(f, Extra)]

            self.result_text.delete("1.0", tk.END)
            self.explain_text.delete("1.0", tk.END)

            if recs:
                rec = recs[0]
                self.result_text.insert(tk.END, f"Backend : {rec['backend']}\n")
                self.result_text.insert(tk.END, f"Frontend: {rec['frontend']}\n")
                self.result_text.insert(tk.END, f"Database: {rec['database']}\n")
                self.result_text.insert(tk.END, f"Infra   : {rec['infra']}\n")
            else:
                self.result_text.insert(tk.END, "Не удалось собрать финальную рекомендацию.\n")

            if extras:
                self.result_text.insert(tk.END, "\nДополнительные заметки:\n")
                for e in extras:
                    self.result_text.insert(tk.END, f"- {e['note']}\n")

            if engine.explanations:
                for i, exp in enumerate(engine.explanations, 1):
                    self.explain_text.insert(tk.END, f"{i}. {exp}\n")
            else:
                self.explain_text.insert(tk.END, "Объяснения отсутствуют (движок не записал причины).\n")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при работе движка:\n{e}")


if __name__ == "__main__":
    app = TechStackApp()
    app.mainloop()
