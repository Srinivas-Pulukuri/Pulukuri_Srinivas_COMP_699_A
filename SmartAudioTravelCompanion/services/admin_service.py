from database.models.audio_story import AudioStory
from database.models.usage_report import UsageReport

from services.audio_service import AudioService


class AdminService:

    # -------------------------------
    # UPLOAD AUDIO STORY
    # -------------------------------
    @staticmethod
    def upload_story(title, category, duration, file):
        """
        Upload audio file and create story record
        """

        # Save file using AudioService
        file_path = AudioService.save_audio_file(file)

        if not file_path:
            return {"success": False, "message": "Invalid or failed file upload"}

        # Create story in DB
        AudioStory.create_story(title, category, duration, file_path)

        return {"success": True, "message": "Story uploaded successfully"}

    # -------------------------------
    # GET ALL STORIES
    # -------------------------------
    @staticmethod
    def get_all_stories():
        stories = AudioStory.get_all_stories()
        return [story.to_dict() for story in stories]

    # -------------------------------
    # UPDATE STORY
    # -------------------------------
    @staticmethod
    def update_story(story_id, title, category, duration):
        AudioStory.update_story(story_id, title, category, duration)

        return {"success": True, "message": "Story updated successfully"}

    # -------------------------------
    # DELETE STORY
    # -------------------------------
    @staticmethod
    def delete_story(story_id):
        AudioStory.delete_story(story_id)

        # Also delete report data (optional cleanup)
        UsageReport.delete_report(story_id)

        return {"success": True, "message": "Story deleted successfully"}

    # -------------------------------
    # UPDATE STORY FILE (RE-UPLOAD)
    # -------------------------------
    @staticmethod
    def update_story_file(story_id, file):
        file_path = AudioService.save_audio_file(file)

        if not file_path:
            return {"success": False, "message": "Invalid file"}

        AudioStory.update_file_path(story_id, file_path)

        return {"success": True, "message": "Audio file updated"}

    # -------------------------------
    # GET STORY REPORT
    # -------------------------------
    @staticmethod
    def get_story_report(story_id):
        report = UsageReport.get_by_story(story_id)

        if not report:
            return None

        return report.to_dict()

    # -------------------------------
    # GET ALL REPORTS
    # -------------------------------
    @staticmethod
    def get_all_reports():
        reports = UsageReport.get_all_reports()
        return [report.to_dict() for report in reports]

    # -------------------------------
    # RESET STORY REPORT
    # -------------------------------
    @staticmethod
    def reset_report(story_id):
        UsageReport.reset_report(story_id)

        return {"success": True, "message": "Report reset successfully"}

    # -------------------------------
    # SYSTEM HEALTH CHECK (SIMPLE)
    # -------------------------------
    @staticmethod
    def system_health():
        """
        Basic system check for demo
        """
        try:
            stories = AudioStory.get_all_stories()
            reports = UsageReport.get_all_reports()

            return {
                "status": "OK",
                "total_stories": len(stories),
                "total_reports": len(reports)
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "message": str(e)
            }