import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import warnings
from sklearn.ensemble import RandomForestRegressor
warnings.filterwarnings("ignore")
pd.set_option('display.max_columns', None)


def crop_prediction(sample):
    df = pd.read_csv("/home/andalus/Documents/django/AgriTech/crop_last_data.csv")
    sum_maxp = df["Production"].sum()
    # df["percent_of_production"] = df["Production"].map(lambda x:(x/sum_maxp)*100) 
    original = df
    data_dum = df[df["Crop"] == sample[1]]
    # data_dum = pd.get_dummies(df) 
    reserve = data_dum[data_dum["Zone_Name"] == sample[0]]

    if len(reserve) > 10:
        data_dum = reserve
    print(data_dum)
    if(len(data_dum) < 10):
        data_dum = original
    data_dum = data_dum.drop(["Zone_Name", "Crop"], axis=1)
    x = data_dum.drop("Production",axis=1)
    y = data_dum[["Production"]]

    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.33, random_state=42)
    model = LinearRegression()
    # model = RandomForestRegressor()

    model.fit(x_train,y_train)

    #sample = np.array([1, 1, 1, 2, 5, 5, 3, 3, 1, 1, 1,2, 5, 2,2,0,0, 0, 0,0,3,3,3,3,1,0])
    sample = sample[2:]
    sample = np.array(sample)
    data = pd.DataFrame(sample.reshape(-1, len(sample)),columns=x.columns)
    result = model.predict(data)
    res = result[0][0]
    if(res < 0):res = 0
    return res
