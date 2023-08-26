import os
import re
import datetime
from googleapiclient.discovery import build

api_key: str = os.getenv("YOU_TUBE_API")


class PlayList:
    """
    Класс создает экземпляры, содержащие данные о конкретном плейлисте.
    playlist_id: id плейлиста
    response: содержит информацию об роликах в плейлисте.
    title: название плейлиста
    url: ссылка на плейлист
    """

    def __init__(self, playlist_id):
        self.__playlist_id = playlist_id
        request = self.get_api_object().playlistItems().list(
            part="snippet,contentDetails",
            maxResults=25,
            playlistId=self.__playlist_id
        )
        self.__response = request.execute()
        title_playlist = self.__response["items"][0]["snippet"]["title"]
        self.title = title_playlist.split('.')[0]
        self.url = f"https://www.youtube.com/playlist?list={self.__playlist_id}"

    @classmethod
    def get_api_object(cls):
        """Возвращает объект для работы с API YouTube"""
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    @property
    def response(self):
        return self.__response

    @property
    def playlist_id(self):
        return self.__playlist_id

    @property
    def total_duration(self):
        """
        Метод возвращает объект класса datetime.timedelta, который содержит суммарную продолжительность всех видео в
        плейлисте.
        return: Возвращает экземпляр класса timedelta
        """
        # Инициализируем список с id каждого видео
        list_ids = self.video_ids()
        # Переменные для хранения соответствующих величин продолжительности видеоролика.
        hours, minutes, seconds = int(), int(), int()
        # В цикле вызываем словарь данных по каждому видео из списка
        for video in list_ids:
            # Получаем данные о видео
            video_response = self.get_api_object().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                                 id=video).execute()
            # Получаем данные о продолжительности
            text = video_response['items'][0]['contentDetails']['duration']
            # С помощью библиотеки re и регулярных выражений ищем значение каждой единицы времени,
            # обозначающей продолжительность видео
            if "H" in text:
                result_search_hours = re.findall(r"(\d\d?)H", text)
                hours += int(result_search_hours[0])
            if 'M' in text:
                result_search_minutes = re.findall(r"(\d\d?)M", text)
                minutes += int(result_search_minutes[0])
            if "S" in text:
                result_search_seconds = re.findall(r"(\d\d?)S", text)
                seconds += int(result_search_seconds[0])
        # Сокращаем полученные значения до возможно минимальных величин
        minutes = minutes + (seconds // 60)
        seconds = round(seconds % 60, 2)
        hours = hours + (minutes // 60)
        minutes = round(minutes % 60, 2)
        # Создаем экземпляр класса timedelta
        playlist_duration = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
        return playlist_duration

    def show_best_video(self):
        """
        Функция возвращает ссылку на самое популярное видео по количеству лайков
        """
        # Переменная для хранения id видеоролика
        best_video_url = str()
        # Переменная для числа, обозначающего максимальное количество лайков
        like_count = int()
        # Инициализируем список с id каждого видеоролика
        list_ids = self.video_ids()
        # В цикле пробегаем по каждому видео и получаем количество лайков и id
        for video in list_ids:
            video_response = self.get_api_object().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                                 id=video).execute()
            count = int(video_response['items'][0]['statistics']['likeCount'])
            # Сравниваем количество лайков
            if count > like_count:
                like_count = count
                best_video_url = video_response['items'][0]['id']
        return f"https://youtu.be/{best_video_url}"

    def video_ids(self):
        """
        Функция возвращает список id всех видеороликов, содержащихся в плейлисте
        """
        list_ids = []
        for video in self.__response["items"]:
            list_ids.append(video["contentDetails"]['videoId'])
        return list_ids
