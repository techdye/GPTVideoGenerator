import json
from pathlib import Path

import openai

KEY_FILE = Path(__file__).parents[1] / "token" / "token.json"

with open(KEY_FILE, "r") as f:
    openai.api_key = json.load(f)["key"]


def ask(text, max_tokens=1000, model="text-davinci-003") -> str:
    response = openai.Completion.create(
        engine=model,
        prompt=text,
        max_tokens=max_tokens,
    )

    return response.choices[0]['text']


def split(delimiters, string):
    import re
    regex_pattern = '|'.join(map(re.escape, delimiters))
    return re.split(regex_pattern, string, 0)
