from googleapiclient.discovery import build

api_key = 'AIzaSyDmeT8Isv-2I-jkqr5K5o8bEhXg66JfTEQ'
channel_id = 'UC7Elc-kLydl-NAV4g204pDQ'

youtube = build('youtube', 'v3', developerKey=api_key)

def get_channel_info(youtube, channel_id):
  request = youtube.channels().list(
    part='snippet,statistics',
    id=channel_id
  )
  response = request.execute()
  return response['items'][0]

channel_info = get_channel_info(youtube, channel_id)
print(channel_info)
