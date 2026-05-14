
from utils import call_counter, log
from notification_service import NotificationService

# Thresholds for decision logic (will be replaced with Decision Table in Task 3)
ACCEPT_THRESHOLD  = 7.0   # average >= this → accepted
REJECT_THRESHOLD  = 4.0   # average <  this → rejected
                           # between the two  → revision
CONSENSUS_MARGIN  = 2.0   # max allowed spread between scores for consensus


class EvaluationManager:
    def __init__(self, database):
        self._database = database
        self._notification_service = NotificationService()
        self._scores = []
        self._submission_id = None
        self._author = None

    def startEvaluation(self, submission_id: str, author: str, assigned_reviewers: list):
        """
        Kick off the evaluation loop.
        Per the diagram, for each reviewer:
          1. Reviewer.submitScore(score)  [simulated here]
          2. Database.saveScore(score)
        Then:
          3. calculateAverage()
          4. checkConsensus()
          5. applyRules()  → triggers the alt (accepted / rejected / revision)
        """
        call_counter.increment("EvaluationManager.startEvaluation")
        log("EvaluationManager", f"startEvaluation() — submission: {submission_id}")

        self._submission_id = submission_id
        self._author = author
        self._scores = []

        # --- loop: each reviewer ---
        for reviewer in assigned_reviewers:
            # Reviewer submits their score
            reviewer.submitScore(reviewer.score)                          # Reviewer -> EvaluationManager (simulated)
            self._scores.append(reviewer.score)

            # EvaluationManager saves score to Database
            self._database.saveScore(reviewer.id, reviewer.score)

        # After all scores collected
        average = self.calculateAverage()
        consensus = self.checkConsensus()
        outcome = self.applyRules(average, consensus)

        # alt: outcome branch
        self._dispatchNotification(outcome)

    def submitScore(self, reviewer_id: str, score: float):
        """Called by a Reviewer to hand in their score."""
        call_counter.increment("EvaluationManager.submitScore")
        log("EvaluationManager", f"submitScore(score={score}) received from {reviewer_id}")
        # Score is stored via startEvaluation loop; this method exists
        # to preserve the diagram interaction explicitly.

    def calculateAverage(self) -> float:
        call_counter.increment("EvaluationManager.calculateAverage")
        log("EvaluationManager", "calculateAverage()")
        if not self._scores:
            return 0.0
        avg = sum(self._scores) / len(self._scores)
        log("EvaluationManager", f"Average score: {avg:.2f}")
        return avg

    def checkConsensus(self) -> bool:
        call_counter.increment("EvaluationManager.checkConsensus")
        log("EvaluationManager", "checkConsensus()")
        if len(self._scores) < 2:
            log("EvaluationManager", "Only one score — consensus assumed")
            return True
        spread = max(self._scores) - min(self._scores)
        consensus = spread <= CONSENSUS_MARGIN
        log("EvaluationManager", f"Score spread: {spread:.2f} — Consensus: {consensus}")
        return consensus

    def applyRules(self, average: float, consensus: bool) -> str:
        """
        Scattered conditional logic (intentionally suboptimal — Task 2 will flag this).
        Returns: 'accepted', 'rejected', or 'revision'
        """
        call_counter.increment("EvaluationManager.applyRules")
        log("EvaluationManager", "applyRules()")

        if average >= ACCEPT_THRESHOLD and consensus:
            outcome = "accepted"
        elif average < REJECT_THRESHOLD:
            outcome = "rejected"
        else:
            outcome = "revision"

        log("EvaluationManager", f"Outcome determined: {outcome.upper()}")
        return outcome

    # ---- alt branch dispatcher ----
    def _dispatchNotification(self, outcome: str):
        if outcome == "accepted":
            self._notification_service.notifyAcceptance(self._submission_id, self._author)
        elif outcome == "rejected":
            self._notification_service.notifyRejection(self._submission_id, self._author)
        else:
            self._notification_service.notifyRevision(self._submission_id, self._author)
