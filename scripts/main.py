from config import STUDENTS_FORM, GRADUATES_FORM
from process import save_raw_responses

if __name__ == "__main__":
    save_raw_responses(STUDENTS_FORM, "data/raw_students_responses.json")
    save_raw_responses(GRADUATES_FORM, "data/raw_graduates_responses.json")
