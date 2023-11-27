import re
from datetime import datetime



def main():
    parser = SubtitleFileParser('subtitles.srt')
    parsed_subs = parser.parse()
    
    for sub in parsed_subs[:5]:
        print(sub.str_full())

    
class SubtitleFileReader:
    DEFAULT_FILE_PATH = 'subtitles.srt'

    def read_file(self, file_path=None):
        if not file_path:
            file_path = self.DEFAULT_FILE_PATH

        try:
            with open(file_path, 'r') as file:
                return file.read()
        except Exception:
            return None

# TODO: passing sub time format
class SubtitleFileParser:
    SUBTITLE_TIME_FORMAT = '%H:%M:%S,%f'
    file_content = None

    def __init__(self, file=None) -> None:
        self.read_file(file)

    def read_file(self, file=None):
        self.file_content = SubtitleFileReader().read_file(file)

    def parse(self):
        if not self.file_content:
            raise ValueError('Cannot parse an empty file.')
            
        if type(self.file_content) != str:
            raise TypeError('Incorrect parser argument type. Str expected.')

        pattern = r'(\d+)\n(\d\d.*\d\d\d) --> (\d\d.*\d\d\d)\n(?:(?:\n\n)|((?:.+\n)+))'
        matches = re.findall(
            pattern,
            self.file_content
        )
        
        subtitle_blocks = []

        for match in matches:
            try:
                subtitle_blocks.append(
                    SubtitleBlock(
                        order=int(match[0]),
                        start_time=datetime.strptime(match[1], self.SUBTITLE_TIME_FORMAT),
                        end_time=datetime.strptime(match[2], self.SUBTITLE_TIME_FORMAT),
                        text=match[3]
                    )
                )
            except ValueError as ve:
                print('Error in block: ' + str(match))
                print(ve)
                continue
            except Exception as exc:
                print('Error in block: ' + str(match))
                print(exc)
                continue

        return subtitle_blocks

# TODO: passing sub title format
class SubtitleBlock:
    SUBTITLE_TIME_FORMAT = '%H:%M:%S,%f'
    def __init__(self, order, start_time, end_time, text) -> None:
        self.order = order
        self.start_time = start_time
        self.end_time = end_time
        self.text = text
    
    def str_full(self):
        start = self.start_time.strftime(self.SUBTITLE_TIME_FORMAT)[:-3]
        end = self.end_time.strftime(self.SUBTITLE_TIME_FORMAT)[:-3]
        return f'{self.order}\n{start} --> {end}\n{self.text}'

    def __str__(self) -> str:
        return f'{self.order}: {self.text if self.text else "<empty_text>"}'


if __name__ == "__main__":
    main()