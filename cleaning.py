import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests 
import json
import isodate
from apiclient.discovery import build
class CleanYoutubeCSV():
    
    
    def __init__(self):
        pass

        
    def add_dummies(self, df):
        
#         Drop Outliers
        top_5_index = df.view_count.sort_values(ascending = False).head().index
        df.drop(labels = top_5_index, inplace = True)
        

#         Add numerical variables in buckets for season, time of day, and if its a weekend

        df['season'] = df['publish_month'].map(lambda x: 
                               'winter' if (x == 12) |( x < 3) else 
                               ('spring' if (3 <= x < 6) else
                               ('summer' if (6 <= x < 9) else 
                               'fall')))
        df['day_part'] = df['publish_hour'].map(lambda x: 
                               'morning' if (6 <= x <12) else 
                               ('afternoon' if (12 <= x < 18) else
                               ('evening' if (18 <= x < 24) else 
                               'overnight')))
        df['weekend'] = df['publish_day'].map(lambda x: 1 if x >= 5 else 0)
        
#         Catagorize Variables
                               
        df.season = df.season.astype('category').cat.codes    
        df.day_part = df.day_part.astype('category').cat.codes
        
        season_dummies = pd.get_dummies(df.season, prefix ='season')
        season_dummies.drop(columns = 'season_2', inplace = True)

        day_part_dummies = pd.get_dummies(df.day_part, prefix = 'day_part')
        day_part_dummies.drop(columns = 'day_part_2', inplace = True)

#         Join databases

        df = pd.concat([df, season_dummies, day_part_dummies], axis = 1)
        df.drop(columns = ['season', 'day_part'], inplace = True)
        
#         Add dummy varibales for keywords used in video titles
        
        df['review'] = df.title.map(lambda x: 1 if ('Review' in x.split(' ')) | 
                            ('Review!' in x.split(' ')) | 
                            ('Review:' in x.split(' ')) |
                            ('Impressions' in x.split(' ')) | 
                            ('Impressions:' in x.split(' ')) |
                            ('Impressions!' in x.split(' ')) | 
                            ('Unboxing' in x.split(' ')) | 
                            ('Unboxing:' in x.split(' ')) |
                            ('Unboxing!' in x.split(' ')) 
                            else 0)
        
        df['apple'] = df.title.map(lambda x: 1 if ('Apple' in x.split(' ')) | 
                            ('Apple!' in x.split(' ')) | 
                            ('iPhone' in x.split(' ')) |
                            ('iPhone!' in x.split(' ')) | 
                            ('iPad!:' in x.split(' ')) |
                            ('iPad' in x.split(' ')) | 
                            ('iMac' in x.split(' ')) | 
                            ('Mac' in x.split(' ')) |
                            ('Macbook' in x.split(' ')) |
                            ('Macbook:' in x.split(' ')) |
                            ('AirPods' in x.split(' ')) |
                            ('Airpods!' in x.split(' ')) 
                            else 0)
        
        df['google'] = df.title.map(lambda x: 1 if ('Google' in x.split(' ')) else 0)
        
        df['samsung'] = df.title.map(lambda x: 1 if ('Samsung' in x.split(' ')) | 
                            ('Samsung!' in x.split(' ')) | 
                            ('Galaxy' in x.split(' ')) |
                            ('Note' in x.split(' '))  
                            else 0)
        
        df['tesla'] = df.title.map(lambda x: 1 if ('Tesla' in x.split(' ')) else 0)
        
#         Drop columns which we have previously catagorized or dummied
        
        df.drop(columns = ['publish_date', 'title', 'publish_day', 'publish_hour', 'publish_month', 'live'], inplace = True)
        
        return df
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
