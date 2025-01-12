from googleapiclient.discovery import build
from server.common import YOUTUBE_API_KEY

api_key = YOUTUBE_API_KEY
video_id = 'fPr3vbxnNew'

youtube = build('youtube', 'v3', developerKey=api_key)

def get_video_info(youtube, video_id):
  request = youtube.videos().list(
      part='snippet,statistics',
      id=video_id
  )
  response = request.execute()
  return response['items'][0]

video_info = get_video_info(youtube, video_id)
print(video_info)
