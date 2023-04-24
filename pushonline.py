import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import mysql.connector
import pandas as pd 
import pygsheets

gc = pygsheets.authorize(service_file='spreadsheet_interface/uplifted-might-336521-5dee01c27d1d.json')



db_conn = mysql.connector.connect(
      host="34.89.81.147",
      user="root",
      passwd="wase2022",
      database="cabinet_datasets"
    )


print('here')

current_db = pd.read_sql('SELECT*FROM rs_current_data', con=db_conn)
temp_db_load = pd.read_sql('SELECT*FROM temperature', con=db_conn)
probe_names = temp_db_load['probe_id'].unique().tolist()
flow_db = pd.read_sql('SELECT*FROM flowmeter', con= db_conn)
reactor_names = flow_db['Name'].unique().tolist()
reactor_names.sort() 
print(reactor_names) 

reactor_names[9] = '1D'
reactor_names[10] = '2D'
reactor_names[11] = '3D'

print('here')

################################
################################
#####  sorting temperature #####  
################################
################################

df = temp_db_load.copy()
ls = []
for probe in probe_names:
  df_id = df[df['probe_id'] == probe]
  df_id = df_id.drop_duplicates(subset=['datetime'])
  df_id = df_id.pivot(index='datetime', columns='probe_id', values='temperature_degC')
  ls.append(df_id)
temp_db = pd.concat(ls, axis = 0)
temp_db = temp_db.groupby([pd.Grouper(freq='D', level='datetime')])['TA', 'TB', 'TC', 'TD'].max()
temp_db['cabinet_ambient_temp_degC'] = (temp_db['TA'] + temp_db['TB'])/2
temp_db['reactor_internal_temp_degC'] = (temp_db['TC'] + temp_db['TD'])/2


################################
################################
######  sorting current  ####### 
################################
################################

current_db.set_index(['datetime', 'Name'], inplace=True)

current_db_D = current_db.groupby([pd.Grouper(freq='D', level='datetime'), pd.Grouper(level='Name')])['voltageV', 'currentA', 'powerP'].mean()


current_db_D.reset_index(inplace=True)
current_db_D['tank_num'] = current_db_D['Name'].str[1]
current_db_D.set_index(['tank_num', 'datetime', 'Name'], inplace=True)
current_db_D['mean_current_A'] = current_db_D.groupby(['tank_num', 'datetime'])['currentA'].mean()






################################
################################
#####  sorting flow data  ######
################################
################################



flow_db['Name'] = flow_db['Name'].replace(['4A','4B', '4C'],['1D', '2D','3D'])
flow_db['tank_num'] = flow_db['Name'].str[1]

ls = []
flow_db.to_csv('combined_test.csv')

for reactor in reactor_names:
  df = flow_db[flow_db['Name'] == reactor]
  df.set_index(['datetime'], inplace=True)
  
  df['flow_rate_mlD'] = df['total_vol_since_startml'].diff(periods = 1)
  df = df[df.select_dtypes(include=[np.number]).ge(0).all(1)]
  ls.append(df)
flow_db = pd.concat(ls, axis = 0)
flow_db.dropna(inplace=True)
flow_db.reset_index(inplace=True)
flow_db.set_index(['datetime', 'Name'], inplace=True)
flow_db_1 = flow_db.groupby([pd.Grouper(freq='D', level='datetime'), pd.Grouper(level='Name')])['total_vol_since_startml', 'total_tips_since_start', 'volume_this_tip_intervalml','tank_num'].max()
flow_db_2 = flow_db.groupby([pd.Grouper(freq='D', level='datetime'), pd.Grouper(level='Name')])['flow_rate_mlD'].sum()
flow_db = pd.concat([flow_db_1, flow_db_2], axis = 1)
flow_db.reset_index(inplace=True)
flow_db.set_index(['tank_num', 'datetime','Name'], inplace=True)



flow_db['mean_flow_rate_mlD'] = flow_db.groupby(['tank_num', 'datetime'])['flow_rate_mlD'].mean()



# flow_db = flow_db.drop(columns=['total_vol_since_startml', 'total_tips_since_start', 'volume_this_tip_intervalml'])





combined = pd.concat([flow_db, current_db_D], axis = 1)
print(combined)






combined.reset_index(inplace=True)

frame_ls = []
for name in reactor_names:
    df = combined.loc[combined['Name'] == name]
    df = df.drop(columns=['Name'])
    df.set_index('datetime', inplace=True)
    
    df = df.drop(columns=['total_vol_since_startml', 'total_tips_since_start', 'volume_this_tip_intervalml', 'tank_num', 'mean_flow_rate_mlD', 'powerP', 'mean_current_A'])
    df.columns = pd.MultiIndex.from_product([['reactor' + name],['flow_rate_mlD', 'volatgeV', 'currentC']])

    frame_ls.append(df)



df_1Dsheet = pd.concat(frame_ls, axis=1)

df_1Dsheet.reset_index(inplace=True)


#open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
sht1 = gc.open_by_key('1hf-qRd-VOd6lqdAdgygNJQ-fsVAFC01ha25zEokKm1E')

#select the first sheet 
wks = sht1[6]

#update the first sheet with df, starting at cell B2. 
wks.set_dataframe(df_1Dsheet,(1,1))


