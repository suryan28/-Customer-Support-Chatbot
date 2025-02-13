import os
import json

current_directory = os.path.dirname(os.path.abspath(__file__))


def load_qna_files():
    answers_file = os.path.join(os.path.dirname(__file__), "..", "db", "answers.json")

    with open(answers_file, 'r', encoding='utf-8') as answers:  # Specify encoding
        data = json.load(answers)
    return data


def get_qna_keywords():
    qna = load_qna_files()

    keywords_list = [keyword.strip().lower() for keywords_str in qna["KEYWORDS"].keys() for keyword in keywords_str.split('/')]
    keywords_dict = {f"key{i + 1}": keyword for i, keyword in enumerate(qna['KEYWORDS'].keys())}
    content_dict = {f"key{i + 1}": content for i, content in enumerate(qna['KEYWORDS'].values())}
    return keywords_dict, content_dict, keywords_list


qnas = get_qna_keywords()


def get_qna():
    return {"keywords_dict": qnas[0], "content_dict": qnas[1],
            "keywords_list": qnas[2]}
