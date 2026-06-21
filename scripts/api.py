from config import service


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
