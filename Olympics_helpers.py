import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st




def add_bg_from_url():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("https://www.wallpaperflare.com/static/954/381/189/olympic-bright-colourfull-circle-wallpaper.jpg");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )



def medal_tally(athlets):
  athlets = athlets.drop_duplicates(subset=['Team','region','Games','Year','Sport','Event', 'Medal'])
  medals_tally =athlets.groupby('NOC').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()
  medals_tally['toatal'] = medals_tally['Gold']+medals_tally['Silver']+medals_tally['Bronze']
  medals_tally.index = medals_tally.index+1
  return medals_tally

def athlets_country(athlets, selected_country, selected_year):
    # Filter by country, year, and non-zero medal counts
    country_athletes = athlets[
        (athlets['region'] == selected_country) &
        (athlets['Year'] == selected_year) &
        ((athlets['Gold'] > 0) | (athlets['Silver'] > 0) | (athlets['Bronze'] > 0))
    ][['Name', 'Age', 'Event', 'Gold', 'Silver', 'Bronze']]

    # Sort by Gold medals and select top 10
    country_athletes = country_athletes.sort_values('Gold', ascending=False).head(10)
    country_athletes= country_athletes.reset_index(drop=True)
    country_athletes.index = country_athletes.index+1

    return country_athletes



def country_year_list(athlets):
    # Get unique country/region values
    country = athlets['region'].dropna().unique().tolist()
    country.sort()
    country.insert(0, 'Overall')  # Insert 'Overall' at the beginning

    # Get unique years
    year = athlets['Year'].dropna().unique().tolist()
    year.sort()
    year.insert(0, 'Overall')  # Insert 'Overall' at the beginning

    return country, year
def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x



def Participating_nations_over(athlets, col):

  Nations_over_time =athlets.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('Year')
  Nations_over_time.rename(columns={'Year':'Year','count':col},inplace=True)
  return Nations_over_time


def Most_successful(athlets, sports):
    # Drop rows without medals
    b = athlets.dropna(subset=['Medal'])

    if sports == 'overall':
        b = athlets.dropna(subset=['Medal'])
    # Filter by sport if not 'overall'
    if sports != 'overall':
        b = b[b['Sport'] == sports]

    # Count medals per athlete
    medal_counts = b['Name'].value_counts().reset_index()
    medal_counts.columns = ['Name', 'Medals']

    # Merge with original data to get additional info
    result = medal_counts.merge(athlets[['Name', 'Sport', 'region']], on='Name', how='left').drop_duplicates('Name')

    # Select the top 15 athletes
    result = result.head(15)
    result = result.reset_index(drop = True)
    result.index = result.index +1
    result.index.name = 'Rank'


    return result



def country_wise_analysis(athlets,coutry):
  df = athlets.dropna(subset=['Medal'])
  df.drop_duplicates(subset = ['Team', 'NOC', 'Games', 'Year', 'City','Sport', 'Event', 'Medal'], inplace = True)
  new =df[df["region"] == coutry]
  new = new.groupby('Year').count()['Medal'].reset_index()
  return new





def country_event_Heatmap(athlets, selected_country):
    # Example of generating a pivot table (replace this with your actual logic)
    pt = athlets[athlets['region'] == selected_country].pivot_table(
        index='Sport',
        columns='Event',
        values='Medal',
        aggfunc='count'  # Example aggregation
    )
    return pt

def Country_wise_Most_successful(athlets, country):
    # Drop rows without medals
    b = athlets.dropna(subset=['Medal'])
    b = b[b['region'] == country]

    # Count medals per athlete
    medal_counts = b['Name'].value_counts().reset_index()
    medal_counts.columns = ['Name', 'Medals']

    # Merge with original data to get additional info
    result = medal_counts.merge(athlets[['Name', 'Sport']], on='Name', how='left').drop_duplicates('Name')

    # Select the top 15 athletes
    result = result.head(10)
    result = result.reset_index(drop = True)
    result.index = result.index+1
    return result

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df


def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final