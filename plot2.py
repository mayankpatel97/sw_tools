
import sys
import pandas as pd
from matplotlib import pyplot as plt

n = len(sys.argv)
#print("Total arguments passed:", n)

if n < 2 : 
    print("Please enter the filename.")
else:
    # Arguments passed
    print("\nInput File:", sys.argv[1])


    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    columns = ['lat', 'lon']

    #df = pd.read_csv("gnssdata10.csv", usecols=columns)
    filePath = sys.argv[1]
    df = pd.read_csv(filePath, usecols=columns)
    print(df)


    #plt.plot(df.lat, df.lon,'o') # lines
    plt.plot(df.lat, df.lon,'o') # dots
    plt.show()



'''
import plotly.express as px
import pandas as pd

df = pd.read_csv("output.csv")

fig = px.scatter_geo(df,lat='lat',lon='lon')
fig.update_layout(title = 'World map', title_x=0.5)
fig.show()
'''

'''
import matplotlib.pyplot as plt
plt.scatter(x=df['lat'], y=df['lon'])
plt.show()
'''
