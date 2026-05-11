from utils import call_counter, log

MAX_WORKLOAD = 4  # Reviewers with workload >= this are considered overloaded


class Reviewer:
    def __init__(self, reviewer_data: dict):
        self.id = reviewer_data["id"]
        self.name = reviewer_data["name"]
        self.conflicts = reviewer_data["conflicts"]
        self.workload = reviewer_data["workload"]
        self.assigned_submission = None
        self.score = None

    def filterConflicts(self, reviewer_list: list, submission_id: str) -> list:
        """
        Remove reviewers who have a conflict with the given submission.
        NOTE (baseline): called on a single Reviewer instance but filters the
        whole list — a responsibility issue we will flag in Task 2.
        """
        call_counter.increment("Reviewer.filterConflicts")
        log("Reviewer", f"filterConflicts(reviewerList) — checking conflicts for submission {submission_id}")

        filtered = [r for r in reviewer_list if submission_id not in r.conflicts]
        log("Reviewer", f"After conflict filter: {len(filtered)} of {len(reviewer_list)} reviewers remain")
        return filtered

    def checkWorkload(self, reviewer_list: list) -> list:
        """
        Remove reviewers whose workload exceeds the threshold.
        NOTE (baseline): same responsibility issue as filterConflicts.
        """
        call_counter.increment("Reviewer.checkWorkload")
        log("Reviewer", f"checkWorkload(reviewerList) — threshold is {MAX_WORKLOAD}")

        filtered = [r for r in reviewer_list if r.workload < MAX_WORKLOAD]
        log("Reviewer", f"After workload filter: {len(filtered)} of {len(reviewer_list)} reviewers remain")
        return filtered

    def assignReview(self, submission_id: str):
        """Assign this reviewer to a submission."""
        call_counter.increment("Reviewer.assignReview")
        log("Reviewer", f"assignReview() — {self.name} assigned to submission {submission_id}")
        self.assigned_submission = submission_id

    def submitScore(self, score: float):
        """Record this reviewer's evaluation score."""
        call_counter.increment("Reviewer.submitScore")
        log("Reviewer", f"submitScore(score={score}) — {self.name} submits score")
        self.score = score
