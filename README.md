# Flatiron Mod 4 - Predicting YouTube views using linear regression

The files included in this repository include:

     - api_request.py - Create request for Youtube API & exports data to csv
     - cleaning.py - Converts catagorical variables into dummy binary variables & Removes outliers
     - Visualisation.ipynb - EDA plots
     - Regression Analysis.ipynb - Regession Models
     - TimeSeriesAnalysis.ipynb - ARIMA model
     
     
Our client was a tech influencer looking to start a successfull Tech focussed Youtube channel

We used number of views as a proxy variable to represent success of the channel.

We analysed youtube meta-data to look at what objective metrics could be useful to help formate their video production.

The following attributes were included in the first model:
- comment_count            
- dislike_count            
- duration                 
- like_count               
- days_after_last_video    
- title_length             
- description_length       
- tag_count                
- weekend                  
- season_0                 
- season_1                 
- season_3                 
- day_part_0               
- day_part_1               
- day_part_3               
- season_0.1               
- season_1.1               
- season_3.1               
- day_part_0.1             
- day_part_1.1             
- day_part_3.1             
- review                   
- apple                    
- google                   
- samsung                  
- tesla                    

Following using all the parameters, we aimed to improve the model through the following steps:

- removing features which were highly correlated with each other
- scaling numerical predictors
- removing features to avoid overfitting through variance threshold, recursive feature elimination

Our second model resulted in using 11 features
We then checked for interactions between the features using lasso and ridge regularization techniques

Our final regression model contained the following features as predictors for view count: 

 - 'comment_count',
 - 'duration',
 - 'tag_count',
 - 'duration title_length',
 - 'duration review',
 - 'review apple'



Our final r2 results for the training data was:
0.36728210434714337

And fo the test data 
-0.32282276217897343

To conclude we found that it is hard to predict a videos success using meta-data.

As an extension we would use time series analysis to predict views based purely on channal popularity growth, and combine the models using ARIMAX time-seies model