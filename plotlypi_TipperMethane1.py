import pandas as pd
import numpy as np
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html

           
        

def import_data_tipper(csv_name, volume = None, tank_id = None, tipper=['Methane','CO2','OH'], datatype=float):
    """DOCSTRING- Expand the documentation heere"""
     
    # Declare Variables
    colnames=['Time','data']
    df_final = pd.DataFrame()
    i = 0   # Index used to assign tipper values. We add 1 in the loop so we actually start by asigning 1 to the tank id.
    # now we operate on the correct format CSV
    df = pd.read_csv(csv_name,index_col=0, skiprows=1, names = colnames)
    # Preprocessing of data read
    df.dropna(inplace = True) 
    df['datetime'] = pd.to_datetime(df.index, format="%a %b %d %X %Y")
    df.set_index('datetime', inplace=True)
    df_split = df.loc[:,'data'].str.split(',')
    
    df.drop('data',axis=1, inplace=True)
    # Checking that the length of the array from df_split is the same as the lenght of tipper values provided
        # This is necessary to run the code without errors
        # If check isnt met, quit the script
    if len(df_split[0]) != len(tipper):
        print('ERROR: The length of the columns specified must be the same length as the array created by the splitting of the "data" column in df_split.')
        quit()

    # For each individual tipper (i.e. the length of array we expect from the split), we append the data by rows
    # Using the dataframe.append method
    for t in tipper:
        df_tipper = df
        df_tipper['tank_id'] = i + 1    #Python index starts at 0, so to set to tank id, we add 1
        df_tipper['data'] = df_split.str[i].astype(float, errors='raise') # change this to test data name
        df_final = df_final.append(df_tipper)
        i+=1
    
    # Return df_final
    return df_final


def import_tank_data(csv_name, tank_id):
    colnames=['Time','data'] 
    # now we operate on the correct format CSV
    df = pd.read_csv(csv_name,index_col=0, skiprows=1, names = colnames)
    df2 = df.loc[:,'data'].str.split(',')

    df['Methane'] = df2.str[0].astype(float, errors='ignore')
    df['CO2'] = df2.str[1].astype(float, errors='ignore')
    df['OH'] = df2.str[2].astype(float, errors='ignore')
    

    df.drop('data',axis=1, inplace=True)
    df.dropna(inplace = True) 

    df['datetime'] = pd.to_datetime(df.index, format="%a %b %d %X %Y")
    df.set_index('datetime', inplace=True)
    df['tank_id'] = tank_id
   # df['Methane'].round(decimals=2)
    return df


dfs = []
dfs_group1 = []
dfs_group2 = []

csv_names = {1:'gas_Sensor1.csv',2:'gas_Sensor2.csv',3:'gas_Sensor3.csv'}

csv_Flowdata = {1:'gas_Flow.csv'}

# Iterate through each csv to import data, appending to list of dataframes "dfs"
for tank, csv in csv_names.items():
    df = import_tank_data(csv, tank)
    dfs.append(df)
   

# Iterate through each csv to import data, appending to list of dataframes "list_dfs"
for tank, csv in csv_Flowdata.items():
    df_final = import_data_tipper(csv, tank,tipper=['Tipper1','Tipper2','Tipper3'])
    #df_final.append(df)
      

# Create a single dataframe
df_tipper = pd.concat(dfs, axis=0)
df_tipper = df_tipper.round({'Methane':4, 'CO2':4, 'OH':4})
df_tipper['Combustables'] = df_tipper.loc[:,['Methane','OH']].sum(axis=1)
df_tipper.reset_index(inplace=True)
df_tipper.set_index(['tank_id'], inplace=True)



tank_id = 0
for x in range(3) :
    tank_id += 1 
    tank_id_group = (df_tipper.loc[tank_id])
    df_tank_id_group = pd.DataFrame(tank_id_group)
    df_tank_id_group['date'] = df_tank_id_group['datetime'].dt.date
    #print(df_tank_id_group)
    df_group2 = df_tank_id_group.groupby(['date','tank_id']).mean()
 

    df_average_conact = pd.DataFrame(df_group2)
    dfs_group1.append(df_average_conact)    
  
df_Methane = pd.concat(dfs_group1, axis=0)  
df_Methane.reset_index(inplace=True)
df_Methane.set_index(['date'], inplace=True)


df_final.reset_index(inplace=True)
df_final['volume'] = df_final.data[(df_final.data.shift(1) <= df_final.data) & (df_final.data.shift(-1) < df_final.data)]
df_final.set_index(['tank_id'], inplace=True)




tank_id = 0
for x in range(3) :
    tank_id += 1 
    tank_id_group2 = (df_final.loc[tank_id])
    df_tank_id_group2 = pd.DataFrame(tank_id_group2)
    df_tank_id_group2['date'] = df_tank_id_group2['datetime'].dt.date
    df_group2 = df_tank_id_group2.groupby(['date','tank_id']).sum()
    df_average_conact2 = pd.DataFrame(df_group2)
    dfs_group2.append(df_average_conact2)

df_volume = pd.concat(dfs_group2, axis=0)  
df_volume.reset_index(inplace=True)
df_volume.set_index(['date'], inplace=True)
#df_volume= df_volume[df_volume['volume'] != 0]
df_volume.drop(columns=['data'], inplace=True )



df_Methane.reset_index(inplace=True)
df_Methane.set_index(['tank_id', 'date'], inplace=True)
df_volume.reset_index(inplace=True)
df_volume.set_index(['tank_id', 'date'], inplace=True)



## calculation ##


result = pd.merge(df_Methane, df_volume, on=['tank_id','date'], how='outer')
df_combined_gas = pd.DataFrame(result)
df_combined_gas= df_combined_gas[df_combined_gas['volume'] != 0]
df_combined_gas_calculation = df_combined_gas
df_combined_gas_calculation['Combustables'] += 4
df_combined_gas_calculation['Combustables'] /= 100
df_combined_gas_calculation2 = pd.DataFrame()
df_combined_gas_calculation2['volume_Combustable_biogas(ml)'] = df_combined_gas_calculation["Combustables"] * df_combined_gas_calculation["volume"]
df_volume_combustables = pd.merge(df_combined_gas_calculation, df_combined_gas_calculation2, on=['tank_id','date'], how='outer')
pd.to_numeric(df_volume_combustables['volume_Combustable_biogas(ml)'], downcast="float")
df_volume_combustables['daily_energy_production(kWh)'] = (df_volume_combustables['volume_Combustable_biogas(ml)']/1000) * 0.0105
df_volume_combustables['pH'] = "0"
df_volume_combustables['COD'] = "0"
df_volume_combustables['BOD'] = "0"
df_volume_combustables['Total N'] = "0"
df_volume_combustables['TS'] = "0"
df_volume_combustables['VS'] = "0"
df_volume_combustables.reset_index(inplace=True)
#print(df_volume_combustables)



# compression_opts = dict(method='zip',
#                         archive_name='barrel_gas_data.csv')  
# df_volume_combustables.to_csv('barrel_gas_data.zip', index=False,
#           compression=compression_opts) 




df_Methane.reset_index(inplace=True)
df_Methane.set_index(['date'], inplace=True)
df_volume.reset_index(inplace=True)
df_volume.set_index(['date'], inplace=True)
df_final.reset_index(inplace=True)
df_final.set_index(['datetime'], inplace=True)
df_volume_combustables.reset_index(inplace=True)
df_volume_combustables.set_index(['date'], inplace=True)
df_tipper.reset_index(inplace=True)
df_tipper.set_index(['datetime'], inplace=True)

print(df_volume_combustables)
fig1 = px.line(df_volume_combustables, 
             x=df_volume_combustables.index, 
             y='daily_energy_production(kWh)', 
             title='Daily Energy Production',
             color='tank_id')
fig1.update_xaxes(title_text='Date')
fig1.update_yaxes(title_text='Energy (kWh)')  

fig2 = px.line(df_Methane, 
             x=df_Methane.index, 
             y='Combustables', 
             title='Daily Combustables',
             color='tank_id')
fig2.update_xaxes(title_text='Date')
fig2.update_yaxes(title_text='Daily Combustables (%)')

fig3 = px.line(df_volume, 
             x=df_volume.index, 
             y='volume', 
             title='Daily Volume',
             color='tank_id')
fig3.update_xaxes(title_text='Date')
fig3.update_yaxes(title_text='Volume (ml)')

fig4 = px.line(df_final, 
             x=df_final.index, 
             y='data', 
             title='Tipper data from live stream',
             color='tank_id')
fig4.update_xaxes(title_text='Date/Time')
fig4.update_yaxes(title_text='Volume (ml)')


fig5 = px.line(df_tipper, 
             x=df_tipper.index, 
             y='Methane', 
             title='Dynament data from live stream',
             color='tank_id')
fig5.update_xaxes(title_text='Date')
fig5.update_yaxes(title_text='Energy (kWh)')     


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([

    html.H1("Tipper Stream"),
    html.Br(),
    dcc.Graph(figure=fig4),

    html.H2("Dynament Stream"),
    html.Br(),
    dcc.Graph(figure=fig5),

    html.H3("Energy"),
    html.Br(),
    dcc.Graph(figure=fig1),

    html.H4("Combustables"),
    html.Br(),
    dcc.Graph(figure=fig2),

    html.H5("Volume"),
    html.Br(),
    dcc.Graph(figure=fig3),


])

if __name__ == '__main__':
    app.run_server(debug=True)