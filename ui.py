from utils import call_counter, log
from submission_controller import SubmissionController


class UI:
    def __init__(self):
        self._controller = SubmissionController()

    def submitResearchOutput(self, data: dict):
        """Entry point called by the Researcher."""
        call_counter.increment("UI.submitResearchOutput")
        log("UI", "submitResearchOutput(data) — received from Researcher")

        result = self._controller.submit(data)

        self.sendNotification(result)
        return result

    def sendNotification(self, result: dict):
        """Display the final outcome back to the Researcher."""
        call_counter.increment("UI.sendNotification")
        log("UI", "sendNotification() — displaying result to Researcher")

        if result["status"] == "error":
            print(f"\n[UI → Researcher] Error: {result['message']}\n")
        else:
            print(f"\n[UI → Researcher] Submission '{result['submission_id']}' processed successfully.\n")
