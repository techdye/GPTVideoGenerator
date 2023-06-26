import json
from pathlib import Path

import typer
from rich import print

import utils.file_management
import utils.chat


def main(number_words: int,
         language: str,
         max_tokens: int,
         model: str,
         stop_create_files: bool = True,
         delete_files: bool = True,
         warning_sources: bool = True,
         write_empty: bool = True):
    created_elements = utils.file_management.create_files(files=["sources.json", "settings.json"],
                                                          folders=[str(Path("temp") / "images"),
                                                                   str(Path("temp") / "audio"), "output", "settings"],
                                                          main_path=Path(__file__).parents[0])

    if (created_elements[0] or created_elements[1]) and stop_create_files:
        print("Restart the program! Elements are creating.")
        raise typer.Exit()

    sources = Path(__file__).parents[0] / "sources.json"

    if not sources.read_text():
        print("Nothing is in the sources.json file.")

        if write_empty:
            sources.write_text("[]")

        raise typer.Exit()

    settings = Path(__file__).parents[0] / "settings.json"

    if not settings.read_text():
        with open(settings, "w") as f:
            dictionary = {
                "prompt": r"Generate a script for a video with the sources that I give to you."
                          r"The video needs to be {words} words. You are a top write. You need"
                          r"to adapt to the script. Don't say what you think and be kind."
                          r"Make a intro that show the subject in a very intense way."
                          r"Do it in {language} :"
            }
            json.dump(dictionary, f, indent=4)

    if warning_sources:
        delete = typer.confirm("Did you format correctly sources in a json list?")

        if not delete:
            print("Format correctly it.")
            raise typer.Exit()

    with open(settings, "r") as settings_f:
        with open(sources, "r") as sources_f:
            prompt = json.load(settings_f)["prompt"].replace("{words}", str(number_words)).replace("{language}",
                                                                                                   str(language))
            prompt += "First article - " + "\nNew article - ".join(json.load(sources_f))

    verification = False
    sentences = []

    while not verification or not sentences:
        sentences = [i.replace("\n", "") for i in utils.chat.split(r"!\.\?", utils.chat.ask(prompt, max_tokens, model))
                     if i]

        print(sentences)

        verification = typer.confirm("It's a good prompt for you?")

    sentences_images = []

    for i in sentences:
        print(sentences)

        image = typer.prompt("What image takes this prompt?")




if __name__ == "__main__":
    typer.run(main)
