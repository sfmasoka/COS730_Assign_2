
from utils import call_counter, log


class NotificationService:
    def notifyAcceptance(self, submission_id: str, author: str):
        call_counter.increment("NotificationService.notifyAcceptance")
        log("NotificationService", f"notifyAcceptance() — Submission {submission_id} ACCEPTED. Notifying {author}.")
        print(f"\n[{author}] Congratulations! Your submission '{submission_id}' has been ACCEPTED.\n")

    def notifyRejection(self, submission_id: str, author: str):
        call_counter.increment("NotificationService.notifyRejection")
        log("NotificationService", f"notifyRejection() — Submission {submission_id} REJECTED. Notifying {author}.")
        print(f"\n[{author}] We regret to inform you that submission '{submission_id}' has been REJECTED.\n")

    def notifyRevision(self, submission_id: str, author: str):
        call_counter.increment("NotificationService.notifyRevision")
        log("NotificationService", f"notifyRevision() — Submission {submission_id} requires REVISION. Notifying {author}.")
        print(f"\n[{author}] Your submission '{submission_id}' requires REVISION before it can be accepted.\n")
