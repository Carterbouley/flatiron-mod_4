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
        
        df2 = pd.concat([df, season_dummies], axis = 1)
        
        day_part_dummies = pd.get_dummies(df.day_part, prefix = 'day_part')
        day_part_dummies.drop(columns = 'day_part_morning', inplace = True)
        
        df3 = pd.concat([df2, day_part_dummies], axis = 1)
        
        return df3