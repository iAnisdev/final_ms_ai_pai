import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler


class CryptoPredictor:
    def __init__(self):
        self.model = LinearRegression()
        self.scaler = MinMaxScaler()
        self.feature_columns = [
            "open",
            "high",
            "low",
            "close",
            "volume",
            "number_of_trades",
        ]

    def preprocess_data(self, data, duration):
        df = pd.DataFrame(
            data,
            columns=["timestamp"] + self.feature_columns,
        )
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df.set_index("timestamp", inplace=True)

        if duration in [1, 3]:
            df = df.resample("1H").mean()
        else:
            df = df.resample("1D").mean()

        # Drop missing values
        df = df.dropna()

        # Scale features
        features = df[self.feature_columns]
        self.scaler.fit(features)
        scaled_features = pd.DataFrame(
            self.scaler.transform(features),
            columns=self.feature_columns,
            index=features.index,
        )

        # Prepare target
        df["target"] = df["close"].shift(-1)
        target = scaled_features["close"].shift(-1).dropna()

        features = scaled_features.iloc[:-1]

        timestamps = features.index

        return features, target, timestamps

    def train(self, data, duration):
        features, target, _ = self.preprocess_data(data, duration)
        self.model.fit(features, target)

    def predict(self, data, duration):
        # Preprocess the data
        features, _, timestamps = self.preprocess_data(data, duration)

        if duration in [1, 3]:  # Hourly predictions for 1 or 3 days
            steps = 24 * duration
            freq = "1H"
        else:
            steps = duration
            freq = "1D"

        last_features = features.iloc[-1:].copy()

        future_timestamps = pd.date_range(
            start=timestamps[-1] + pd.Timedelta(freq), periods=steps, freq=freq
        )

        predictions = []
        for _ in range(steps):
            last_features = pd.DataFrame(
                last_features.values,
                columns=self.feature_columns,
                index=last_features.index,
            )

            next_prediction = self.model.predict(last_features)[0]

            denorm_prediction = self.denormalize(next_prediction, feature_index=3)
            predictions.append(denorm_prediction)

            next_features = last_features.iloc[0].copy()
            next_features["close"] = next_prediction
            next_features["open"] = next_prediction
            next_features["high"] = max(next_features["open"], next_features["close"])
            next_features["low"] = min(next_features["open"], next_features["close"])

            last_features = pd.DataFrame([next_features], columns=self.feature_columns)

        results = [
            {
                "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
                "value": round(predictions[i], 2),
            }
            for i, ts in enumerate(future_timestamps)
        ]
        return results

    def denormalize(self, value, feature_index):
        min_val = self.scaler.data_min_[feature_index]
        max_val = self.scaler.data_max_[feature_index]
        return value * (max_val - min_val) + min_val


def get_prediction(data, duration):
    model = CryptoPredictor()

    # Remove `id` column and prepare the data
    prepared_data = [(x[1], *map(float, x[2:])) for x in data]

    # Train and predict
    model.train(prepared_data, duration)
    predicted = model.predict(prepared_data, duration)
    expected_change = predicted[-1]["value"] - prepared_data[-1][3]
    expected_change_percent = (expected_change / prepared_data[-1][3]) * 100
    return {
        "expected_price": predicted[-1]["value"],
        "expected_change": expected_change_percent.round(2),
        "predicted": predicted,
    }
