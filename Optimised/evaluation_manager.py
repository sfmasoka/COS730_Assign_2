

from utils import call_counter, log
from notification_service import NotificationService
from decision_table import determine_outcome, CONSENSUS_MARGIN


class EvaluationManager:
    def __init__(self, database):
        self._database = database
        self._notification_service = NotificationService()
        self._scores = []

    def startEvaluation(self, submission_id: str, author: str, assigned_reviewers: list):
       
        call_counter.increment("EvaluationManager.startEvaluation")
        log("EvaluationManager", f"startEvaluation() — submission: {submission_id}")

        self._scores = []
        score_map = {}   # collected for batch save

        # Loop: each reviewer submits their score (same as Original)
        for reviewer in assigned_reviewers:
            reviewer.submitScore(reviewer.score)
            self._scores.append(reviewer.score)
            score_map[reviewer.id] = reviewer.score

        # One batch save instead of N individual saves
        self._database.saveScoresBatch(score_map)

        # Evaluate using the decision table
        outcome = self._evaluate()

        # One notification call — NotificationService handles the message
        self._notification_service.notify(outcome, submission_id, author)

    def _evaluate(self) -> str:
    
        if not self._scores:
            return "revision"

        average = sum(self._scores) / len(self._scores)
        log("EvaluationManager", f"Average score: {average:.2f}")

        if len(self._scores) >= 2:
            spread = max(self._scores) - min(self._scores)
            consensus = spread <= CONSENSUS_MARGIN
            log("EvaluationManager", f"Score spread: {spread:.2f} — Consensus: {consensus}")
        else:
            consensus = True

        outcome = determine_outcome(average, consensus)
        log("EvaluationManager", f"Outcome: {outcome.upper()}")
        return outcome
