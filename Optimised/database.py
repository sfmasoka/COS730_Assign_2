
from utils import call_counter, log


class Database:
    def __init__(self):
        self._submissions = {}
        self._scores = {}

    def saveSubmission(self, data: dict) -> str:
        """Persist submission and return a confirmation ID."""
        call_counter.increment("Database.saveSubmission")
        log("Database", "saveSubmission(data)")

        submission_id = f"S{len(self._submissions) + 1:03d}"
        self._submissions[submission_id] = data
        log("Database", f"Saved submission with ID: {submission_id}")
        return submission_id

    def saveScoresBatch(self, scores: dict) -> bool:
        """
        Save all reviewer scores in a single call.
        Optimisation: replaces the per-reviewer saveScore() loop from the Original.
        Original made N separate calls to Database; now it is one.
        scores = {reviewer_id: score, ...}
        """
        call_counter.increment("Database.saveScoresBatch")
        log("Database", f"saveScoresBatch() — saving {len(scores)} score(s) in one call")
        self._scores.update(scores)
        return True
