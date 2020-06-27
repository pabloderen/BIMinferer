import pandas as pd
import json
import urllib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_absolute_error
import numpy as np
import dill
#Here it go the the route of access of the model (Model_rfc_dill.sav)
model = dill.load(open("Model_rfc_dill.sav","rb"))

column=['properties_Dimensions_Length', 'Material_Number','Domestic Cold Water', 'Domestic Hot Water', 'Fire Protection Dry','Fire Protection Wet', 'Hydronic Return', 'Hydronic Supply', 'Other','Sanitary', 'Vent', '1 1/2"', '1 1/4"', '1 3/8"', '1"', '1/2"', '10"', '12"', '14"', '16"', '2 1/2"', '2"', '3"', '3/4"', '30"', '36"', '4"', '5"', '6"', '8"']
#here We create a DataFrame with the same Shape of the one that was used to make predictions
model_1=pd.DataFrame(index=column).T
model_1
#here we ask for the Values:

Size=input("Size: ") # The Size of the Diameters is ingresed like: '1 1/2"', '1 1/4"', '1 3/8"', '1"', '1/2"'
Length=float(input("Length: ")) # The lenfth has to be inputted as: 4.56 format
Classification=input("Classification: ") #You can input a System Classification like: "Domestic Cold Water", "Sanitary", "Fire Protection Wet","Vent"
values={"Size":Size,"Length":Length,"Classification":Classification}

values
#this list is just for make the new_row dictionary 
items=[values["Classification"],values["Size"]]
# Then create a dictionary to make a new row of the dataframe
new_row={}

for i in model_1.columns:
  if i == "properties_Dimensions_Length":
    new_row[i]=float(values["Length"])
  elif i in items:
    new_row[i]=1
  else:
      new_row[i]=0
#We add the new row to the data frame "k"

k=model_1.append(new_row, ignore_index=True)
#this is the DataFrame that we will infer the result
X_infer = k.drop('Material_Number',axis=1)
predic=model.predict(X_infer)
a=int(predic)
dict={0: 'Copper',1: 'Steel, Carbon',
 2: 'NaN',3: 'PVC',
 4: 'CP_PI - Copper - ASTM B88 H.D.',
 5: 'Carbon Steel - ASTM A53 B',
 6: 'Cast Iron', 7: 'Black Steel',
 8: 'Carbon Steel',9: 'Ductile Iron'}
print(dict[a])
