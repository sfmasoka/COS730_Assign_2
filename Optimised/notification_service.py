
from utils import call_counter, log

# Messages table — keeps the message content out of the method logic
_MESSAGES = {
    "accepted": "Congratulations! Your submission has been ACCEPTED.",
    "rejected":  "We regret to inform you that your submission has been REJECTED.",
    "revision":  "Your submission requires REVISION before it can be accepted.",
}


class NotificationService:
    def notify(self, outcome: str, submission_id: str, author: str):
        """
        Single notification entry point.
        Replaces three separate notifyX() methods from the Original.
        """
        call_counter.increment("NotificationService.notify")
        log("NotificationService", f"notify(outcome={outcome}) — {submission_id} -> {author}")

        message = _MESSAGES.get(outcome, "Your submission status has been updated.")
        print(f"\n  [{author}] {message} (Submission: {submission_id})\n")
