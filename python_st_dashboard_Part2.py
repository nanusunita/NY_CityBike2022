################################################ NY BIKE SHARING DASHABOARD #####################################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt
from PIL import Image
from numerize import numerize
import seaborn as sns
import plotly.express as px


########################### Initial settings for the dashboard ##################################################################

st.set_page_config(page_title = 'New York Citi Bike Sharing Strategy Dashboard', layout='wide')
st.title("NY City Bikes Strategy Dashboard")

# Define Sidebar

st.sidebar.title('Dashboard Pages')
page = st.sidebar.selectbox('Select a page below:',
                            ['Intro page',
                             'Most popular stations',
                             'Weather component and bike usage',
                             'Interactive map with aggregated bike trips',
                             'Member Vs Casual riders',
                             'Recommendations'])


########################## Import data ###########################################################################################

df = pd.read_csv('reduced_data_to_plot.csv', index_col = 0)
top20 = pd.read_csv('NYtop20_Stations.csv', index_col = 0)


# ######################################### DEFINE THE PAGES #####################################################################

### 1. Intro Page #

if page == 'Intro page':
    st.markdown("The dashboard will help with the expansion problems NY Citi Bikes Sharing Program currently faces")
    st.markdown("Right now, New York Citi Bike Sharing program has higher demand.This has led to distribution problems—such as fewer bikes at popular bike stations or stations full of docked bikes, making it difficult to return a hired bike—and customer complaints. This dashboard will diagnose where distribution issues stem from — whether it’s sheer numbers, seasonal demand, or something else.")
    st.markdown('#### Dashboard Sections:')
    
    st.markdown('The dropdown menu on the left under "Dashboard Pages" will take you to the different aspects of the analysis our team looked at.')
    
    st.markdown('- Most popular stations')
    st.markdown('- Weather component and bike usage')
    st.markdown('- Interactive map with aggregated bike trips')
    st.markdown('- Member Vs Casual riders')
    st.markdown('- Recommendations')
    

    myImage = Image.open('NY CitiBike 2022.jpg') # Source: https://unsplash.com/photos/blue-citi-bike-bicycles-parked-on-sidewalk-8ol9rD0BHAU
    st.image(myImage)
    st.markdown('Source: https://unsplash.com/s/photos/Citi-bike')



# ######################################### DEFINE THE CHARTS #####################################################################

## Bar chart
elif page =='Most popular stations':
    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color': top20['value'],'colorscale': 'Tealgrn'}))
    fig.update_layout(
    title = 'Top 20 most popular bike stations in New York Citi Bike Sharing Program',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600
    )
    st.plotly_chart(fig, use_container_width=True)
    
    myImage1 = Image.open('Top 20 Stations.PNG') 
    st.image(myImage1)
    
    st.markdown('The bar chart shows that some stations are more popular than others making them stations with higher demand than others. W 21 St &6 Ave is the most popular station with 131K rides in 2022. Based on the quick research, this station is in the middle of Manhattan nearby popular tourist destination and also closed to train station. Both tourist and locals probably are using this station making it most popular. West St & Chambers St along with Broadway & W 58 St are the other two top stations. In general the stations along the water and central park are more popular')


### LINE CHART PAGE: WEATHER COMPONENT AND BIKE USAGE

elif page == 'Weather component and bike usage':

    fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

    fig_2.add_trace(
        go.Scatter(x = df['date'], y = df['bike_rides_daily'], name = 'Daily bike rides', marker={'color': df['bike_rides_daily'],'color': 'blue'}),
    secondary_y = False
    )

    fig_2.add_trace(
    go.Scatter(x=df['date'], y = df['avgTemp'], name = 'Daily temperature', marker={'color': df['avgTemp'],'color': 'red'}),
    secondary_y=True
    )

    fig_2.update_layout(
    title = 'Daily bike trips and temperatures in 2022',
    xaxis_title = 'Dates',
    height = 600
    )
    
    st.plotly_chart(fig_2, use_container_width=True)
    st.markdown('We can see that rise in temperature and the ride volume have similar pattern indicating that they are related to each other. We can see the highest ride volume in the summer months when the temperature is high. The ride volume goes down in the winter months when the temperature is low. There are some peaks and valleys on certain days which might not be temperature related but related to other events. We can see the low number of rides on may 7 (day before mothers day) and september 6 (labor day).')


# ######################################### ADD THE MAP #####################################################################

elif page == 'Interactive map with aggregated bike trips': 

    ### Create the map ###

    st.write("Interactive map showing aggregated bike trips over New York")

    path_to_html = "NY Bike Trips Aggregated.html" 

    # Read file and keep in variable
    with open(path_to_html,'r') as f: 
        html_data = f.read()

    ## Show in webpage
    st.header("Aggregated Bike Trips in New York")
    st.components.v1.html(html_data,height=1000)
    st.markdown("#### Using the filter on the left hand side of the map we can check whether the most popular start stations also appear in the most popular trips.")
    st.markdown("We can see the most popular route is from W 21 St & 6 eve to 9 Ave & W 22 St. Based on quick google search the location is at center of Manhattan nearby Hudson River and the high rise buildigns. It indicates the tourists might be renting the bike. Also employees and tourists might be renting to go to the Chelsea Market. The most popular locations with same starting and ending point is at the edge of central park. This indicates people renting bike and tour the areas around central park and return it at the same destination") 
    
    ### BoxPlot: Member_Casual and Average Temperature

elif page == 'Member Vs Casual riders':

    st.write("The following box plots will show the riding habits of members and casual riders in different temperatures.")
    
    # Create BoxPlot for each category
    plt.figure(figsize=(9,5))
    fig = px.box(df, x = 'member_casual', y = 'avgTemp')


    # Display the figure
    st.plotly_chart(fig)

    st.markdown('''We can see that on average casual rider use the bikes when it is little warmer than the member riders. The number of members is relatively higher than the casual members, which might skew the result - but looks like the range of the temperature that members use bikes is wider than the casual riders. There are some outliers in the casual riders compared to member riders.''')
    
    ### CONCLUSIONS AND RECOMMENDATIONS

else:
    
    st.markdown('### Here are some conclusions and recommendations based on our study:')
    
    bikes = Image.open('NY CitiBike Snow.jpg')  # Source: https://nycdotbikeshare.info/news-and-events/citi-bike-launch-nyc
    st.image(bikes)
    st.markdown('Source: https://www.wsj.com/articles/SB10001424052702304256404579451770072629130')
    
    st.markdown('- Some of the stations are more popular, especially towards the central park and other tourist destinations. These need more bikes compared to others - especially in the summer months when the temperature is higher.')
    
    st.markdown('- Weather has to be considered as this is important factor for bike usage. As the bike is being used less in the winter months. Probably winter months could be used for bike maintenance, and creating plan for next summer.')
   
    st.markdown('- We see that members use more bikes than casual members especially in colder temperature. It might be good idea to do marketing for membership programs especially in winter months to create more demand of bikes.')