from googleapiclient.discovery import build
from server.common import YOUTUBE_API_KEY

api_key = YOUTUBE_API_KEY
video_id = 'fPr3vbxnNew' # ID видео

# Создаем объект API клиента
youtube = build('youtube', 'v3', developerKey=api_key)

# Запрашиваем комментарии к видео
def get_comments(youtube, video_id):
    comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100  # Максимальное количество комментариев в одном запросе
    )
    response = request.execute()

    # Парсим комментарии из ответа API
    for item in response['items']:
        # comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comment = item
        comments.append(comment)

    return comments

# Получаем комментарии
comments = get_comments(youtube, video_id)

# # Выводим комментарии
# for i, comment in enumerate(comments, start=1):
#     print(f"{i}. {comment}")
