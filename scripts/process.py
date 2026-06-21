import json
from collections import defaultdict

from api import get_all_responses, get_questions_info
from utils import extract_answer_values


def save_raw_responses(form_id, raw_filename):
    if not form_id:
        print(f"ID de formulario vacío, saltando...")
        return

    responses = get_all_responses(form_id)
    with open(raw_filename, "w", encoding="utf-8") as f:
        json.dump(responses, f, indent=2, ensure_ascii=False)
    print(f"Respuestas crudas guardadas en {raw_filename} ({len(responses)} respuestas)")


def process_raw_responses(raw_filename, form_id, output_filename):
    if not form_id:
        print(f"ID de formulario vacío, saltando...")
        return

    questions_info = get_questions_info(form_id)

    with open(raw_filename, "r", encoding="utf-8") as f:
        responses = json.load(f)

    actual_counts = defaultdict(lambda: defaultdict(int))

    for resp in responses:
        answers_dict = resp.get("answers", {})
        for q_id, answer in answers_dict.items():
            values = extract_answer_values(answer)
            for value in values:
                if value:
                    actual_counts[q_id][value] += 1

    form_answers = {}
    for q_info in questions_info:
        q_id = q_info["id"]
        title = q_info["title"]
        choices = q_info["choices"]

        if choices is not None:
            answer_counts = {choice: 0 for choice in choices}
        else:
            answer_counts = {}

        if q_id in actual_counts:
            for ans, cnt in actual_counts[q_id].items():
                answer_counts[ans] = cnt

        form_answers[title] = answer_counts

    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(form_answers, f, indent=2, ensure_ascii=False)

    print(
        f"Archivo {output_filename} generado con {len(form_answers)} preguntas.")
