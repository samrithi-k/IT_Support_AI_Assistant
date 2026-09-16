import json
import re
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

KNOWLEDGE_BASE_PATH = (
    BASE_DIR / "data" / "knowledge_base.json"
)


STOP_WORDS = {
    "i",
    "me",
    "my",
    "the",
    "a",
    "an",
    "is",
    "are",
    "am",
    "was",
    "were",
    "do",
    "does",
    "did",
    "how",
    "what",
    "why",
    "can",
    "could",
    "would",
    "should",
    "to",
    "of",
    "for",
    "in",
    "on",
    "with",
    "and",
    "or",
    "but",
    "it",
    "this",
    "that",
    "have",
    "has",
    "been",
    "be",
    "please"
}


def load_knowledge_base():

    with open(
        KNOWLEDGE_BASE_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def tokenize(text):

    words = re.findall(
        r"\b[a-zA-Z0-9]+\b",
        text.lower()
    )

    return {
        word
        for word in words
        if word not in STOP_WORDS
    }


def retrieve_context(question):

    knowledge_base = load_knowledge_base()

    question_words = tokenize(question)

    if not question_words:

        return (
            "No relevant knowledge-base information "
            "was found for this question."
        )


    scored_items = []


    for item in knowledge_base:

        searchable_text = " ".join(
            [
                item["problem"],
                *item["keywords"]
            ]
        )

        item_words = tokenize(searchable_text)

        matching_words = (
            question_words.intersection(item_words)
        )

        score = len(matching_words)


        if score > 0:

            scored_items.append(
                (score, item)
            )


    scored_items.sort(
        key=lambda item: item[0],
        reverse=True
    )


    # Require at least two meaningful matching words
    if (
        not scored_items
        or scored_items[0][0] < 2
    ):

        return (
            "No relevant knowledge-base information "
            "was found for this question."
        )


    # Return only the strongest match
    best_item = scored_items[0][1]


    return (
        f"Problem: {best_item['problem']}\n"
        f"Solution: {best_item['solution']}"
    )