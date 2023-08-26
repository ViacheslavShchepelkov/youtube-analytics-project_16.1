import os
from googleapiclient.discovery import build


#Создаем глобальную переменную, содержащую ключ от API YouTube
api_key: str = os.getenv('YOU_TUBE_API')


class Video:
    """

    В экземплярах данного класса содержится информация о конкретном видео
    с сайта YouTube
    video_id: индивидуальный id видео
    title: заголовок видео
    link: ссылка на видео
    view_count: количество просмотров
    like_count: количество лайков

    """
    def __init__(self, video_id):
        try:
            self.video_id = video_id
        # Получаем информацию о конкретном видео в виде словаря

            self.response = Video.get_yt_object().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                             id=video_id
                                                             ).execute()
            self.title = self.response['items'][0]['snippet']['title']
            self.link = f'https://www.youtube.com/watch?v={self.video_id}'
            self.view_count: int = self.response['items'][0]['statistics']['viewCount']
            self.like_count: int = self.response['items'][0]['statistics']['likeCount']
        except IndexError:
            self.video_id = video_id
            self.title = None
            self.link = None
            self.view_count = None
            self.like_count = None



    def __repr__(self):
        return f"{self.__class__.__name__}({self.video_id}, {self.title}, {self.link}, {self.view_count},{self.like_count})"

    def __str__(self):
        return f"{self.title}"

    @classmethod
    def get_yt_object(cls):
        """ Создает специальный объект для работы с YouTube API"""
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube


class PLVideo(Video):
    """
    Класс наследует поведение от класса Video.
    При инициализации экзмепляра на вход принимается один доп. параметр
    play_list_id: id плейлиста

    """
    def __init__(self, video_id, play_list_id):
        super().__init__(video_id)
        self.play_list_id = play_list_id


broken_video = Video('broken_video_id')
