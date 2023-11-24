import re
from datetime import datetime

SUBTITLE_TIME_FORMAT = '%H:%M:%S,%f'

def main():
    file_content = read_file()
    parse_file(file_content)
    
    for sub in Subtitle.subtitles[:5]:
        print(sub.str_full())
    
def read_file(to_list=False):
    with open('subtitles.srt', 'r') as file:
        if to_list:
            return file.readlines()
        else:
            return file.read()

def parse_file(file_content: str):
    if not file_content:
        return
    elif type(file_content) != str:
        raise TypeError('Incorrect argument type. Str expected.')
    
    Subtitle.subtitles.clear()

    pattern = r'(\d+)\n(\d\d.*\d\d\d) --> (\d\d.*\d\d\d)\n(?:(?:\n\n)|((?:.+\n)+))'
    subtitle_blocks = re.findall(
        pattern,
        file_content
    )

    for block in subtitle_blocks:
        try:
            Subtitle.subtitles.append(
                Subtitle(
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


class Subtitle:
    subtitles = []

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