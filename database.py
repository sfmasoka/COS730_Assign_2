from utils import call_counter, log


# Simulated in-memory reviewer store
_REVIEWER_STORE = [
    {"id": "R1", "name": "Dr. Alice Mokoena",  "conflicts": [],       "workload": 2},
    {"id": "R2", "name": "Prof. Brian Nkosi",   "conflicts": ["S001"], "workload": 5},
    {"id": "R3", "name": "Dr. Carol Dlamini",   "conflicts": [],       "workload": 1},
    {"id": "R4", "name": "Dr. David Sithole",   "conflicts": [],       "workload": 4},
]


class Database:
    def __init__(self):
        self._submissions = {}
        self._scores = []

    def saveSubmission(self, data: dict) -> str:
        """Persist submission and return a confirmation ID."""
        call_counter.increment("Database.saveSubmission")
        log("Database", "saveSubmission(data)")

        submission_id = f"S{len(self._submissions) + 1:03d}"
        self._submissions[submission_id] = data
        log("Database", f"Saved submission with ID: {submission_id}")
        return submission_id

    def fetchReviewers(self) -> list:
        """Return the full list of available reviewers."""
        call_counter.increment("Database.fetchReviewers")
        log("Database", "fetchReviewers()")
        log("Database", f"Returning {len(_REVIEWER_STORE)} reviewers")
        return list(_REVIEWER_STORE)  # return a copy

    def saveScore(self, reviewer_id: str, score: float) -> bool:
        """Persist a reviewer's score."""
        call_counter.increment("Database.saveScore")
        log("Database", f"saveScore(score={score}) from reviewer {reviewer_id}")
        self._scores.append({"reviewer_id": reviewer_id, "score": score})
        return True
