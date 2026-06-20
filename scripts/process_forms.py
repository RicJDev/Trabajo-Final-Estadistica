import os
import json
from collections import defaultdict
from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
from dotenv import load_dotenv

load_dotenv()

STUDENTS_FORM = os.getenv("STUDENTS_FORM", "")
GRADUATES_FORM = os.getenv("GRADUATES_FORM", "")

SCOPES = [
    "https://www.googleapis.com/auth/forms.responses.readonly",
    "https://www.googleapis.com/auth/forms.body.readonly"
]
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

store = file.Storage("token.json")
creds = None
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets(
        "credentials.json", SCOPES, redirect_uri="http://localhost:8080/"
    )
    creds = tools.run_flow(flow, store)

service = discovery.build(
    "forms",
    "v1",
    http=creds.authorize(Http()),
    discoveryServiceUrl=DISCOVERY_DOC,
    static_discovery=False,
)


def get_questions_info(form_id):
    form = service.forms().get(formId=form_id).execute()

    questions = []
    if "items" in form:
        for item in form["items"]:
            if "questionItem" in item:
                q = item["questionItem"]["question"]
                q_id = q.get("questionId")
                title = item.get("title", "")
                choices = None

                if "choiceQuestion" in q:
                    choice_info = q["choiceQuestion"]
                    if "options" in choice_info:
                        choices = [opt.get("value", "")
                                   for opt in choice_info["options"]]

                questions.append({
                    "id": q_id,
                    "title": title,
                    "choices": choices
                })
    return questions


def extract_answer_values(answer):
    values = []
    if "textAnswers" in answer:
        for ans in answer["textAnswers"]["answers"]:
            values.append(ans["value"])
    elif "fileUploadAnswers" in answer:
        for ans in answer["fileUploadAnswers"]["answers"]:
            values.append(ans["fileId"])
    return values


def get_all_responses(form_id):
    responses = []
    page_token = None
    while True:
        params = {"formId": form_id, "pageSize": 500}
        if page_token:
            params["pageToken"] = page_token
        result = service.forms().responses().list(**params).execute()
        if "responses" in result:
            responses.extend(result["responses"])
        page_token = result.get("nextPageToken")
        if not page_token:
            break
    return responses


def process_form(form_id, output_filename):
    if not form_id:
        print(f"ID de formulario vacío, saltando...")
        return

    questions_info = get_questions_info(form_id)

    responses = get_all_responses(form_id)
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

    # 4. Guardar a JSON
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(form_answers, f, indent=2, ensure_ascii=False)

    print(
        f"Archivo {output_filename} generado con {len(form_answers)} preguntas.")


if __name__ == "__main__":
    process_form(STUDENTS_FORM, "data/students_answers.json")
    process_form(GRADUATES_FORM, "data/graduates_answers.json")
