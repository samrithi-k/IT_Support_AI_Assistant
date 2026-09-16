import json
import re
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

KNOWLEDGE_BASE_PATH = (
    BASE_DIR / "data" / "knowledge_base.json"
)


def load_knowledge_base():

    with open(
        KNOWLEDGE_BASE_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def tokenize(text):

    return set(
        re.findall(
            r"\b[a-zA-Z0-9-]+\b",
            text.lower()
        )
    )


def retrieve_context(question, top_k=3):

    knowledge_base = load_knowledge_base()

    question_words = tokenize(question)

    scored_items = []


    for item in knowledge_base:

        searchable_text = " ".join(
            [item["problem"]] +
            item["keywords"]
        )

        item_words = tokenize(
            searchable_text
        )

        score = len(
            question_words.intersection(
                item_words
            )
        )

        if score > 0:

            scored_items.append(
                (score, item)
            )


    scored_items.sort(
        key=lambda item: item[0],
        reverse=True
    )


    selected_items = [
        item
        for _, item in scored_items[:top_k]
    ]


    if not selected_items:

        return (
            "No directly matching knowledge-base "
            "entry was found."
        )


    context_parts = []


    for item in selected_items:

        context_parts.append(
            f"Problem: {item['problem']}\n"
            f"Solution: {item['solution']}"
        )


    return "\n\n".join(context_parts)