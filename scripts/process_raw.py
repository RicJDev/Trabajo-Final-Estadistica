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
OUTPUT_DIR = os.path.join(BASE_DIR, "json_data")

STUDENTS_RAW = os.path.join(DATA_DIR, "raw_students_responses.json")


def load_data(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def count_answers_by_question(responses):
    counts = defaultdict(Counter)
    for r in responses:
        for qid, answer in r.get("answers", {}).items():
            if "textAnswers" in answer:
                for ans in answer["textAnswers"]["answers"]:
                    val = ans.get("value", "").strip()
                    if val:
                        counts[qid][val] += 1
    return counts


QUESTION_MAP_STUDENTS = {
    "4ef35c1a": "estLenguajes",
    "146d6517": "estFrameworks",
    "096600b7": "estAreaAspirada",
    "0fba86b0": "estHorasAutonomas",
    "083ae2d9": "estFactorEmpleo",
    "7902ee66": "estImpactoIa",
    "25a71b67": "estMetaGraduacion",
    "18a0872c": "estFrecuenciaIa",
}


def save_chart_data(filename, labels, values):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"labels": labels, "values": values}, f, indent=2, ensure_ascii=False)
    print(f"  Saved {path}")


def build_heatmap(student_responses):
    heatmap_data = defaultdict(lambda: defaultdict(int))

    for r in student_responses:
        langs = set()
        frameworks = set()
        answers = r.get("answers", {})
        if "4ef35c1a" in answers:
            for ans in answers["4ef35c1a"]["textAnswers"]["answers"]:
                val = ans.get("value", "").strip()
                if val and val != "Otro":
                    langs.add(val)
        if "146d6517" in answers:
            for ans in answers["146d6517"]["textAnswers"]["answers"]:
                val = ans.get("value", "").strip()
                if val and val != "Otro":
                    frameworks.add(val)

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

    path = os.path.join(OUTPUT_DIR, "insights.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(insights, f, indent=2, ensure_ascii=False)
    print(f"  Saved {path}")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    student_responses = load_data(STUDENTS_RAW)
    student_counts = count_answers_by_question(student_responses)

    print("Generating student charts...")
    for qid, name in QUESTION_MAP_STUDENTS.items():
        counter = student_counts.get(qid, Counter())
        labels = [k for k, _ in counter.most_common()]
        values = [v for _, v in counter.most_common()]
        save_chart_data(f"{camel_to_snake(name)}.json", labels, values)

    print("Generating heatmap...")
    build_heatmap(student_responses)

    print("Generating insights...")
    build_insights(student_counts, student_responses)

    print(f"\nAll files generated in '{OUTPUT_DIR}/'")


if __name__ == "__main__":
    main()
