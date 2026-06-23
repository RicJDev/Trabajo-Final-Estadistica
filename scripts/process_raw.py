import json
import os
import re
from collections import Counter, defaultdict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def camel_to_snake(name):
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    s2 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1)
    return s2.lower()


DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(os.path.dirname(BASE_DIR), "public", "json_data")

STUDENTS_RAW = os.path.join(DATA_DIR, "raw_students_responses.json")
GRADUATES_RAW = os.path.join(DATA_DIR, "raw_graduates_responses.json")


def load_data(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def count_answers_by_question(responses):
    from utils import LABEL_CLEANUP

    counts = defaultdict(Counter)
    for r in responses:
        for qid, answer in r.get("answers", {}).items():
            if "textAnswers" in answer:
                for ans in answer["textAnswers"]["answers"]:
                    val = ans.get("value", "").strip()
                    if val:
                        val = LABEL_CLEANUP.get(val, val)
                        counts[qid][val] += 1
    return counts


QUESTION_MAP_STUDENTS = {
    "4ef35c1a": "est_lenguajes",
    "146d6517": "est_frameworks",
    "096600b7": "est_area_aspirada",
    "0fba86b0": "est_horas_autonomas",
    "083ae2d9": "est_factor_empleo",
    "7902ee66": "est_impacto_ia",
    "25a71b67": "est_meta_graduacion",
    "18a0872c": "est_frecuencia_ia",
    "7d845f08": "est_semestre",
}

QUESTION_MAP_GRADUATES = {
    "5b46c850": "grad_anos_graduacion",
    "37b9dc70": "grad_trabaja_sector",
    "028a9705": "grad_rol",
    "5e9090b4": "grad_tiempo_empleo",
    "532b020d": "grad_nivel_ingles",
    "7a5496a6": "grad_frecuencia_ia",
    "2524b367": "grad_impacto_ia",
    "57068564": "grad_factor_seleccion",
    "7c745229": "grad_lenguajes",
    "69842ab6": "grad_frameworks",
}


def save_chart_data(filename, labels, values):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"labels": labels, "values": values}, f, indent=2, ensure_ascii=False)
    print(f"  Saved {path}")


def save_comparison_data(filename, labels, dataset_a, dataset_b):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({
            "labels": labels,
            "datasets": [dataset_a, dataset_b],
        }, f, indent=2, ensure_ascii=False)
    print(f"  Saved {path}")


def align_labels(counter_a, counter_b, top_n=15):
    all_labels = set(counter_a.keys()) | set(counter_b.keys())
    sorted_labels = sorted(
        all_labels,
        key=lambda l: counter_a.get(l, 0) + counter_b.get(l, 0),
        reverse=True,
    )[:top_n]
    return sorted_labels


def build_comparison_ia_frecuencia(student_counter, graduate_counter):
    mapping = {
        "Diariamente (Es parte fundamental de mi método de estudio)": "Diariamente",
        "Diariamente (Están completamente integradas en mi flujo de trabajo regular)": "Diariamente",
        "Ocasionalmente (1 o 2 veces por semana)": "Ocasionalmente",
        "Ocasionalmente (Para consultas puntuales, revisión de errores o refactorización)": "Ocasionalmente",
        "Rara vez (1 o 2 veces al mes)": "Rara vez / Nunca",
        "Nunca": "Rara vez / Nunca",
    }
    norm_s = defaultdict(int)
    norm_g = defaultdict(int)
    for k, v in student_counter.items():
        norm_s[mapping.get(k, k)] += v
    for k, v in graduate_counter.items():
        norm_g[mapping.get(k, k)] += v
    labels = sorted(set(norm_s.keys()) | set(norm_g.keys()),
                    key=lambda l: norm_s.get(l, 0) + norm_g.get(l, 0), reverse=True)
    return labels, list(norm_s.get(l, 0) for l in labels), list(norm_g.get(l, 0) for l in labels)


def build_heatmap(student_responses):
    from utils import LABEL_CLEANUP

    heatmap_data = defaultdict(lambda: defaultdict(int))

    for r in student_responses:
        langs = set()
        frameworks = set()
        answers = r.get("answers", {})
        if "4ef35c1a" in answers:
            for ans in answers["4ef35c1a"]["textAnswers"]["answers"]:
                val = ans.get("value", "").strip()
                if val and val != "Otro":
                    langs.add(LABEL_CLEANUP.get(val, val))
        if "146d6517" in answers:
            for ans in answers["146d6517"]["textAnswers"]["answers"]:
                val = ans.get("value", "").strip()
                if val and val != "Otro":
                    frameworks.add(LABEL_CLEANUP.get(val, val))

        for l in langs:
            for f in frameworks:
                heatmap_data[l][f] += 1

    top_langs = sorted(heatmap_data.keys(), key=lambda x: sum(heatmap_data[x].values()), reverse=True)[:10]
    top_frameworks = sorted(
        {f for v in heatmap_data.values() for f in v},
        key=lambda f: sum(heatmap_data[l][f] for l in heatmap_data),
        reverse=True,
    )[:10]

    y_labels = top_langs
    x_labels = top_frameworks
    data_matrix = [[heatmap_data[l][f] for f in x_labels] for l in y_labels]

    path = os.path.join(OUTPUT_DIR, "heatmap_lenguajes_frameworks.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "xLabels": x_labels,
                "yLabels": y_labels,
                "data": data_matrix,
                "title": "Lenguajes vs Frameworks (Estudiantes)",
            },
            f,
            indent=2,
            ensure_ascii=False,
        )
    print(f"  Saved {path}")


def build_graduate_insights(graduate_counts, graduate_responses):
    insights = {}

    def top_n(counter, n=5):
        return [{"label": k, "count": v} for k, v in counter.most_common(n)]

    total_grad = len(graduate_responses)

    trabaja_sector = graduate_counts.get("37b9dc70", Counter()).get("Sí", 0)
    usa_ia_diario = graduate_counts.get("7a5496a6", Counter()).get(
        "Diariamente (Están completamente integradas en mi flujo de trabajo regular)", 0
    )

    insights["egresados"] = {
        "total": total_grad,
        "top_lenguajes": top_n(graduate_counts.get("7c745229", Counter())),
        "top_frameworks": top_n(graduate_counts.get("69842ab6", Counter())),
        "top_rol": top_n(graduate_counts.get("028a9705", Counter())),
        "top_factor_seleccion": top_n(graduate_counts.get("57068564", Counter())),
        "top_tiempo_empleo": top_n(graduate_counts.get("5e9090b4", Counter())),
        "top_nivel_ingles": top_n(graduate_counts.get("532b020d", Counter())),
        "frecuencia_ia": top_n(graduate_counts.get("7a5496a6", Counter())),
        "impacto_ia": top_n(graduate_counts.get("2524b367", Counter())),
        "trabaja_sector_pct": round(
            (trabaja_sector / total_grad) * 100, 1
        ) if total_grad else 0,
        "usa_ia_diario_pct": round(
            (usa_ia_diario / total_grad) * 100, 1
        ) if total_grad else 0,
    }
    return insights


def build_insights(student_counts, student_responses):
    insights = {}

    def top_n(counter, n=5):
        return [{"label": k, "count": v} for k, v in counter.most_common(n)]

    total_est = len(student_responses)

    uso_diario_ia_est = student_counts.get("18a0872c", Counter()).get(
        "Diariamente (Es parte fundamental de mi método de estudio)", 0
    )
    impacto_positivo_est = student_counts.get("7902ee66", Counter()).get(
        "Será una herramienta obligatoria que aumentará la productividad, pero no reemplazará el rol", 0
    )

    insights["estudiantes"] = {
        "total": total_est,
        "top_lenguajes": top_n(student_counts.get("4ef35c1a", Counter())),
        "top_frameworks": top_n(student_counts.get("146d6517", Counter())),
        "top_areas": top_n(student_counts.get("096600b7", Counter())),
        "distribucion_horas": top_n(student_counts.get("0fba86b0", Counter())),
        "factor_empleo": top_n(student_counts.get("083ae2d9", Counter())),
        "impacto_ia": top_n(student_counts.get("7902ee66", Counter())),
        "frecuencia_ia": top_n(student_counts.get("18a0872c", Counter())),
        "meta_graduacion": top_n(student_counts.get("25a71b67", Counter())),
        "uso_diario_ia_pct": round(
            (uso_diario_ia_est / total_est) * 100, 1
        ) if total_est else 0,
        "impacto_positivo_ia_pct": round(
            (impacto_positivo_est / total_est) * 100, 1
        ) if total_est else 0,
    }

    return insights


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    student_responses = load_data(STUDENTS_RAW)
    student_counts = count_answers_by_question(student_responses)

    print("Generating student charts...")
    for qid, name in QUESTION_MAP_STUDENTS.items():
        counter = student_counts.get(qid, Counter())
        labels = [k for k, _ in counter.most_common()]
        values = [v for _, v in counter.most_common()]
        save_chart_data(f"{name}.json", labels, values)

    print("Generating heatmap...")
    build_heatmap(student_responses)

    print("Generating student insights...")
    insights = build_insights(student_counts, student_responses)

    print("\nGenerating graduate charts...")
    graduate_responses = load_data(GRADUATES_RAW)
    graduate_counts = count_answers_by_question(graduate_responses)
    for qid, name in QUESTION_MAP_GRADUATES.items():
        counter = graduate_counts.get(qid, Counter())
        labels = [k for k, _ in counter.most_common()]
        values = [v for _, v in counter.most_common()]
        save_chart_data(f"{name}.json", labels, values)

    print("\nGenerating graduate insights...")
    grad_insights = build_graduate_insights(graduate_counts, graduate_responses)
    insights.update(grad_insights)

    path = os.path.join(OUTPUT_DIR, "insights.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(insights, f, indent=2, ensure_ascii=False)
    print(f"  Saved {path}")

    print("\nGenerating comparison charts...")
    total_est = len(student_responses)
    total_grad = len(graduate_responses)

    # Lenguajes
    sc = student_counts.get("4ef35c1a", Counter())
    gc = graduate_counts.get("7c745229", Counter())
    labels = align_labels(sc, gc)
    s_pct = [round(sc.get(l, 0) / total_est * 100, 1) for l in labels]
    g_pct = [round(gc.get(l, 0) / total_grad * 100, 1) for l in labels]
    save_comparison_data("comparativa_lenguajes.json", labels,
                         {"label": "Estudiantes", "data": s_pct, "color": "#3b82f6"},
                         {"label": "Egresados", "data": g_pct, "color": "#10b981"})

    # Frameworks
    sc = student_counts.get("146d6517", Counter())
    gc = graduate_counts.get("69842ab6", Counter())
    labels = align_labels(sc, gc)
    s_pct = [round(sc.get(l, 0) / total_est * 100, 1) for l in labels]
    g_pct = [round(gc.get(l, 0) / total_grad * 100, 1) for l in labels]
    save_comparison_data("comparativa_frameworks.json", labels,
                         {"label": "Estudiantes", "data": s_pct, "color": "#3b82f6"},
                         {"label": "Egresados", "data": g_pct, "color": "#10b981"})

    # Frecuencia IA
    sc = student_counts.get("18a0872c", Counter())
    gc = graduate_counts.get("7a5496a6", Counter())
    labels, s_data, g_data = build_comparison_ia_frecuencia(sc, gc)
    s_pct = [round(v / total_est * 100, 1) for v in s_data]
    g_pct = [round(v / total_grad * 100, 1) for v in g_data]
    save_comparison_data("comparativa_frecuencia_ia.json", labels,
                         {"label": "Estudiantes", "data": s_pct, "color": "#3b82f6"},
                         {"label": "Egresados", "data": g_pct, "color": "#10b981"})

    print(f"\nAll files generated in '{OUTPUT_DIR}/'")


if __name__ == "__main__":
    main()
