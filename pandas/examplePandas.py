import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

serie = pd.Series([1,2,3])

serie.name="nombre"

df = pd.DataFrame({'column1':[1,2,3,4],'column2':['a','b','c','d']})

print(df.shape)#Indica tamaño
print("**********************************")
ul = pd.read_excel('practice.xlsx')
#ul = pd.read_csv('practices.csv') 
print(ul)
print("**********************************")
print(ul.head())#Return first five rows
print("**********************************")
print(ul.head(2))#Return fist two rows
print("**********************************")
print(ul.tail())#Return last five rows
print("**********************************")
#We don´t have name for the columns, but we can create it...

names = ["Month","Light","Water","Gas"]
ul.columns=names
print(ul.head())

#print(ul.columns) Return the names of columns

#ul.index Return index
print("**********************************")
print(ul["Light"].value_counts())

print("**********************************")

#print(ul.T)We can change position of rows and columns
print("**********************************")
print(ul.sort_values("Light",ascending=False)) #We can sort by the value of a column
print("**********************************")
print(ul[["Light","Gas"]])#Select the column we want to show
print("**********************************")
print(ul[:4])#Show first *** rows
print("************SPECIFIC ROWS AND COLUMNS**********************")
print(ul.iloc[[0,10],[0,1,2,3]])#Show content of specific rows and columns
print("**********************************")
print(ul[ul["Light"]>100]) #Show the bill major to...
print(ul[(ul["Light"]>5)&(ul["Gas"]>5)]) #Or filter results
print("**********************************")
print(ul["Light"]+ul["Water"]) #Operations between columns
print("**********************************")
ul.isna().sum().sum() #missed cases

print(ul) #Show all values

print(ul["Gas"].fillna(0)) #Replace null value by...

ul["Gas"] = ul["Gas"].fillna(1) #Now replace null value by... in dataframe

print(ul)
print("**********************************")
#Compute means
print(ul["Gas"].mean())
print("**********************************")
#Compute median
print(ul["Gas"].median())
print("**********************************")
print(ul['Light'].apply(lambda x:-x)) #Lambda x let us acces differente values Light
print("**********************************")
ul_group = ul.groupby('Month')['Light'].mean()
print(ul_group) #Return mean of every month (only light)
ul_group.name="meanLight"
ul_join = ul.join(ul_group,on=["Month"],how="inner")
print(ul_join)
#Graphically display the data
#ul["Light"].plot()
#ul.plot(figsize=[10,10]) #size
ul.plot(kind='bar')
plt.savefig("Image.jpg")#Save grapthics
plt.show() #desplegamos el gráfico