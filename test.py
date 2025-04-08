import requests

url = "http://127.0.0.1:5000/predict"

input_data = {
     "PM2.5":33,
     "PM10": 110,
     "NO2": 10,
     "NOx": 10,
     "NH3":101,
     "CO":92,
     "SO2":22,
     "O3":33,
     "Toluene":12
}

try:
     print("sending request with data", input_data)
     response = requests.post(url, json = input_data)

     print("Raw respone", response.text)

     if response.text:
          print("response json", response.json())
     else:
          print("Expty respone receive")

except requests.exceptions.RequestException as e:
     print("request failed", str(e))
except json.JSONDecodeError as e:
    print("Failed to decode JSON:", str(e))
    print("Response content:", response.text)
except Exception as e:
    print("An unexpected error occurred:", str(e))