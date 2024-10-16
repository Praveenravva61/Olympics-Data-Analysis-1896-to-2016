

import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff


import Olympics_helpers
import Olympics_preprocesser


athlets = pd.read_csv(r'E:\pycharm\pythonProject\pythonProject6\Data\athlete_events.csv')
region = pd.read_csv('E:\\pycharm\\pythonProject\\pythonProject6\\Data\\noc_regions.csv')

df = Olympics_preprocesser.preprocess(athlets, region)

st.title("Olympics Data Analysis")

user_menu = st.sidebar.radio(
    "Olympics Data Analysis",
    ("Medal Tally", "Overall Analysis", "Country-wise Analysis", "Athlete wise Analysis")
)

if user_menu == "Medal Tally":
  st.sidebar.header("Medal Tally")
  country,years = Olympics_helpers.country_year_list(df)

  selected_year = st.sidebar.selectbox("Select Year", years)
  selected_country = st.sidebar.selectbox("Select Country", country)

  medal_tally = Olympics_helpers.fetch_medal_tally(athlets, selected_year, selected_country)
  if selected_year == 'overall' and selected_country == 'overall':
    st.title('Overall Medal_Tally')
  if selected_year == 'overall' and selected_country != 'overall':
    st.title('Medal Tally in country' + selected_country)
  if selected_year != 'overall' and selected_country == 'overall':
    st.title('Medal Tally in Year '+ str(selected_year))
  if selected_year == 'overall' and selected_country != 'overall':
    st.title('Medal Tally in year' + selected_year + " in " + selected_country)
  st.dataframe(medal_tally)


if user_menu == "Overall Analysis":
  Editions = athlets['Year'].unique().shape[0]-1
  cities = athlets['City'].unique().shape[0]
  sports = athlets['Sport'].unique().shape[0]
  Events = athlets['Event'].unique().shape[0]
  countries = athlets['region'].unique().shape[0]
  athletes = athlets['Name'].unique().shape[0]


  st.title('Top Statistics')
  col1,col2, col3 = st.beta_columns(3)
  with col1:
    st.header("Editions")
    st.title(Editions)
  with col2:
    st.header("Cities")
    st.title(cities)
  with col3:
    st.header('Sports')
    st.title(sports)

  col1,col2, col3 = st.beta_columns(3)
  with col1:
    st.header("Events")
    st.title(Events)
  with col2:
    st.header("Countries")
    st.title(countries)
  with col3:
    st.header('Athletes')
    st.title(athletes)


  nations_over_time = Olympics_helpers.Participating_nations_over(athlets,'region')
  fig =px.line(Nations_over_time, x = 'Year', y = 'Countries')
  st.title('Participating Nations over time')
  st.plotly_chart(fig)

  nations_over_time = Olympics_helpers.Participating_nations_over(athlets,'Events')
  fig =px.line(Nations_over_time, x = 'Year', y = 'Countries')
  st.title('Events over time the Years')
  st.plotly_chart(fig)

  nations_over_time = Olympics_helpers.Participating_nations_over(athlets,'region')
  fig =px.line(Nations_over_time, x = 'Year', y = 'Countries')
  st.title('Athlets over the time')
  st.plotly_chart(fig)


  st.title('No. of Events over time(Every sport)')
  fig, ax = plt.subplots(figsize = (20,20))
  a = athlets.drop_duplicates(['Year','Sport','Event'])
  sns.heatmap(a.pivot_table(index = 'Sport', columns = 'Year', values = 'Event', aggfunc = "count").fillna(0), annot = True)
  st.pyplot(fig)


  st.title('Most_Successful_Athletes')
  sport_list = athlets['Sport'].unique().tolist()
  sport_list.sort()
  sport_list.insert(0, 'Overall')

  selected_sport = st.selectbox('Select a Sport', sport_list)

  c = Olympics_Helpers.most_successful(athlets, selected_sport)
  st.table(c)


if user_menu == "Country-wise Analysis":

  st.sidebar.title('Country-wise Analysis')
  countries = athlets['region'].dropna().unique().tolist()
  countries.sort()

  selectd_country = st.sidebar.selectbox('Select a country', countries)



  country_df = Olympics_helpers.country_wise_analysis(athlets,selectd_country)
  fig = px.line(country_df, x = 'Year', y = 'Medal')
  st.title(country + "Medal Tally over the years")
  st.plotly_chart(fig)

  st.title(selected_country + 'Excels in the following sports')
  pt = Olympics_Helpers.country_event_heatmap(athlets, selected_country)
  fig, ax = plt.subplots(figsize = (20,20))
  ax = sns.heatmap(pt, annot = True)
  st.pyplot(fig)


  st.title('Top 10 Athletes of'+ selected_country)
  top_10 = Olympics_helpers.Country_wise_Most_successful(athlets, selected_country)
  st.table(top_10)

if user_menu == "Athlete wise Analysis":
  athletes_new = athlets.drop_duplicates(subset= ['Name', "region"])
  p1 =athletes_new['Age'].dropna()
  p2 =athletes_new[athletes_new['Medal'] == 'Gold']['Age'].dropna()
  p3 = athletes_new[athletes_new['Medal'] == 'Silver']['Age'].dropna()
  p4 = athletes_new[athletes_new['Medal'] == 'Bronze']['Age'].dropna()


  fig.update_layout(autosize = False, width = 1000, height = 600)
  fig = ff.create_distplot([p1,p2,p3,p4],["Overall Age", 'Gold Medalist', 'Silver Medalist', 'Bronze'], show_hist = False, show_rug = False)
  fig.title('Distribution of Age')
  st.plotly_chart(fig)