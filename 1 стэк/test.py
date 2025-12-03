import yaml

from tech_stack_expert_system_tk import TechStackEngine, Project, Recommendation


def recommend_stack(params: dict) -> dict:
    engine = TechStackEngine()
    engine.reset()
    engine.declare(Project(**params))
    engine.run()

    rec_facts = [
        (fid, f)
        for fid, f in engine.facts.items()
        if isinstance(f, Recommendation)
    ]

    if not rec_facts:
        return {}

    rec_facts.sort(key=lambda x: x[0])
    _, rec = rec_facts[-1]

    return {
        "backend": rec["backend"],
        "frontend": rec["frontend"],
        "database": rec["database"],
        "infra": rec["infra"],
    }


def run_tech_stack_tests(cases: dict) -> None:
    print("=== Тесты системы выбора стека ===")
    total = 0
    failed = 0

    for case in cases.get("tests", []):
        total += 1
        test_id = case.get("id", "<no-id>")
        desc = case.get("description", "")
        params = case["project"]
        expected = case["expect"]

        rec = recommend_stack(params)

        ok_backend = rec.get("backend") == expected["backend"]
        ok_frontend = rec.get("frontend") == expected["frontend"]
        ok_db = rec.get("database") == expected["database"]
        ok_infra = rec.get("infra") == expected["infra"]

        all_ok = ok_backend and ok_frontend and ok_db and ok_infra
        status = "OK" if all_ok else "FAIL"

        print(f"[{status}] {test_id} — {desc}")
        if not all_ok:
            failed += 1
            print("  Ожидалось:", expected)
            print("  Получено :", rec)

    print(f"\nИТОГО: {total} сценариев, ошибок: {failed}")


def main():
    with open("tests_tech_stack.yaml", "r", encoding="utf-8") as f:
        cases = yaml.safe_load(f)
    run_tech_stack_tests(cases)


if __name__ == "__main__":
    main()
