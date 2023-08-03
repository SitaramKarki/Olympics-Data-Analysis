import streamlit as st
import pandas as pd
import preprocessor , helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')


df = preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympics Data Analysis till 2016\n-An Initiative By Situ Sporting Limited")

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Player-wise Analysis')
)


if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)



    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    if selected_year == "Overall" and selected_country == "Overall":
        st.title("Overall Medal Tally")
    if selected_year != "Overall" and selected_country == "Overall":
        st.title("Medal Tally in "  + str(selected_year) +" Olympics")
    if selected_year == "Overall" and selected_country != "Overall":
        st.title("Overall Medal Tally of "+ selected_country)
    if selected_year != "Overall" and selected_country != "Overall":
        st.title("Medal Tally of "+ selected_country + " in "+ str(selected_year))


    st.table(medal_tally)


if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]
    cities = df['City'].unique().shape[0]
    sports= df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    import streamlit as st

    st.title("Top Statistics")

    # Create three columns in the first row
    col1, col2, col3 = st.columns(3)

    # Column 1
    with col1:
        st.header("Editions")
        st.title(editions)

    # Column 2
    with col2:
        st.header("Hosts")
        st.title(cities)

    # Column 3
    with col3:
        st.header("Sports")
        st.title(sports)

    # Create three columns in the second row
    col4, col5, col6 = st.columns(3)

    # Column 4
    with col4:
        st.header("Events")
        st.title(events)

    # Column 5
    with col5:
        st.header("Athletes")
        st.title(athletes)

    # Column 6
    with col6:
        st.header("Nations")
        st.title(nations)

    nation_over_time = helper.participating_nations_over_time(df)
    st.title("Participating Nations Over The Year")
    fig = px.line(nation_over_time, x='Year', y='Number_of_countries_participating')
    st.plotly_chart(fig)

    event_over_time = helper.number_of_events_over_time(df)
    st.title("Number Of Events Over The Year")
    fig = px.line(event_over_time, x='Year', y='Number_of_events')
    st.plotly_chart(fig)

    athletes_over_times = helper.number_of_athletes_over_time(df)
    st.title("Number Of Athletes Over The Year")
    fig = px.line(athletes_over_times, x='Year', y='Number_of_athletes')
    st.plotly_chart(fig)

    st.title("Number of Events Over Time for Every Sports")
    fig,ax =plt.subplots(figsize = (25,25))
    x = df.drop_duplicates(['Year', 'Event', 'Sport'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox("Select a Sport",sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)


if user_menu == 'Country-wise Analysis':

    st.sidebar.title("Country-wise Analysis")
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox("Select a Country",country_list)


    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title("Medal Tally of " + selected_country +" Over The Years")
    st.plotly_chart(fig)

    st.title(selected_country +" Excels in the Following Sports")
    pt = helper.country_event_heatmap(df,selected_country)
    fig,ax =plt.subplots(figsize = (25,25))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)


    st.title("Top 10 Athletes of " + selected_country)
    top10_df = helper.most_successful_player_countrywise(df,selected_country)
    st.table(top10_df)

if user_menu == "Player-wise Analysis":
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width = 800,height = 600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
       'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
       'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
       'Water Polo', 'Hockey', 'Rowing', 'Fencing', 'Equestrianism',
       'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
       'Tennis', 'Golf', 'Softball', 'Archery',
       'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
       'Rhythmic Gymnastics', 'Rugby Sevens',
       'Beach Volleyball', 'Triathlon', 'Rugby', 'Lacrosse', 'Polo',
       'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)


    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=800, height=600)
    st.title("Distribution of Age With Respect to Sports for Gold Medalist")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title("Height Versus Weight in DIfferent Games")

    selected_sport = st.selectbox("Select a Sport", sport_list)
    temp_df = helper.weight_vs_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(temp_df, x = 'Height',y = 'Weight',hue = 'Medal',style = 'Sex',s = 60)
    st.pyplot(fig)

    st.title("Man Versus Women Participation in Different Olympics")
    final = helper.men_versus_women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    fig.update_layout(autosize=False,width = 800,height = 600)
    st.plotly_chart(fig)















