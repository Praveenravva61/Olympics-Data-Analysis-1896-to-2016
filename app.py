
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import scipy
import plotly.figure_factory as ff


import Olympics_helpers
import Olympics_preprocesser



# Call the function to apply the background
Olympics_helpers.add_bg_from_url()


athletes = pd.read_csv(r"X:\Data Science\Pro_Projects\Data store\athlete_events.csv")
region = pd.read_csv(r"X:\Data Science\Pro_Projects\Data store\noc_regions.csv")

athlets = Olympics_preprocesser.preprocess(athletes,region)



st.sidebar.image('https://c.tenor.com/qsiepKaQZKEAAAAC/olympic-flame-olympic-fire.gif')
st.title("Olympics Data Analysis 1896 - 2016")

user_menu = st.sidebar.radio(
    "Olympics Data Analysis",
    ("Medal Tally", "Overall Analysis", "Country-wise Analysis", "Athlete wise Analysis")
)

if user_menu == "Medal Tally":
  st.sidebar.header("Medal Tally")
  country,years = Olympics_helpers.country_year_list(athlets)

  selected_year = st.sidebar.selectbox("Select Year", years)
  selected_country = st.sidebar.selectbox("Select Country", country)

  medal_tally = Olympics_helpers.fetch_medal_tally(athlets, selected_year, selected_country)

  st.dataframe(medal_tally)
  if selected_country != 'Overall' and selected_year != 'Overall':
    st.title(f'{selected_country} - {selected_year}')
    country_athletes = Olympics_helpers.athlets_country(athlets, selected_country, selected_year)
    st.dataframe(country_athletes)

if user_menu == "Overall Analysis":
  Editions = athlets['Year'].unique().shape[0]-1
  cities = athlets['City'].unique().shape[0]
  sports = athlets['Sport'].unique().shape[0]
  Events = athlets['Event'].unique().shape[0]
  countries = athlets['region'].unique().shape[0]
  athletes = athlets['Name'].unique().shape[0]


  st.title('Top Statistics')
  col1,col2, col3 = st.columns(3)
  with col1:
    st.header("Editions")
    st.title(Editions)
  with col2:
    st.header("Cities")
    st.title(cities)
  with col3:
    st.header('Sports')
    st.title(sports)

  col1,col2, col3 = st.columns(3)
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
  fig =px.line(nations_over_time, x = 'Year', y = 'region')
  st.title('Participating Nations over time')
  st.plotly_chart(fig)

  nations_over_time = Olympics_helpers.Participating_nations_over(athlets,'Event')
  fig =px.line(nations_over_time, x = 'Year', y = 'Event')
  st.title('Events over the Years')
  st.plotly_chart(fig)

  nations_over_time = Olympics_helpers.Participating_nations_over(athlets, 'region')
  # Create the line chart
  figur = px.line(nations_over_time, x='Year', y='region')

  # Set the title and plot the chart with a unique key
  st.title('Athletes over the time')
  st.plotly_chart(figur, key="athletes_over_time_chart")  # Add a unique key here

  st.title('No. of Events over time (Every sport)')

  # Create a figure and axis object
  fig, ax = plt.subplots(figsize=(20, 20))

  # Create the heatmap on the axes
  a = athlets.drop_duplicates(['Year', 'Sport', 'Event'])
  sns.heatmap(a.pivot_table(index='Sport', columns='Year', values='Event', aggfunc="count").fillna(0), annot=True,
              ax=ax)

  # Display the figure (not the heatmap/axes)
  st.pyplot(fig)

  st.title('Most_Successful_Athletes')
  sport_list = athlets['Sport'].unique().tolist()
  sport_list.sort()
  sport_list.insert(0, 'Overall')

  selected_sport = st.selectbox('Select a Sport', sport_list)

  c = Olympics_helpers.Most_successful(athlets, selected_sport)
  st.table(c)


if user_menu == "Country-wise Analysis":

  st.sidebar.title('Country-wise Analysis')
  countries = athlets['region'].dropna().unique().tolist()
  countries.sort()

  selectd_country = st.sidebar.selectbox('Select a country', countries)



  country_df = Olympics_helpers.country_wise_analysis(athlets,selectd_country)
  fig = px.line(country_df, x = 'Year', y = 'Medal')
  st.title(selectd_country + " Medal Tally over the years")
  st.plotly_chart(fig)

  st.title(selectd_country + 'Excels in the following sports')
  pt = Olympics_helpers.country_event_Heatmap(athlets, selectd_country)
  fig, ax = plt.subplots(figsize = (20,20))
  ax = sns.heatmap(pt, annot = True)
  st.pyplot(fig)


  st.title('Top 10 Athletes of '+ selectd_country)
  top_10 = Olympics_helpers.Country_wise_Most_successful(athlets, selectd_country)
  st.table(top_10)

if user_menu == "Athlete wise Analysis":
  athletes_new = athlets.drop_duplicates(subset= ['Name', "region"])
  p1 =athletes_new['Age'].dropna()
  p2 =athletes_new[athletes_new['Medal'] == 'Gold']['Age'].dropna()
  p3 = athletes_new[athletes_new['Medal'] == 'Silver']['Age'].dropna()
  p4 = athletes_new[athletes_new['Medal'] == 'Bronze']['Age'].dropna()


  fig = ff.create_distplot([p1,p2,p3,p4],["Overall Age", 'Gold Medalist', 'Silver Medalist', 'Bronze'], show_hist = False, show_rug = False)
  fig.update_layout(autosize=False, width=1000, height=600)
  st.title('Distribution of Age')
  st.plotly_chart(fig)

  x = []
  name = []
  famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                 'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                 'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                 'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                 'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                 'Tennis', 'Golf', 'Softball', 'Archery',
                 'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                 'Rhythmic Gymnastics', 'Rugby Sevens',
                 'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
  for sport in famous_sports:
    temp_df = athlets[athlets['Sport'] == sport]
    x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
    name.append(sport)

  fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
  fig.update_layout(autosize=False, width=1000, height=600)
  st.title("Distribution of Age wrt Sports(Gold Medalist)")
  st.plotly_chart(fig)

  sport_list = athlets['Sport'].unique().tolist()
  sport_list.sort()
  sport_list.insert(0, 'Overall')

  st.title('Height Vs Weight')

  selected_sport = st.selectbox('Select a Sport', sport_list)

  # Get the filtered data based on the selected sport
  temp_df = Olympics_helpers.weight_v_height(athlets, selected_sport)

  # Create the scatter plot
  fig, ax = plt.subplots(figsize=(8, 6))  # Optional: Set figure size for better display
  sns.scatterplot(
    x='Weight', y='Height',
    hue='Medal', style='Sex',
    s=60, data=temp_df, ax=ax
  )

  # Display the plot in Streamlit
  st.pyplot(fig)
  st.title("Men Vs Women Participation Over the Years")
  final = Olympics_helpers.men_vs_women(athlets)
  fig = px.line(final, x="Year", y=["Male", "Female"])
  fig.update_layout(autosize=False, width=1000, height=600)
  st.plotly_chart(fig)


