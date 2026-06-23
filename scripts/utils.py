LABEL_CLEANUP = {
    "JavaScript / TypeScript": "JavaScript",
    "C++ / C": "C++",
    "C / C++": "C++",
    "SQL (PostgreSQL, MySQL, etc.)": "SQL",
    "Node.js (Express, NestJS)": "Node.js",
    "React / Next.js": "React",
    "Desarrollo Web Frontend": "Desarrollo Frontend",
    "Ciberseguridad": "Ciberseguridad / Pen Testing",
}


def clean_labels(labels, values):
    from collections import defaultdict

    merged = defaultdict(int)
    for label, value in zip(labels, values):
        canonical = LABEL_CLEANUP.get(label, label)
        merged[canonical] += value
    sorted_items = sorted(merged.items(), key=lambda x: x[1], reverse=True)
    return [item[0] for item in sorted_items], [item[1] for item in sorted_items]


def extract_answer_values(answer):
    values = []
    if "textAnswers" in answer:
        for ans in answer["textAnswers"]["answers"]:
            values.append(ans["value"])
    elif "fileUploadAnswers" in answer:
        for ans in answer["fileUploadAnswers"]["answers"]:
            values.append(ans["fileId"])
    return values
