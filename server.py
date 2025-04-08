from flask import Flask, render_template, request, jsonify, redirect
import pickle
import json
import numpy as np
import pandas as pd
import sqlite3
import os
import plotly
import plotly.express as px
from json import JSONEncoder

class NumpyEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)

app = Flask(__name__)


# Database Setup
def get_db():
    conn = sqlite3.connect('aqi.db')
    return conn

def init_db():
    if not os.path.exists('dataset/city_data_aqi.csv'):
        raise FileNotFoundError("CSV file not found")

    df = pd.read_csv('dataset/city_data_aqi.csv')
    df = df.rename(columns={
        'PM2.5': 'PM2_5',
        'City': 'city',
        'Date': 'date'
    })

    conn = get_db()
    df.to_sql('city_data_aqi', conn, if_exists='replace', index=False)
    conn.close()


if not os.path.exists('aqi.db'):
    init_db()

# Load Model
try:
    model = pickle.load(open("xgb_model.pkl", "rb"))
    model_columns = json.load(open("model_columns.json"))
except Exception as e:
    print(f"Model loading error: {e}")
    model = None


@app.route('/')
def home():
    conn = get_db()
    cities = pd.read_sql("SELECT DISTINCT city FROM city_data_aqi", conn)['city'].tolist()
    conn.close()
    return render_template('index.html', cities=cities)


@app.route('/city', methods=['GET'])
def city_data():
    city = request.args.get('city')
    if not city:
        return redirect('/')

    conn = get_db()

    # Get city data
    df = pd.read_sql(f'''
        SELECT date, PM2_5, PM10, AQI 
        FROM city_data_aqi 
        WHERE city = "{city}"
        ORDER BY date
    ''', conn)

    # Get averages
    avg = pd.read_sql(f'''
            SELECT 
                AVG(PM2_5) as PM2_5,
                AVG(PM10) as PM10,
                AVG(NO2) as NO2,
                AVG(NOx) as NOx,
                AVG(NH3) as NH3,
                AVG(CO) as CO,
                AVG(SO2) as SO2,
                AVG(O3) as O3,
                AVG(Toluene) as Toluene
            FROM city_data_aqi 
            WHERE city = "{city}"
        ''', conn).iloc[0].to_dict()

    conn.close()

    # Create plot
    fig = px.line(df, x='date', y=['PM2_5', 'PM10'], title=f'AQI for {city}')
    graph_html = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')

    return render_template(
        'index.html',
        cities=[city],
        selected_city=city,
        graph_html=graph_html,
        averages=avg
    )


@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model not loaded'}), 500

    try:
        data = request.get_json()
        input_data = [data[col] for col in model_columns]
        prediction = float(model.predict([input_data])[0])
        return jsonify({'predicted_aqi': round(prediction, 2)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5000)