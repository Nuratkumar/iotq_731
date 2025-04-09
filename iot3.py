import time
import random
import json
from datetime import datetime
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import requests


class SoilMoistureSensor:
    def read_moisture(self):
        return random.uniform(20, 80)

    def read_temperature(self):
        return random.uniform(10, 35)


class IrrigationPredictor:
    def _init_(self):
        self.model = None
        self.load_or_train_model()

    def load_or_train_model(self):
        try:
            self.model = joblib.load('irrigation_model.pkl')
            print("Loaded pre-trained model")
        except FileNotFoundError:
            self.train_model()

    def train_model(self):
        data = {
            'moisture': [random.uniform(20, 80) for _ in range(1000)],
            'temperature': [random.uniform(10, 35) for _ in range(1000)],
            'hour_of_day': [random.randint(0, 23) for _ in range(1000)],
            'needs_irrigation': [random.randint(0, 1) for _ in range(1000)]
        }

        df = pd.DataFrame(data)

        X = df[['moisture', 'temperature', 'hour_of_day']]
        y = df['needs_irrigation']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        self.model = RandomForestClassifier(n_estimators=100)
        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model trained with accuracy: {accuracy:.2f}")

        joblib.dump(self.model, 'irrigation_model.pkl')

    def predict_irrigation(self, moisture, temperature):
        current_hour = datetime.now().hour

        prediction = self.model.predict([[moisture, temperature, current_hour]])
        return prediction[0]


class CloudNotifier:
    def _init_(self):
        self.api_url = "https://api.exampleiot.com/notifications"
        self.api_key = "aditya_123#@1"

    def send_notification(self, message):
        payload = {
            "message": message,
            "recipient": "farmer_mobile_app",
            "timestamp": datetime.now().isoformat()
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        try:
            response = requests.post(
                self.api_url,
                data=json.dumps(payload),
                headers=headers
            )

            if response.status_code == 200:
                print("Notification sent successfully")
            else:
                print(f"Failed to send notification. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error sending notification: {str(e)}")


class SmartAgricultureSystem:
    def _init_(self):
        self.sensor = SoilMoistureSensor()
        self.predictor = IrrigationPredictor()
        self.notifier = CloudNotifier()
        self.reading_interval = 3600

    def run(self):
        print("Smart Agriculture System Started")
        while True:
            moisture = self.sensor.read_moisture()
            temperature = self.sensor.read_temperature()

            print(f"\nCurrent Readings - Moisture: {moisture:.1f}%, Temperature: {temperature:.1f}°C")

            needs_irrigation = self.predictor.predict_irrigation(moisture, temperature)

            if needs_irrigation:
                message = f"Irrigation Alert! Soil moisture is low ({moisture:.1f}%). Temperature: {temperature:.1f}°C"
                print(message)
                self.notifier.send_notification(message)
            else:
                print("No irrigation needed at this time")

            time.sleep(self.reading_interval)


if _name_ == "_main_":
    system = SmartAgricultureSystem()
    system.run()