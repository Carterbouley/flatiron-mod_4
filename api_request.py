import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests 
import json
import isodate
from apiclient.discovery import build
class CreateYoutubeRequest():
    def __init__(self):
        self.key = json.load(open(".secret/api_key.json"))['api_key']
        self.youtube = build("youtube", "v3", developerKey=self.key)
        
        
    
    def top_n_channels(self, topic_id, n):
        req = self.youtube.search().list(topicId = topic_id, part = 'snippet', type = 'channel',
                                    order = 'viewCount', maxResults = n).execute()
        channel_ids = [channel['id']['channelId'] for channel in req['items']]
        req = self.youtube.channels().list(part = "snippet,statistics", id = ', '.join(channel_ids)).execute()
        channels = []
        for channel in req['items']:
            channels.append({'channel_name': channel['snippet']['title'], 
                             'channel_id': channel['id'],
                             'video_count': int(channel['statistics']['videoCount']),
                             'subscriber_count': int(channel['statistics']['subscriberCount'])})
        channels_df = pd.DataFrame.from_dict(channels)
        return channels_df.sort_values(by = 'subscriber_count', ascending=False)

    def get_channel_videos(self, channel_id):
        res = self.youtube.channels().list(id = channel_id, part = 'contentDetails').execute()
        playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        next_page_token = None
        videos = []
        while True:
            res = self.youtube.playlistItems().list(playlistId = playlist_id, 
                                               part = 'snippet', 
                                               maxResults = 50,
                                               pageToken = next_page_token).execute()
            video_ids = [x['snippet']['resourceId']['videoId'] for x in res['items']]
            next_page_token = res.get('nextPageToken')
            res = self.youtube.videos().list(id = ', '.join(video_ids), 
                                        part = 'snippet,contentDetails,statistics').execute()
            videos += res['items']
            if next_page_token is None:
                break
        return videos
    
    def get_video_attributes(self, videos):
        video_list = []
        for video in videos:
            video_list.append({'title': video['snippet']['title'],
                               'description': video.get('snippet', {}).get('description'), 
                               'publish_time': video.get('snippet', {}).get('publishedAt'),
                               'tags': video.get('snippet', {}).get('tags'),
                               'duration': video.get('contentDetails', {}).get('duration'),
                               'like_count': video.get('statistics', {}).get('likeCount'),
                               'dislike_count': video.get('statistics', {}).get('dislikeCount'),
                               'comment_count': video.get('statistics', {}).get('commentCount'),
                               'live': video.get('snippet', {}).get('liveBroadcastContent'),
                               'view_count': video.get('statistics', {}).get('viewCount')})
        return pd.DataFrame.from_dict(video_list)
    
    def transform_video_attributes(self, df):
        df.dropna(inplace=True)
        df['duration'] = pd.to_datetime(df['duration'].map(lambda x: isodate.parse_duration(x))).map(lambda x: x.minute).astype('int')
        df['publish_time'] = pd.to_datetime(df['publish_time'])
        time_split = pd.DataFrame(df['publish_time'].map(lambda x: [x.hour, x.weekday(), x.month, x.date()]).to_list(), 
                                  columns = ['publish_hour', 'publish_day', 'publish_month', 'publish_date'])
        df = pd.concat([df, time_split], axis = 1)
        df.dropna(inplace=True)
        df['publish_date'] = pd.to_datetime(df['publish_date'])
        df.sort_values(by = 'publish_date', inplace = True)
        df['days_after_last_video'] = df['publish_date'].diff(periods = 1)
        df.dropna(inplace=True)
        df['days_after_last_video'] = df['days_after_last_video'].map(lambda x: x.days).astype('int')
        for col in ['duration', 'publish_hour', 'publish_day', 'publish_month', 'comment_count', 'like_count', 'dislike_count', 'view_count']:
            df[col] = df[col].astype('int')
        df[['title_length', 'description_length', 'tag_count']] = df[['title', 'description', 'tags']].applymap(len)
        df['live'] = df['live'].map(lambda x: 0 if 'none' else 1) 
        df.drop(columns = ['description', 'publish_time'], inplace = True)
        return df

    def create_channel_df(self, channel_id):
        videos = self.get_channel_videos(channel_id)
        df = self.get_video_attributes(videos)
        transformed_df = self.transform_video_attributes(df)
        return transformed_df  
