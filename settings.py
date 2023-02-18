class Language:
    code: str
    name: str
    column_index: int

    def __init__(self, code: str, name: str, column_index: int) -> None:
        self.code = code
        self.name = name
        self.column_index = column_index


class Settings:
    first_language: Language
    second_language: Language
    silence_interval: int
    csv_separator: str

    def __init__(self, first_language: Language, second_language: Language, silence_interval: int, csv_separator: str) -> None:
        self.first_language = first_language
        self.second_language = second_language
        self.silence_interval = silence_interval
        self.csv_separator = csv_separator
