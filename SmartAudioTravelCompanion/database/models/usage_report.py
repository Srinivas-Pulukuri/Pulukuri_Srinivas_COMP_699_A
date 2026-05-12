from database.db import execute_query


class UsageReport:
    def __init__(self, report_id=None, story_id=None, play_count=0, engagement_rate=0.0):
        self.report_id = report_id
        self.story_id = story_id
        self.play_count = play_count
        self.engagement_rate = engagement_rate

    # -------------------------------
    # CREATE OR GET REPORT
    # -------------------------------
    @staticmethod
    def get_or_create(story_id):
        query = """
            SELECT * FROM usage_report WHERE story_id = ?
        """
        row = execute_query(query, (story_id,), fetch_one=True)

        if row:
            return UsageReport(
                report_id=row["report_id"],
                story_id=row["story_id"],
                play_count=row["play_count"],
                engagement_rate=row["engagement_rate"]
            )

        # Create new report if not exists
        insert_query = """
            INSERT INTO usage_report (story_id, play_count, engagement_rate)
            VALUES (?, 0, 0.0)
        """
        execute_query(insert_query, (story_id,), commit=True)

        return UsageReport.get_or_create(story_id)

    # -------------------------------
    # INCREMENT PLAY COUNT
    # -------------------------------
    @staticmethod
    def increment_play_count(story_id):
        query = """
            UPDATE usage_report
            SET play_count = play_count + 1
            WHERE story_id = ?
        """
        execute_query(query, (story_id,), commit=True)

    # -------------------------------
    # UPDATE ENGAGEMENT RATE
    # -------------------------------
    @staticmethod
    def update_engagement_rate(story_id):
        """
        Engagement = completed / total plays
        """
        # Get total plays
        report = UsageReport.get_or_create(story_id)
        total_plays = report.play_count

        if total_plays == 0:
            return

        # Get completed count from listening_history
        query = """
            SELECT COUNT(*) as completed_count
            FROM listening_history
            WHERE story_id = ? AND completion_status = 1
        """
        row = execute_query(query, (story_id,), fetch_one=True)
        completed = row["completed_count"] if row else 0

        engagement = completed / total_plays

        update_query = """
            UPDATE usage_report
            SET engagement_rate = ?
            WHERE story_id = ?
        """
        execute_query(update_query, (engagement, story_id), commit=True)

    # -------------------------------
    # GET REPORT BY STORY
    # -------------------------------
    @staticmethod
    def get_by_story(story_id):
        query = """
            SELECT * FROM usage_report WHERE story_id = ?
        """
        row = execute_query(query, (story_id,), fetch_one=True)

        if row:
            return UsageReport(
                report_id=row["report_id"],
                story_id=row["story_id"],
                play_count=row["play_count"],
                engagement_rate=row["engagement_rate"]
            )
        return None

    # -------------------------------
    # GET ALL REPORTS (ADMIN)
    # -------------------------------
    @staticmethod
    def get_all_reports():
        query = "SELECT * FROM usage_report"
        rows = execute_query(query, fetch_all=True)

        reports = []
        for row in rows:
            reports.append(UsageReport(
                report_id=row["report_id"],
                story_id=row["story_id"],
                play_count=row["play_count"],
                engagement_rate=row["engagement_rate"]
            ))
        return reports

    # -------------------------------
    # RESET REPORT DATA
    # -------------------------------
    @staticmethod
    def reset_report(story_id):
        query = """
            UPDATE usage_report
            SET play_count = 0, engagement_rate = 0.0
            WHERE story_id = ?
        """
        execute_query(query, (story_id,), commit=True)

    # -------------------------------
    # DELETE REPORT
    # -------------------------------
    @staticmethod
    def delete_report(story_id):
        query = """
            DELETE FROM usage_report WHERE story_id = ?
        """
        execute_query(query, (story_id,), commit=True)

    # -------------------------------
    # CONVERT OBJECT TO DICT
    # -------------------------------
    def to_dict(self):
        return {
            "report_id": self.report_id,
            "story_id": self.story_id,
            "play_count": self.play_count,
            "engagement_rate": self.engagement_rate
        }