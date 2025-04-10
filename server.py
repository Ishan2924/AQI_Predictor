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
    if not os.path.exists('dataset/city_data_aqi_cleaned.csv'):
        raise FileNotFoundError("CSV file not found")

    df = pd.read_csv('dataset/city_data_aqi_cleaned.csv')
    df = df.rename(columns={
        'PM2.5': 'PM2_5',
        'City': 'city',
        'Date': 'date'
    })

    conn = get_db()
    df.to_sql('city_data_aqi_cleaned', conn, if_exists='replace', index=False)
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
    cities = pd.read_sql("SELECT DISTINCT city FROM city_data_aqi_cleaned", conn)['city'].tolist()
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
        SELECT date, AQI 
        FROM city_data_aqi_cleaned 
        WHERE city = "{city}"
        AND (strftime('%Y', date) = '2020' 
                 OR date LIKE '%2020%'
                 OR substr(date, 1, 4) = '2020')
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
            FROM city_data_aqi_cleaned 
            WHERE city = "{city}"
        ''', conn).iloc[0].to_dict()

    conn.close()

    # Create plot
    fig = px.line(df, x='date', y='AQI',
                  title=f'AQI Levels for {city}',
                  labels={'AQI': 'AQI Value', 'date': 'Date'},
                  line_shape='hv',
                  template='plotly_white')

    aqi_bands = [
        (0, 50, 'Good', '#4CAF50'),  # Soft green
        (51, 100, 'Moderate', '#FFEB3B'),  # Pale yellow
        (101, 150, 'Sensitive', '#FF9800'),  # Muted orange
        (151, 200, 'Unhealthy', '#F44336'),  # Soft red
        (201, 300, 'Very Unhealthy', '#9C27B0'),  # Light purple
        (301, 500, 'Hazardous', '#795548')  # Muted brown
    ]

    for y0, y1, label, color in aqi_bands:
        fig.add_hrect(y0=y0, y1=y1,
                      fillcolor=color,
                      opacity=0.15,
                      line_width=0,
                      annotation_text=f'<b>{label}</b>',
                      annotation_font_size=10,
                      annotation_font_color="#333333",
                      annotation_bgcolor="rgba(255,255,255,0.7)",
                      annotation_position="top left")

    fig.update_traces(
        line=dict(color='#2196F3', width=2.5),  # Nice blue line
        mode='lines+markers',
        marker=dict(size=6, color='#2196F3')
    )

    fig.update_layout(
        font_family="Arial, sans-serif",
        plot_bgcolor='rgba(255,255,255,0.9)',
        paper_bgcolor='rgba(255,255,255,0.9)',
        title_font_size=18,
        title_x=0.5,
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            linecolor='rgba(0,0,0,0.1)'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            linecolor='rgba(0,0,0,0.1)'
        )
    )

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
        rounded_pred = round(prediction, 2)

        if rounded_pred <= 50:
            category = "Good"
            description = "Air quality is satisfactory"
        elif rounded_pred <= 100:
            category = "Moderate"
            description = "Acceptable quality"
        elif rounded_pred <= 150:
            category = "Unhealthy for Sensitive Groups"
            description = "Sensitive people may experience effects"
        elif rounded_pred <= 200:
            category = "Unhealthy"
            description = "Everyone may begin to experience effects"
        elif rounded_pred <= 300:
            category = "Very Unhealthy"
            description = "Health alert: serious effects possible"
        else:
            category = "Hazardous"
            description = "Health warning of emergency conditions"

        return jsonify({
            'predicted_aqi': rounded_pred,
            'aqi_category': category,
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5000)