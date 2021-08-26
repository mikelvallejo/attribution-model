import pandas as pd
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns

def read_and_sort_data():
    '''reads the data from the csv file and sorts it by the date. 
    It also creates a visit_order column for event hierarchy'''
    df = pd.read_csv('attribution data.csv')
    df = df.sort_values(['cookie', 'time'],
                        ascending=[False, True])
    df['visit_order'] = df.groupby('cookie').cumcount() + 1

    return df

def create_paths():
    '''assigns each path to the cookie and adds conversion if it is true'''
    #Group by cookie and aggregate channels
    df_paths = df.groupby('cookie')['channel'].aggregate(
    lambda x: x.unique().tolist()).reset_index()
    #Drop duplicates
    df_last_interaction = df.drop_duplicates('cookie', keep='last')[['cookie', 'conversion']]
    #Merge the two dataframes
    df_paths = pd.merge(df_paths, df_last_interaction, how='left', on='cookie')
    #Add start to the beggining and Null/Conversion at the end of the path
    df_paths['path'] = np.where( df_paths['conversion'] == 0,
    ['Start, '] + df_paths['channel'].apply(', '.join) + [', Null'],
    ['Start, '] + df_paths['channel'].apply(', '.join) + [', Conversion'])
    df_paths['path'] = df_paths['path'].str.split(', ')
    #Final version of the Dataframe
    df_paths = df_paths[['cookie', 'path', 'conversion']]

    return df_paths

def get_common_paths():
    '''creates a dictionary with the paths and the number of times they appear'''
    #Create a new column with the path as string to fetch distinct paths
    df_paths['string'] = df_paths['path'].apply(lambda x: ' -> '.join(x))
    #Group by path and count the occurrences
    return df_paths.groupby('string')['conversion'].count().sort_values(ascending=False).head(10)

def get_common_conversion_paths():
    '''creates a dictionary with the paths with more conversions and the number of times they appear'''
    #Create a new column with the path as string to fetch distinct paths
    df_paths['string'] = df_paths['path'].apply(lambda x: ' -> '.join(x))
    #Group by path and count the occurrences, only conversion events
    df_paths[df_paths.conversion == 1].groupby('string')['conversion'].count().sort_values(ascending=False).head(10)