from ml.random_forest_model import RandomForestModel


class PreferenceEngine:

    # Shared model instance (singleton style)
    model = RandomForestModel()

    # -------------------------------
    # TRAIN MODEL
    # -------------------------------
    @staticmethod
    def train_model(feature_data, labels):
        """
        Train the Random Forest model
        """

        # If not enough data, skip training
        if not feature_data or not labels or len(feature_data) < 2:
            return False

        return PreferenceEngine.model.train(feature_data, labels)

    # -------------------------------
    # PREDICT CATEGORY FROM FEATURES
    # -------------------------------
    @staticmethod
    def predict_category(feature_vector):
        """
        Predict user interest category
        """

        if not PreferenceEngine.model.is_ready():
            return None

        return PreferenceEngine.model.predict(feature_vector)

    # -------------------------------
    # GET PROBABILITY SCORES
    # -------------------------------
    @staticmethod
    def get_prediction_scores(feature_vector):
        """
        Returns probability distribution across categories
        """

        if not PreferenceEngine.model.is_ready():
            return {}

        return PreferenceEngine.model.predict_proba(feature_vector)

    # -------------------------------
    # GET USER PREFERENCE SCORES
    # -------------------------------
    @staticmethod
    def get_user_preferences(existing_profile):
        """
        Combines ML predictions + stored interest profile
        """

        # Default categories
        categories = ["history", "nature", "culture", "legends"]

        # Initialize base scores
        scores = {cat: 1.0 for cat in categories}

        # Add stored profile influence
        if existing_profile:
            for cat in categories:
                scores[cat] += existing_profile.get(cat, 0)

        # Normalize scores (avoid very large values)
        total = sum(scores.values())
        if total > 0:
            scores = {k: v / total for k, v in scores.items()}

        return scores

    # -------------------------------
    # HYBRID SCORE (ML + RULE BASED)
    # -------------------------------
    @staticmethod
    def compute_hybrid_score(feature_vector, existing_profile):
        """
        Advanced scoring combining ML prediction + user profile
        """

        categories = ["history", "nature", "culture", "legends"]

        # Base scores
        scores = {cat: 0 for cat in categories}

        # Step 1: Add ML probability scores
        ml_scores = PreferenceEngine.get_prediction_scores(feature_vector)

        for cat in categories:
            scores[cat] += ml_scores.get(cat, 0)

        # Step 2: Add profile scores
        if existing_profile:
            for cat in categories:
                scores[cat] += existing_profile.get(cat, 0)

        return scores

    # -------------------------------
    # DEFAULT FALLBACK (NO DATA)
    # -------------------------------
    @staticmethod
    def get_default_preferences():
        """
        Used when no data exists
        """
        return {
            "history": 1,
            "nature": 1,
            "culture": 1,
            "legends": 1
        }