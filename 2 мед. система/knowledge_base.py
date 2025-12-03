#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
knowledge_base.py
Знаниевая база и логический вывод для учебной мед. экспертной системы
на kanren (logpy).

ВНИМАНИЕ: не медицинский совет.
"""

from kanren import Relation, facts, run, var

# ---------------------------------
#   ОПРЕДЕЛЯЕМ РЕЛЯЦИЮ ПРАВИЛ
# ---------------------------------

# rule_urgency(urgency, flag, text)
#   urgency: 'emergency' | 'urgent' | 'doctor' | 'home'
#   flag: строковый идентификатор симптоматического паттерна
#   text: текстовое объяснение
rule_urgency = Relation()

facts(
    rule_urgency,

    # ===== ЭКСТРЕННЫЕ СОСТОЯНИЯ =====
    ('emergency', 'breathing_difficulty',
     "Отмечены выражённые затруднения дыхания. "
     "Это потенциально опасное для жизни состояние. "
     "Немедленно вызовите скорую помощь (103/112)."),

    ('emergency', 'chest_pain',
     "Боль или давление в груди. "
     "Это может быть признаком инфаркта миокарда, тромбоэмболии или другой "
     "опасной патологии. Немедленно вызовите скорую помощь (103/112)."),

    ('emergency', 'confusion',
     "Есть признаки спутанности сознания или дезориентации. "
     "Это может быть инсульт, тяжёлая инфекция или другое экстренное состояние. "
     "Нужна немедленная медицинская помощь."),

    ('emergency', 'head_trauma_with_symptoms',
     "Недавняя травма головы в сочетании с болью, температурой или другими "
     "жалобами. Это требует срочного осмотра в приёмном отделении/травмпункте "
     "или вызова скорой помощи."),

    ('emergency', 'bleeding',
     "Сообщается о значительном кровотечении. "
     "Это может быть опасно для жизни. Немедленно вызовите скорую помощь."),

    ('emergency', 'very_high_fever_infant',
     "Очень высокая температура у младенца. "
     "Это потенциально опасное состояние. Необходимо срочно обратиться "
     "за экстренной медицинской помощью."),

    ('emergency', 'very_high_fever_elderly_chronic',
     "Очень высокая температура у пожилого человека или пациента "
     "с тяжёлым хроническим заболеванием. Это может быть признаком "
     "тяжёлой инфекции или декомпенсации. Требуется экстренная помощь."),

    # ===== СРОЧНО (В БЛИЖАЙШИЕ ЧАСЫ/ДЕНЬ) =====
    ('urgent', 'high_fever_child',
     "Высокая температура у ребёнка. "
     "Рекомендуется обратиться к педиатру в тот же день или как можно скорее."),

    ('urgent', 'high_fever_elderly',
     "Высокая температура у пожилого человека. "
     "Рекомендуется срочная консультация врача (вызов врача на дом или "
     "обращение в поликлинику/приёмное отделение)."),

    ('urgent', 'high_fever_adult',
     "У взрослого высокая температура. "
     "Рекомендуется осмотр врача в ближайшее время, особенно если симптомы "
     "держатся более суток или усиливаются."),

    ('urgent', 'severe_pain',
     "Выраженная (сильная) боль даже без других \"красных флагов\" "
     "требует осмотра врача в ближайшие часы."),

    ('urgent', 'abdominal_pain',
     "Сильная боль в животе может быть признаком аппендицита, панкреатита "
     "или другой серьёзной патологии. Рекомендуется срочно обратиться к врачу."),

    ('urgent', 'rash_with_high_fever',
     "Высыпания на коже в сочетании с высокой температурой. "
     "Это может быть проявлением инфекционных или аллергических заболеваний, "
     "требующих срочной оценки."),

    ('urgent', 'rash_with_mild_fever',
     "Высыпания на коже в сочетании с небольшой температурой. "
     "Рекомендуется консультация врача в ближайшее время."),

    ('urgent', 'pregnancy_moderate_symptoms',
     "При беременности умеренная боль, повышение температуры или другие "
     "выраженные симптомы требуют быстрого контакта с врачом или акушером-гинекологом."),

    ('urgent', 'high_fever_chronic',
     "Высокая температура на фоне серьёзных хронических заболеваний "
     "(сердце, лёгкие, диабет и др.). Рекомендуется срочная консультация врача."),

    ('urgent', 'dehydration_with_fever',
     "Есть признаки обезвоживания на фоне повышенной температуры. "
     "Это может быть опасно, особенно для детей и пожилых. Нужен осмотр врача."),

    # ===== ПЛАНОВАЯ КОНСУЛЬТАЦИЯ ВРАЧА =====
    ('doctor', 'moderate_pain',
     "Боль умеренной интенсивности без явных опасных признаков. "
     "Рекомендуется плановая консультация врача в ближайшие дни."),

    ('doctor', 'mild_fever_chronic',
     "Небольшая температура у пациента с хроническими заболеваниями. "
     "Желательно обсудить ситуацию с лечащим врачом для корректировки терапии."),

    ('doctor', 'rash_without_fever',
     "Высыпания на коже без повышения температуры. "
     "Чаще всего это не экстренная ситуация, но требуется плановый осмотр врача "
     "(дерматолога или терапевта)."),

    ('doctor', 'dehydration_without_fever',
     "Есть признаки лёгкого обезвоживания без высокой температуры. "
     "Рекомендуется увеличить приём жидкости и при сохранении симптомов "
     "обратиться к врачу."),

    # ===== НИЗКАЯ СРОЧНОСТЬ / ДОМАШНЕЕ НАБЛЮДЕНИЕ =====
    ('home', 'low_risk',
     "По текущим данным ситуация выглядит как низкой срочности. "
     "Можно наблюдать состояние дома, соблюдать общие рекомендации "
     "(обильное питьё, отдых). При любом ухудшении или появлении новых "
     "симптомов необходимо обратиться к врачу.")
)

# приоритет уровней срочности (чем меньше число, тем серьёзнее)
URGENCY_PRIORITY = {
    'emergency': 0,
    'urgent': 1,
    'doctor': 2,
    'home': 3,
}


def infer_flags_from_symptoms(symptoms):
    """
    На вход: словарь с сырыми симптомами (внутренние коды).
    На выход: список "флагов" (строк), которые описывают паттерны.
    """
    flags = []

    age = symptoms["age"]         # infant / child / adult / elderly
    fever = symptoms["fever"]     # none / mild / high / very_high
    pain = symptoms["pain"]       # none / mild / moderate / severe

    chest_pain = symptoms["chest_pain"]
    breath = symptoms["breath"]
    confusion = symptoms["confusion"]
    dehydration = symptoms["dehydration"]
    rash = symptoms["rash"]
    abd_pain = symptoms["abd_pain"]
    head_trauma = symptoms["head_trauma"]
    bleeding = symptoms["bleeding"]
    pregnancy = symptoms["pregnancy"]
    chronic = symptoms["chronic"]

    # ----- экстренные флаги -----
    if breath:
        flags.append("breathing_difficulty")
    if chest_pain:
        flags.append("chest_pain")
    if confusion:
        flags.append("confusion")
    if head_trauma and (pain in ("moderate", "severe") or fever in ("high", "very_high")):
        flags.append("head_trauma_with_symptoms")
    elif head_trauma:
        # травма головы без серьёзных дополнительных признаков — всё равно опасный сигнал
        flags.append("head_trauma_with_symptoms")
    if bleeding:
        flags.append("bleeding")

    if age == "infant" and fever == "very_high":
        flags.append("very_high_fever_infant")
    if fever == "very_high" and (age == "elderly" or chronic):
        flags.append("very_high_fever_elderly_chronic")

    # ----- срочные флаги -----
    if age == "child" and fever == "high":
        flags.append("high_fever_child")
    if age == "elderly" and fever == "high":
        flags.append("high_fever_elderly")
    if age == "adult" and fever == "high":
        flags.append("high_fever_adult")

    if pain == "severe":
        flags.append("severe_pain")
    if abd_pain and pain in ("moderate", "severe"):
        flags.append("abdominal_pain")

    if rash and fever in ("high", "very_high"):
        flags.append("rash_with_high_fever")
    elif rash and fever == "mild":
        flags.append("rash_with_mild_fever")
    elif rash and fever == "none":
        flags.append("rash_without_fever")

    if pregnancy and pain in ("moderate", "severe"):
        flags.append("pregnancy_moderate_symptoms")

    if chronic and fever == "high":
        flags.append("high_fever_chronic")
    if chronic and fever == "mild":
        flags.append("mild_fever_chronic")

    if dehydration and fever in ("mild", "high", "very_high"):
        flags.append("dehydration_with_fever")
    elif dehydration and fever == "none":
        flags.append("dehydration_without_fever")

    # ----- плановая консультация / низкий риск -----
    # Если есть умеренная боль, но не было более серьёзных флагов
    if pain == "moderate":
        flags.append("moderate_pain")

    # Low risk — если ни один серьёзный флаг не был добавлен
    dangerous_flags = {
        "breathing_difficulty", "chest_pain", "confusion", "head_trauma_with_symptoms",
        "bleeding", "very_high_fever_infant", "very_high_fever_elderly_chronic",
        "high_fever_child", "high_fever_elderly", "high_fever_adult",
        "severe_pain", "abdominal_pain", "rash_with_high_fever",
        "pregnancy_moderate_symptoms", "high_fever_chronic", "dehydration_with_fever",
    }
    if not any(f in dangerous_flags for f in flags):
        flags.append("low_risk")

    return flags


def infer_urgency_and_text(symptoms):
    """
    Основной вывод:
      1) строим список флагов;
      2) через kanren ищем все (urgency, text) для этих флагов;
      3) выбираем наиболее серьёзный уровень по URGENCY_PRIORITY.
    """
    flags = infer_flags_from_symptoms(symptoms)
    urgency_results = []  # (urgency, text, flag)

    for flag in flags:
        u = var()
        t = var()
        found_urgencies = run(0, u, rule_urgency(u, flag, t))
        for urg in found_urgencies:
            texts = run(0, t, rule_urgency(urg, flag, t))
            for txt in texts:
                urgency_results.append((urg, txt, flag))

    if not urgency_results:
        return (
            "doctor",
            "Система не смогла отнести ситуацию к типичным категориям. "
            "Рекомендуется проконсультироваться с врачом и при ухудшении состояния "
            "немедленно обратиться за медицинской помощью."
        )

    best = min(urgency_results, key=lambda r: URGENCY_PRIORITY.get(r[0], 99))
    urgency, text, _flag = best
    return urgency, text
