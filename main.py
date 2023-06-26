import json
from pathlib import Path
import random
import shutil

import typer
from gtts import gTTS
from moviepy.editor import ImageClip, CompositeVideoClip, AudioFileClip
from rich import print

import utils.file_management
import utils.chat
import utils.image
import utils.video


def main(number_words: int,
         language: str,
         max_tokens: int,
         model: str,
         width: int,
         height: int,
         fps: int,
         stop_create_files: bool = True,
         delete_files: bool = True,
         warning_sources: bool = True,
         write_empty: bool = True):

    ACTUAL_FOLDER = Path(__file__).parents[0]

    image_folder = Path("temp") / "images"
    audio_folder = Path("temp") / "audio"
    output_folder = Path("output")

    created_elements = utils.file_management.create_files(files=["sources.json", "settings.json"],
                                                          folders=[str(image_folder),
                                                                   str(audio_folder),
                                                                   str(output_folder)],
                                                          main_path=ACTUAL_FOLDER)

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
                          r"Do it in {language}. Don't place words like 'script' or 'introduction' at the beginning :"
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
        sentences = [str(i.lower().replace("\n", "")) for i in utils.chat.split(r"!\.\?", utils.chat.ask(prompt, max_tokens, model))
                     if i]

        print(sentences)

        verification = typer.confirm("Is that a good prompt for you?")

    clips = []

    for count, sentence in enumerate(sentences):
        print(sentence)

        url = typer.prompt("What image takes this prompt?")

        image_path = ACTUAL_FOLDER / image_folder / f"{count}.jpg"
        audio_path = ACTUAL_FOLDER / audio_folder / f"{count}.mp3"

        image = utils.image.get_image_online(url)
        image.save(str(image_path))

        tts = gTTS(sentence, lang=language, slow=False)
        tts.save(str(audio_path))

        audio = AudioFileClip(str(audio_path))

        clip = ImageClip(str(image_path)).set_duration(audio.duration)

        clip = clip.resize(width=width)
        clip = utils.video.zoom_in_effect(clip)

        clip = clip.set_audio(audio)
        clip = clip.set_position("center")

        while clip.h < height:
            clip = clip.resize(height=round(clip.h * 1.1))

        if count > 0:
            clip = clip.set_start(clips[count - 1].end)

        clips.append(clip)

    name = f"video-{random.randint(1000000, 9999999)}.mp4"

    assemblate_clip = CompositeVideoClip(clips, size=(width, height))
    assemblate_clip.write_videofile(
        str(ACTUAL_FOLDER / output_folder / name),
        fps=fps,
        codec='libx264',
        audio_codec='aac',
        temp_audiofile='temp-audio.m4a',
        remove_temp=True
    )

    shutil.rmtree(str(ACTUAL_FOLDER / "temp"))


if __name__ == "__main__":
    typer.run(main)
