def extract_answer_values(answer):
    values = []
    if "textAnswers" in answer:
        for ans in answer["textAnswers"]["answers"]:
            values.append(ans["value"])
    elif "fileUploadAnswers" in answer:
        for ans in answer["fileUploadAnswers"]["answers"]:
            values.append(ans["fileId"])
    return values
