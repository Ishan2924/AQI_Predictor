# Air Quality Index (AQI) Predictor

This project presents a robust and user-friendly web application for predicting Air Quality Index (AQI) values. It empowers users to visualize historical AQI trends for selected cities and obtain future AQI predictions based on various environmental parameters. The system integrates a data-driven machine learning backend with an beautiful and intuitive Flask-powered frontend, designed for clarity and ease of use.

## Key Features

* **City-Specific Historical AQI Visualization:** Enables users to select a city and instantly view interactive plots showcasing its past AQI trends, providing immediate insights into air quality patterns.

* **Intelligent AQI Prediction Form:** Offers a dynamic input form where users can adjust relevant environmental parameters to predict future AQI. For enhanced usability, these parameters are intelligently pre-filled with the historical average values specific to the chosen city.

* **Powerful Machine Learning Core:** At its heart, the application leverages a highly accurate XGBoost Regressor model, meticulously trained and optimized to deliver reliable AQI predictions.

* **Intuitive Web Interface:** Built with Flask, HTML, and CSS, the frontend provides a clean, responsive, and engaging user experience, making complex data accessible.

* **Efficient Data Management:** Processed AQI data is efficiently managed and queried via an SQLite database (`aqi.db`), ensuring swift access to historical information and city-specific averages.

## Technology Stack

This project is built upon a comprehensive set of modern technologies:

* **Backend:**

    * Python 3.x

    * Flask (Web Framework)

    * SQLite (Lightweight Database)

* **Machine Learning & Data Science:**

    * `xgboost` (Gradient Boosting Framework)

    * `scikit-learn` (Machine Learning Library for preprocessing and evaluation)

    * `pandas` (Data Manipulation and Analysis)

    * `numpy` (Numerical Computing)

    * `pickle` (Model Persistence)

* **Data Processing Workflow:**

    * Jupyter Notebook (for detailed preprocessing, Exploratory Data Analysis, and model training)

    * Microsoft Excel (for initial raw data preprocessing)

* **Frontend:**

    * HTML5 (Structure)

    * CSS3 (Styling)

* **Development Tools:**

    * `pip` (Python Package Installer)

    * `Git` (Version Control System)

    * `GitHub` (Code Hosting and Collaboration)

*(For a comprehensive list of exact dependencies, please refer to `requirements.txt`.)*

## Project Structure

The repository is organized for clarity and maintainability:

```
AQI_Predictor/
├── server.py                        # Main Flask application file; handles routes, API endpoints, and model inference.
├── requirements.txt                 # Lists all Python package dependencies with their exact versions.
├── .gitignore                       # Configures Git to ignore specified files and directories (e.g., virtual environment).
├── model.pkl                        # The trained and serialized XGBoost Regressor model.
├── aqi.db                           # SQLite database file containing the cleaned and processed AQI dataset.
├── output/                          # Contains visual assets such as screenshots illustrating the application's UI.
│   ├── screenshot_1.png
│   └── ... (additional screenshots)
├── model_features.json              # Defines the exact features (columns) the trained model expects for prediction.
├── city_data_aqi_cleaned.csv        # The intermediate cleaned dataset after Jupyter-based preprocessing and EDA.
├── city_data_aqi.xlsx               # The initial preprocessed dataset, a result of Excel-based data preparation.
├── templates/                       # Flask's directory for serving HTML template files.
│   └── index.html                   # The primary HTML template for the application's user interface.
└── static/                          # Flask's directory for serving static web assets.
└── style.css                    # Custom CSS stylesheet for styling the web application.

Note: The 'test.py' script is an auxiliary file used during development for model input/prediction testing and can be disregarded for core deployment.
```
## Getting Started

Follow these steps to set up and run the AQI Predictor locally:

1.  **Clone the Repository:**
    Navigate to your desired directory in the terminal and clone the project:

    ```bash
    git clone [https://github.com/your-username/AQI_Predictor.git](https://github.com/your-username/AQI_Predictor.git) # Remember to replace with your actual repository URL
    cd AQI_Predictor
    ```

2.  **Create and Activate Virtual Environment:**
    It is highly recommended to use a Python virtual environment to isolate project dependencies.

    * **For Windows:**

        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

    * **For macOS / Linux:**

        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install Dependencies:**
    With your virtual environment activated, install all necessary Python packages:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Verify Model and Database Files:**
    Ensure that the `model.pkl` (trained machine learning model) and `aqi.db` (SQLite database) files are present in the project's root directory. These are critical for the application's functionality.

5.  **Run the Flask Application:**
    Launch the web server by executing the `server.py` script:

    ```bash
    python server.py
    ```

    The application will start, typically accessible at `http://127.0.0.1:5000`.

## Usage Guide

1.  **Access the Web Interface:**
    Open your web browser and navigate to the local server address (e.g., `http://127.0.0.1:5000`).

2.  **Select Your City:**
    From the provided dropdown or input field, choose the city for which you wish to analyze AQI.

3.  **Explore Historical Data:**
    The application will automatically fetch and display a visual graph of historical AQI trends for your selected city, offering a quick overview of past air quality.

4.  **Input Prediction Parameters:**
    You will then be presented with an intuitive form containing various environmental parameters. These fields are intelligently pre-populated with the average values for your selected city's historical data, providing a convenient starting point. You can adjust these values as needed for your prediction.

5.  **Obtain AQI Prediction:**
    Click the "Predict AQI" (or similarly labeled) button. The machine learning model will process your inputs, and the predicted AQI value will be prominently displayed on the page.

## Challenges & Key Learnings

Developing this AQI Predictor involved navigating several common yet insightful challenges in data science and web development:

* **Multi-Stage Data Preprocessing:** The project necessitated a meticulous, multi-stage data preprocessing approach. This included initial cleaning in Excel, followed by extensive null value imputation, feature engineering, and Exploratory Data Analysis (EDA) within Jupyter Notebooks, underscoring the complexities of preparing real-world datasets.

* **Strategic Model Selection and Optimization:** A comparative analysis of various regression models (Linear Regression, Decision Trees, Random Forest) led to the selection and optimization of XGBoost, which demonstrated superior performance for AQI prediction due to its robust handling of complex relationships within the data.

* **Seamless Flask Integration:** A core challenge involved integrating the machine learning backend with the Flask web server. This encompassed serving static assets and dynamic HTML templates, efficiently loading and utilizing the trained `model.pkl`, and executing database queries against `aqi.db` based on real-time user interactions.

* **Dynamic Frontend Visualization:** Implementing dynamic data fetching from the SQLite database to generate and display city-specific historical AQI plots directly on the web interface, enhancing user engagement and data interpretation.

* **Enhanced User Experience through Pre-filling:** Developing the logic to pre-populate prediction input fields with historical average values specific to the chosen city significantly improved the user experience by providing relevant defaults and reducing manual effort.

## Future Enhancements

The project offers ample opportunities for further development and refinement:

* **Real-time Data Integration:** Implement connections to external Air Quality APIs to fetch and incorporate live AQI data for more current and dynamic predictions.

* **Advanced Interactive Visualizations:** Upgrade historical data plots using more sophisticated JavaScript libraries (e.g., Plotly.js, D3.js) to offer interactive elements like zooming, hovering for details, and custom ranges.

* **User Authentication and Personalization:** Introduce user login functionalities, allowing for personalized dashboards, saving favorite cities, tracking individual prediction histories, and setting custom alerts.

* **Cloud Deployment:** Migrate the Flask application to a cloud platform (e.g., Google Cloud Run, AWS Elastic Beanstacks, Heroku) for greater accessibility, scalability, and robust hosting.

* **Automated Model Monitoring and Retraining:** Develop a system to continuously monitor the model's performance in production and trigger automated retraining pipelines when performance degrades or new data becomes available.

* **Comprehensive Frontend Error Handling:** Implement more granular and user-friendly error messages and feedback mechanisms on the frontend for invalid inputs or prediction failures.

* **Dockerization:** Containerize the application using Docker for easier deployment and environment consistency.

# Outputs

![img](https://github.com/user-attachments/assets/7866580c-3b7a-4416-9d08-e80d1358e840)

![img_1](https://github.com/user-attachments/assets/14fa2861-465c-464f-8446-c59d31295e2e)

![img_2](https://github.com/user-attachments/assets/16a1be71-f701-4df3-b2cc-9d4cfcc94019)

![img_3](https://github.com/user-attachments/assets/7502391e-bdcf-4767-ac4c-a228864f97ff)





