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
        df = df.drop(columns = 'Unnamed: 0')
        
        df['season'] = df['publish_month'].map(lambda x: 
                                       'winter' if (x > 12) |( x < 3) else 
                                       ('spring' if (3<x<6) else
                                       ('summer' if (5<x<9) else 
                                       'fall')))
        df.season.astype('category').cat.codes
        
        df['day_part'] = df['publish_hour'].map(lambda x: 
                                       'morning' if (6<=x<12) else 
                                       ('afternoon' if (12<=x<18) else
                                       ('evening' if (18<=x<=23) else 
                                       'overnight')))
        df.day_part.astype('category').cat.codes
        
        season_dummies = pd.get_dummies(df.season, prefix ='season')
        season_dummies.drop(columns = 'season_spring', inplace = True)
        
        df = pd.concat([df, season_dummies], axis = 1)
        
        day_part_dummies = pd.get_dummies(df.day_part, prefix = 'day_part')
        day_part_dummies.drop(columns = 'day_part_morning', inplace = True)
        
        df = pd.concat([df, day_part_dummies], axis = 1)
        
        indices = []
        for item in list(enumerate(df.title.str.contains('Unboxing'))):
            if item[1] == True:
                indices.append(item[0])
        for item in list(enumerate(df.title.str.contains('Review'))):
            if item[1] == True:
                indices.append(item[0])
        for item in list(enumerate(df.title.str.contains('Impressions'))):
            if item[1] == True:
                indices.append(item[0])
        indices = list(np.unique(indices))
        for index in indices:
            df.loc[index, 'review'] = 1
        df.review.fillna(0, inplace = True)
        df.review = df.review.astype('int')
        
        for item in list(enumerate(df.title.str.contains('Apple'))):
            if item[1] == True:
                indices.append(item[0])
        indices = list(np.unique(indices))
        for index in indices:
            df.loc[index, 'apple'] = 1
        df.apple.fillna(0, inplace = True)
        df.apple = df.review.astype('int')
        
        for item in list(enumerate(df.title.str.contains('Google'))):
            if item[1] == True:
                indices.append(item[0])
        indices = list(np.unique(indices))
        for index in indices:
            df.loc[index, 'google'] = 1
        df.google.fillna(0, inplace = True)
        df.google = df.review.astype('int')
        
        for item in list(enumerate(df.title.str.contains('Samsung'))):
            if item[1] == True:
                indices.append(item[0])
        indices = list(np.unique(indices))
        for index in indices:
            df.loc[index, 'samsung'] = 1
        df.samsung.fillna(0, inplace = True)
        df.samsung = df.review.astype('int')
        
        return df
    
    
    