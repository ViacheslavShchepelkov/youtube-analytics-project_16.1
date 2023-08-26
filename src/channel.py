import os
import json
from googleapiclient.discovery import build


class Channel:
    """
    Класс создает экземпляры, содержащие данные о конкретном YouTube канале
    __channel_id: индивидуальный id канала
    title: заголовок канала
    description: описание канала
    url: ссылка на канал
    num_subscribers: количество подписчиков канала
    video_count: количество видео на канале
    total_views: общее количество просмотров на канале

        """
    def __init__(self, channel_id='') -> None:
        self.__channel_id = channel_id
        channel = Channel.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.url = channel['items'][0]['snippet']['customUrl']
        self.num_subscribers = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.total_views = channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f"{self.title} - {self.url}"

    def __add__(self, other):
        return int(self.num_subscribers) + int(other.num_subscribers)

    def __sub__(self, other):
        return int(self.num_subscribers) - int(other.num_subscribers)

    def __lt__(self, other):
        return int(self.num_subscribers) < int(other.num_subscribers)

    def __le__(self, other):
        return int(self.num_subscribers) <= int(other.num_subscribers)

    def __gt__(self, other):
        return int(self.num_subscribers) > int(other.num_subscribers)

    def __ge__(self, other):
        return int(self.num_subscribers) >= int(other.num_subscribers)

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @staticmethod
    def print_json(dict_to_print: dict) -> str:
        """Выводит словарь в json-подобном удобном формате с отступами"""

        return json.dumps(dict_to_print, indent=2, ensure_ascii=False)

    @classmethod
    def get_service(cls):
        """Класс-метод, возвращающий объект для работы YouTube API"""
        return build('youtube', 'v3', developerKey=os.getenv("YOU_TUBE_API"))

    def to_json(self, name_file):
        """
        Метод, который сохраняет словарь со значением атрибутов экземпляра Channel
        """
        with open(str(name_file), 'w+') as file:
            info_about_channel = self.print_json(self.__dict__)
            file.write(info_about_channel)


moscowpython = Channel('UC-OVMPlMA3-YCIeg4z5z23A')

print(moscowpython.__dict__)
