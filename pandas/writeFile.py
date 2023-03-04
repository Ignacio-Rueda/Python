import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image



houseHoldExpenses2020 = {
    "Bills" : ["Light","Water","Gas"],
    "January":[50,30,60],
    "February":[65,0,150],
    "March":[0,95,123]
}

houseHoldExpenses_2020_def = pd.DataFrame(houseHoldExpenses2020)
houseHoldExpenses_2020_def.to_csv("houseHoldExpenses_2020.csv")
houseHoldExpenses_2020_def.to_excel("houseHoldedExpenses_2020.xlsx")

#By default, while writing the DataFrame into a CSV file, the values are separated by a comm. If we want
#to use any other symbols as a separator, we can specify it using the sep parameter.


houseHoldExpenses2021 ={
    "Bills":["Light","Water","Gas"],
    "January":[80,90,100],
    "February":[80,90,100],
    "March":[80,90,100],
}
houseHoldExpenses2021_def = pd.DataFrame(houseHoldExpenses2021)
houseHoldExpenses2021_def.to_csv("houseHoldExpenses_2021.csv",index=False,sep="\t")
print(houseHoldExpenses2021_def)

houseHoldExpenses2022 ={
    "Bills":["Light","Water","Gas"],
    "January":[80,90,100],
    "February":[80,90,100],
    "March":[80,90,100],
}
houseHoldExpenses2022_def = pd.DataFrame(houseHoldExpenses2021)
houseHoldExpenses2022_def.to_csv("houseHoldExpenses_2022.csv",index=False,sep=";")
print(houseHoldExpenses2022_def)