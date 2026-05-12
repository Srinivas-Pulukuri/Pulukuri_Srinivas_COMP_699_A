from sklearn.ensemble import RandomForestClassifier
import numpy as np


class RandomForestModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.is_trained = False

    # -------------------------------
    # TRAIN MODEL
    # -------------------------------
    def train(self, X, y):
        """
        X = list of feature vectors
        y = list of labels (categories)
        """

        if not X or not y or len(X) != len(y):
            return False

        try:
            X_array = np.array(X)
            y_array = np.array(y)

            self.model.fit(X_array, y_array)
            self.is_trained = True

            return True

        except Exception as e:
            print("Model training error:", e)
            return False

    # -------------------------------
    # PREDICT CATEGORY
    # -------------------------------
    def predict(self, feature_vector):
        """
        Predict category for a single input
        """

        if not self.is_trained:
            return None

        try:
            prediction = self.model.predict([feature_vector])
            return prediction[0]

        except Exception as e:
            print("Prediction error:", e)
            return None

    # -------------------------------
    # PREDICT PROBABILITIES
    # -------------------------------
    def predict_proba(self, feature_vector):
        """
        Returns probability for each class
        """

        if not self.is_trained:
            return {}

        try:
            probs = self.model.predict_proba([feature_vector])[0]
            classes = self.model.classes_

            return dict(zip(classes, probs))

        except Exception as e:
            print("Probability prediction error:", e)
            return {}

    # -------------------------------
    # CHECK IF MODEL IS TRAINED
    # -------------------------------
    def is_ready(self):
        return self.is_trained