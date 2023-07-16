import googleapiclient.discovery
import googleapiclient.errors
from youtube_transcript_api import YouTubeTranscriptApi
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file('youtube-to-bigquery-493401d956f9.json')

api_service_name = "youtube"
api_version = "v3"
youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

def get_latest_video_id(channel_id: str):
    search_response = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=1,
        order="date",
        type="video"
    ).execute()

    if "items" in search_response:
        latest_video = search_response["items"][0]["id"]["videoId"] # bruh
        return latest_video
    else:
        return None

def get_video_details(video_id: str):
    try:
        response = youtube.videos().list(
            part="snippet",
            id=video_id
        ).execute()

        if response['items']:
            video = response['items'][0]
            video_title = video['snippet']['title']
            channel_name = video['snippet']['channelTitle']
            return video_title, channel_name
        else:
            return None, None

    except googleapiclient.errors.HttpError as e:
        print(f"An error occurred: {e}")
        return None, None
    
def get_transcript(transcript: str) -> str:
    text_content = [caption['text'] for caption in transcript]
    clean_transcript = ' '.join(text_content)

    if transcript != '':
        return clean_transcript
    else:
        return 'Error, no transcript found.'
    
def get(channel_id='UCBa659QWEk1AI4Tg--mrJ2A') -> dict: # tutaj kanał Toma Scotta
    video_id = get_latest_video_id(channel_id)  
    video_title, channel_name = get_video_details(video_id)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    transcript = get_transcript(transcript)

    output = {
        "id" : video_id,
        "title" : video_title,
        "channel_name" : channel_name,
        "transcript" : transcript
    }

    return output

print(get())
