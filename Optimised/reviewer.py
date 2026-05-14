

from utils import call_counter, log


class Reviewer:
    def __init__(self, reviewer_data: dict):
        self.id = reviewer_data["id"]
        self.name = reviewer_data["name"]
        self.conflicts = reviewer_data.get("conflicts", [])
        self.workload = reviewer_data.get("workload", 0)
        self.assigned_submission = None
        self.score = None

    def assignReview(self, submission_id: str):
        """Assign this reviewer to a submission."""
        call_counter.increment("Reviewer.assignReview")
        log("Reviewer", f"assignReview() — {self.name} assigned to {submission_id}")
        self.assigned_submission = submission_id

    def submitScore(self, score: float):
        """Record this reviewer's evaluation score."""
        call_counter.increment("Reviewer.submitScore")
        log("Reviewer", f"submitScore(score={score}) — {self.name}")
        self.score = score
