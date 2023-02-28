import constants
import csv
import json
import os
from settings import Settings, Language
from gtts import gTTS
from pydub import AudioSegment


def merge_sounds(result: AudioSegment, sound1: AudioSegment, sound2: AudioSegment, silence: AudioSegment):
    return result + sound1 + silence + sound2 + silence


def cleanup():
    if os.path.exists(constants.FIRST_TEMP_FILE):
        os.remove(constants.FIRST_TEMP_FILE)

    if os.path.exists(constants.SECOND_TEMP_FILE):
        os.remove(constants.SECOND_TEMP_FILE)


try:
    with open("settings.json", "r") as f:
        settings_json = json.load(f)

    settings = Settings(Language(settings_json['firstLanguage']['code'], settings_json['firstLanguage']['name'],
                                 settings_json['firstLanguage']['columnIndex']),
                        Language(settings_json['secondLanguage']['code'], settings_json['secondLanguage']['name'],
                                 settings_json['secondLanguage']['columnIndex']),
                        settings_json['silenceInterval'], settings_json['csvSeparator'])

    print("Please specify the input file name:")
    file_name = input()

    # Load CSV file
    csv_file = open(os.path.join("data", file_name), 'r')

    # Specify a number of phrases per file
    print("Please specify a number of phrases per file:")
    phrases_count = input()

    # Generate a segment of silence
    silence_segment = AudioSegment.silent(duration=settings.silence_interval)
    silence_segment.export(constants.RESULT_FILE_NAME + '0' + constants.RESULT_FILE_EXTENSION, format="mp3")

    i = 0
    # Iterate through rows (phrases)
    for row in csv.reader(csv_file, delimiter=settings.csv_separator):
        try:
            # Convert the text to speech using gTTS (Google Text-to-Speech)
            first_item = gTTS(text=row[settings.first_language.column_index], lang=settings.first_language.code,
                              slow=False)
            second_item = gTTS(text=row[settings.second_language.column_index], lang=settings.second_language.code,
                               slow=False)

            # Save as MP3
            with open(constants.FIRST_TEMP_FILE + constants.RESULT_FILE_EXTENSION, "wb") as f:
                first_item.write_to_fp(f)

            with open(constants.SECOND_TEMP_FILE + constants.RESULT_FILE_EXTENSION, "wb") as s:
                second_item.write_to_fp(s)

            part_number = str(i // int(phrases_count))
            result_file_path = constants.RESULT_FILE_NAME + part_number + constants.RESULT_FILE_EXTENSION

            # Load from MP3. This step is because of merging sounds. We have to have the same data type
            if not (os.path.exists(result_file_path)):
                silence_segment.export(result_file_path, format="mp3")

            result = AudioSegment.from_mp3(result_file_path)
            sound1 = AudioSegment.from_mp3(constants.FIRST_TEMP_FILE + constants.RESULT_FILE_EXTENSION)
            sound2 = AudioSegment.from_mp3(constants.SECOND_TEMP_FILE + constants.RESULT_FILE_EXTENSION)

            # Save the result
            to_save = merge_sounds(result, sound1, sound2, silence_segment)
            to_save.export(result_file_path, format="mp3")

            print(f"Finished row: {str(i)}.")
        except Exception as err:
            print(f"Error in row: {str(i)}. {row[0]} ", err)
        finally:
            i = i + 1
except Exception as err:
    print("Error: ", err)
finally:
    cleanup()
    print("Program finished!")
