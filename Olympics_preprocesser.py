import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

athlets = pd.read_csv(r"X:\Data Science\Pro_Projects\Data store\athlete_events.csv")
region = pd.read_csv(r"X:\Data Science\Pro_Projects\Data store\noc_regions.csv")

def preprocess(athlets,region):
    # filtering for summer olympics
    df = athlets[athlets['Season'] == 'Summer']
    # merge with region_df
    df = df.merge(region, on='NOC', how='left')
    # dropping duplicates
    df.drop_duplicates(inplace=True)
    # one hot encoding medals
    df = pd.concat([df, pd.get_dummies(df['Medal']).astype(int)], axis=1)
    return df
