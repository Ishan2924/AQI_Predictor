This is An AQI preditor project
I have taken data from Kaggle , firtly the original dataset (city_data) is preprocessed with excel itself and saved as city_data_aqi
Then this dataset is loaded in Jupyter and detailed preprocessing is done to it, like null value handling, feature extraction and EDA
Then this file is saved as City_data_aqi_cleaned

After doing the preprocessing, model is trained using
1. Linear Regression
2. Decison Trees
3. Random Forest
4. XGBoost

I got the best result from XGBoost so i imported it as .pkl model

After doing model training, i have created a flask server (server.py) to host and created front end for it
The template folder has base file(index.html), and the static file has stylesheet file (style.css)

Flask has several routes
1. Taking input city from user
2. Fetching the past AQI for that city (using sql) and plot a graph for same
3. Asking the user to enter all the required parameters, to predict the AQI , (it will already be filled with average values of that city using sql)
4. Feeding the values to the model and the prediction will be displayed

The repo contains an output folder that contains screenshot of how the prohect will look
it also contains a json file that has the columns/features used by model to make predictions

#ignore test.py it was created to test whether the model was taking inputs and able to predict or not


