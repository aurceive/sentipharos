from googleapiclient.discovery import build

# Замените 'YOUR_API_KEY' на свой ключ API YouTube Data API
api_key = 'AIzaSyDmeT8Isv-2I-jkqr5K5o8bEhXg66JfTEQ'
video_id = 'fPr3vbxnNew'  # Замените на ID видео, откуда нужно получить комментарии

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
