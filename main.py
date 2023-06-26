import json
from pathlib import Path

import typer
from rich import print

import utils.file_management
import utils.chat


def main(number_words: int,
         language: str,
         max_tokens: int,
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
        print("Nothing is in the settings.json file.")

        if write_empty:
            with open(settings, "w") as f:
                dictionary = {
                    "prompt": r"Generate me a script for a video the sources I give to you. The video "
                              r"needs to be 150 words. You have to be a top writer in videos. You need "
                              r"to be very emotional and fun, so the people can be interested in a short "
                              r"amount of time. Your vocabulary needs to be in the political correct, you can't insult"
                              r" anyone or give what you're thinking. The introduction needs to show the subject in a "
                              r"short amount of time and needs to be shocking and not boring. It has to be in {language} :"
                }
                json.dump(dictionary, f, indent=4)

        raise typer.Exit()

    if warning_sources:
        delete = typer.confirm("Did you format correctly sources in a json list?")

        if not delete:
            print("Format correctly it.")
            raise typer.Exit()

    with open(settings, "r") as settings_f:
        with open(sources, "r") as sources_f:
            prompt = json.load(settings_f)["prompt"].replace("{words}", str(number_words)).replace("{language}", str(language))
            prompt += "First article - " + "\nNew article - ".join(json.load(sources_f))

    print(utils.chat.ask(prompt, max_tokens))


if __name__ == "__main__":
    typer.run(main)
