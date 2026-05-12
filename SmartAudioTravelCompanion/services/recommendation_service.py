from database.models.audio_story import AudioStory
from database.models.listening_history import ListeningHistory
from database.models.traveller import Traveller

from ml.preference_engine import PreferenceEngine


class RecommendationService:

    # -------------------------------
    # GET PERSONALIZED RECOMMENDATIONS
    # -------------------------------
    @staticmethod
    def get_recommendations(user_id):
        """
        Returns ranked stories based on user preference
        """

        # Step 1: Get all stories
        stories = AudioStory.get_all_stories()

        if not stories:
            return []

        # Step 2: Get user history
        history_records = ListeningHistory.get_user_history(user_id)

        # Step 3: Get traveller profile
        traveller = Traveller.get_by_user_id(user_id)

        # Step 4: Prepare ML input data
        feature_data = []
        story_labels = []

        for record in history_records:
            feature_data.append(record.to_feature_vector())

            # Get story category as label
            story = AudioStory.get_by_id(record.story_id)
            if story:
                story_labels.append(story.category)

        # Step 5: Train / Update model
        PreferenceEngine.train_model(feature_data, story_labels)

        # Step 6: Get updated preference scores
        if traveller:
            preference_scores = PreferenceEngine.get_user_preferences(
                traveller.get_interest_dict()
            )
        else:
            # fallback default
            preference_scores = {
                "history": 1,
                "nature": 1,
                "culture": 1,
                "legends": 1
            }

        # Step 7: Rank stories based on category score
        ranked_stories = sorted(
            stories,
            key=lambda s: preference_scores.get(s.category, 0),
            reverse=True
        )

        return [story.to_dict() for story in ranked_stories]

    # -------------------------------
    # GET NEXT BEST STORY
    # -------------------------------
    @staticmethod
    def get_next_story(user_id):
        recommendations = RecommendationService.get_recommendations(user_id)

        if recommendations:
            return recommendations[0]

        return None

    # -------------------------------
    # GET STORIES BY USER INTEREST
    # -------------------------------
    @staticmethod
    def get_stories_by_interest(user_id, category):
        """
        Filter stories by selected category
        """
        stories = AudioStory.get_by_category(category)
        return [story.to_dict() for story in stories]

    # -------------------------------
    # UPDATE USER PREFERENCE PROFILE
    # -------------------------------
    @staticmethod
    def update_user_preferences(user_id):
        """
        Updates traveller interest profile based on listening history
        """

        history_records = ListeningHistory.get_user_history(user_id)

        # Initialize scores
        scores = {
            "history": 0,
            "nature": 0,
            "culture": 0,
            "legends": 0
        }

        # Aggregate behavior
        for record in history_records:
            story = AudioStory.get_by_id(record.story_id)
            if not story:
                continue

            category = story.category

            # Basic scoring logic
            score = (
                record.listening_time * 0.5 +
                record.replay_count * 2 -
                record.skip_count * 1 +
                record.completion_status * 3
            )

            if category in scores:
                scores[category] += score

        # Convert to string format
        profile_string = Traveller.dict_to_profile_string(scores)

        # Save to DB
        Traveller.update_interest_profile(user_id, profile_string)

        return scores

    # -------------------------------
    # GET USER PREFERENCE PROFILE
    # -------------------------------
    @staticmethod
    def get_user_preferences(user_id):
        traveller = Traveller.get_by_user_id(user_id)

        if not traveller:
            return {}

        return traveller.get_interest_dict()