#!/usr/bin/env python
# coding: utf-8

# In[1]:


from datetime import datetime
import numpy as np
import pandas as pd
pd.set_option('display.max_rows', 500)


# In[2]:


import seaborn as sns
import matplotlib.pyplot as plt
#%matplotlib inline


# In[3]:


import chart_studio.plotly as py
import plotly.graph_objs as go
import plotly.express as px
from plotly.offline import download_plotlyjs,init_notebook_mode,plot,iplot
init_notebook_mode(connected=True)


# # Scrap Data From The Github Site (Link Below)

# Github Data API - https://raw.githubusercontent.com/2020PB/police-brutality/data_build/all-locations.json
# Github Repository of Police Brutality - https://github.com/2020PB/police-brutality/blob/master/README.md

# In[4]:


pb_data_raw = pd.read_json(r'https://raw.githubusercontent.com/2020PB/police-brutality/data_build/all-locations.json')


# # Tests on Data

# In[5]:


# Check of number of records in repository
len(pb_data_raw)


# # Set data up into proper matrix format 

# In[6]:


# creates a dictionary from the List of Data Frame Names (Keys) and the Data Frame Files (Values) themselves
dict_of_pb_dfs = {}

for pb_record_idex_num in range(0,len(pb_data_raw['data'])): 
    globals()["pb_df_{}".format(pb_record_idex_num)]  = pd.DataFrame(pb_data_raw['data'][pb_record_idex_num])
    dict_of_pb_dfs["pb_df_{}".format(pb_record_idex_num)] = globals()["pb_df_{}".format(pb_record_idex_num)]
    
# Reduces the record numbers to 1 per incident in each data frame
for pb_df in dict_of_pb_dfs.keys():
    num_count = len(dict_of_pb_dfs[pb_df])-1
    while num_count > 0:
        dict_of_pb_dfs[pb_df].drop(num_count, inplace = True)
        num_count -= 1
        
# Concatenate the individual data frames into one dataframe with all the incident data (one link/record per incident)
list_of_values = list(dict_of_pb_dfs.values())
pd_consolidated = pd.concat(list_of_values, sort = True)
pd_consolidated['incident_value'] = 1


# In[7]:


date_text = '2020-06-23'
pd_date_query = pd_consolidated[pd_consolidated['date'] == date_text]
#pd_date_query 


# # Graphing

# In[8]:


fig = go.Figure(data=[go.Bar(
    x=pd_date_query['state'],
    y=pd_date_query['incident_value'],
    marker_color= 'black',
    name = 'Police Brutality Incident Captured on Video',
    text = pd_date_query['city'],
    hovertext = pd_date_query['name'],
    customdata = pd_date_query['date'],
    hovertemplate = "City: %{text}<br>Incident Description: %{hovertext}<br>Date of Incident: %{customdata}<extra></extra>",
    width = .8,
    showlegend = True,
)])

# datetime object containing current date and time
now = datetime.now()
# dd/mm/YY H:M:S
dt_string = now.strftime("%m/%d/%Y %H:%M:%S")

fig.update_layout(title_text = '2020 Police Brutality: {} Incidents Captured on Video<br>Data from {}<br>Date Created: {}'.format(len(pd_date_query),date_text,dt_string),
                  barmode='group',
                  xaxis_tickangle=-45,
                  autosize=True,
#                   width=1500,
#                   height=1200,
                  legend_orientation="h",
                  legend=dict(x=.875, y=0.99)
                 )

fig.write_html(r"C:\Users\cdwhi\Documents\Python\My_Code\Police_Brutality_2020\PB_2020_Bar_Graph_Count_by_State_20200623\index.html")
fig.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




