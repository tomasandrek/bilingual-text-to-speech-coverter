import csv
import json
from settings import Settings, Language
from gtts import gTTS
from pydub import AudioSegment


with open("settings.json", "r") as f:
    settings_json = json.load(f)

settings = Settings(Language(settings_json['firstLanguage']['code'], settings_json['firstLanguage']['name'], settings_json['firstLanguage']['columnIndex']),
                Language(settings_json['secondLanguage']['code'], settings_json['secondLanguage']['name'], settings_json['secondLanguage']['columnIndex']),
                settings_json['silenceInterval'])

print(settings.first_language.name)


csv_file = open('DailyWordsAllTogether.csv','r')

silence_segment = AudioSegment.silent(duration=5000)
silence_segment.export('result.mp3', format="mp3")

i = 0

for row in csv.reader(csv_file, delimiter=';'):
    first_item = gTTS(text=row[0], lang="sk", slow=False)
    second_item = gTTS(text=row[1], lang="en", slow=False)
    with open("first_item_temp.mp3", "wb") as f:
        first_item.write_to_fp(f)

    with open("second_item_temp.mp3", "wb") as s:
        second_item.write_to_fp(s)

    result = AudioSegment.from_mp3("result.mp3")
    sound1 = AudioSegment.from_mp3("first_item_temp.mp3")
    sound2 = AudioSegment.from_mp3("second_item_temp.mp3")

    to_save = result + sound1 + silence_segment + sound2 + silence_segment

    to_save.export("result.mp3", format="mp3")

    print("Finished row: " + str(i))
    i = i + 1

print("Program finished!")