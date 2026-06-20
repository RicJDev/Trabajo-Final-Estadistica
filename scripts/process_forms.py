import os
import json
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


def get_questions(form_id):
    form = service.forms().get(formId=form_id).execute()
    questions = {}
    if "items" in form:
        for item in form["items"]:
            if "questionItem" in item:
                q_id = item["questionItem"]["question"]["questionId"]
                title = item["title"]
                questions[q_id] = title
    return questions


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


def extract_answer_values(answer):
    values = []
    if "textAnswers" in answer:
        for ans in answer["textAnswers"]["answers"]:
            values.append(ans["value"])
    elif "fileUploadAnswers" in answer:
        for ans in answer["fileUploadAnswers"]["answers"]:
            values.append(ans["fileId"])
    return values


def process_form(form_id, output_filename):
    if not form_id:
        print(f"ID de formulario vacío, saltando...")
        return

    questions = get_questions(form_id)
    responses = get_all_responses(form_id)

    form_answers = {}

    for resp in responses:
        answers_dict = resp.get("answers", {})
        for q_id, answer in answers_dict.items():
            question_text = questions.get(q_id, q_id)
            values = extract_answer_values(answer)
            if not values:
                continue
            if question_text not in form_answers:
                form_answers[question_text] = []
            form_answers[question_text].extend(values)

    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(form_answers, f, indent=2, ensure_ascii=False)

    print(f"Archivo {output_filename} generado con {len(form_answers)} preguntas.")


if __name__ == "__main__":
    process_form(STUDENTS_FORM, "data/students_answers.json")
    process_form(GRADUATES_FORM, "data/graduates_answers.json")
