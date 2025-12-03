import yaml
from knowledge_base import infer_urgency_and_text


def run_medical_tests(cases: dict) -> None:
    print("=== Медицинская система (kanren) ===")
    total = 0
    failed = 0

    for case in cases.get("medical_triage", []):
        total += 1
        name = case["name"]
        symptoms = case["input"]
        expected = case["expected_urgency"]

        urgency, _ = infer_urgency_and_text(symptoms)

        ok = urgency == expected
        status = "OK" if ok else "FAIL"
        print(f"{name}: {urgency} (ожидалось: {expected}) -> {status}")

        if not ok:
            failed += 1

    print(f"\nИТОГО: {total} сценариев, ошибок: {failed}\n")


def main():
    with open("test_cases.yml", "r", encoding="utf-8") as f:
        cases = yaml.safe_load(f)

    run_medical_tests(cases)


if __name__ == "__main__":
    main()
