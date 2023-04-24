import pandas as pd
import numpy as np
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html

def import_tank_data(csv_name, tank_id):
    colnames=['Time','data'] 
    # now we operate on the correct format CSV
    df = pd.read_csv(csv_name,index_col=0, skiprows=1, names = colnames)
    df2 = df.loc[:,'data'].str.split(',')

    df['Methane'] = df2.str[0].astype(float, errors='raise')
    df['CO2'] = df2.str[1].astype(float, errors='raise')
    df['OH'] = df2.str[2].astype(float, errors='raise')

    df.drop('data',axis=1, inplace=True)
    df.dropna(inplace = True) 

    df['datetime'] = pd.to_datetime(df.index, format="%a %b %d %X %Y")
    df.set_index('datetime', inplace=True)
    df['tank_id'] = tank_id
   # df['Methane'].round(decimals=2)
    return df


# Empty list to append all data read, this allows us to concatenate the data
dfs = []

#CSV set in key value pairs so that a tank ID can be easily assigned
csv_names = {1:'gas_Sensor1.csv',2:'gas_Sensor2.csv',3:'gas_Sensor3.csv'}

# Iterate through each csv to import data, appending to list of dataframes "dfs"
for tank, csv in csv_names.items():
    df = import_tank_data(csv, tank)
    dfs.append(df)
  

# Create a single dataframe
df_dynaments = pd.concat(dfs, axis=0)
#df['Methane'].apply(np.ceil)
df_dynaments



def import_tank_data_tipper(csv_name, tank_id = None, tipper=['Methane','CO2','OH'], datatype=float):
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
        df_tipper['Gas Production (ml)'] = df_split.str[i].astype(float, errors='ignore') # change this to test data name
        df_final = df_final.append(df_tipper)
        i+=1
    
    # Return df_final
    return df_final

    
csv_names = {1:'gas_Flow.csv'}

# Iterate through each csv to import data, appending to list of dataframes "list_dfs"
for tank, csv in csv_names.items():
    df_final = import_tank_data_tipper(csv, tank,tipper=['Tipper1','Tipper2','Tipper3'])
    #df_final.append(df)

df_final
# import_tank_data_tipper.__doc__
# Iterate through each csv to import data, appending to list of dataframes "dfs"



fig1 = px.line(df_dynaments, 
             x=df_dynaments.index, 
             y='Methane', 
             title='Methane Production',
             color='tank_id')
             

fig2 = px.line(df_final, 
             x=df_final.index, 
             y='Gas Production (ml)', 
             title='Gas Production',
             color='tank_id')
        

fig1.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="Hour", step="hour", stepmode="backward"),
            dict(count=1, label="Day", step="day", stepmode="backward"),
            dict(count=7, label="Week", step="day", stepmode="backward"),
            dict(step="all")
        ])
    )
)

fig2.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="Hour", step="hour", stepmode="backward"),
            dict(count=1, label="Day", step="day", stepmode="backward"),
            dict(count=7, label="Week", step="day", stepmode="backward"),
            dict(step="all")
        ])
    )
)




external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("Methane Data"),
    html.Br(),
    dcc.Graph(figure=fig1),

    html.H2("Tipper data"),
    html.Br(),
    dcc.Graph(figure=fig2),

])

if __name__ == '__main__':
    app.run_server(debug=True)