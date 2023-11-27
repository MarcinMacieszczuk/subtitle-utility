import re
from datetime import datetime

SUBTITLE_TIME_FORMAT = '%H:%M:%S,%f'

def main():
    sub_parser = SubtitleFileParser()
    parsed_subs = sub_parser.parse()
    
    for sub in parsed_subs[:5]:
        print(sub.str_full())
    

class SubtitleFileParser:
    subtitle_file_path = 'subtitles.srt'
    file_content = None

    def __init__(self, file_path) -> None:
        self.subtitle_file_path = file_path

    def read_file(self, to_list=False):
        with open(self.file_path, 'r') as file:
            self.file_content = file.read()
            return self.file_content

    def parse(self, file=None):
        if file:
            self.read_file(file)
        elif type(file) != str:
            raise TypeError('Incorrect argument type. Str expected.')

        pattern = r'(\d+)\n(\d\d.*\d\d\d) --> (\d\d.*\d\d\d)\n(?:(?:\n\n)|((?:.+\n)+))'
        subtitle_blocks = re.findall(
            pattern,
            self.file_content
        )

        subtitle_blocks = []

        for block in subtitle_blocks:
            try:
                subtitle_blocks.append(
                    SubtitleBlock(
                        order=int(block[0]),
                        start_time=datetime.strptime(block[1], SUBTITLE_TIME_FORMAT),
                        end_time=datetime.strptime(block[2], SUBTITLE_TIME_FORMAT),
                        text=block[3]
                    )
                )
            except ValueError as ve:
                print('Error in block: ' + str(block))
                print(ve)
                continue
            except Exception as exc:
                print('Error in block: ' + str(block))
                print(exc)
                continue


class SubtitleBlock:
    def __init__(self):
        pass

    def __init__(self, order, start_time, end_time, text):
        self.order = order
        self.start_time = start_time
        self.end_time = end_time
        self.text = text
    
    def str_full(self):
        start = self.start_time.strftime(SUBTITLE_TIME_FORMAT)[:-3]
        end = self.end_time.strftime(SUBTITLE_TIME_FORMAT)[:-3]
        return f'{self.order}\n{start} --> {end}\n{self.text}'

    def __str__(self) -> str:
        return f'{self.order}: {self.text if self.text else "<empty_text>"}'


if __name__ == "__main__":
    main()