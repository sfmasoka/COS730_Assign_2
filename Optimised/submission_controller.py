
from utils import call_counter, log
from validator import Validator
from database import Database
from reviewer_manager import ReviewerManager
from evaluation_manager import EvaluationManager

NUM_REVIEWERS = 3


class SubmissionController:
    def __init__(self):
        self._validator          = Validator()
        self._database           = Database()
        self._reviewer_manager   = ReviewerManager()       # no database argument needed
        self._evaluation_manager = EvaluationManager(self._database)

    def submit(self, data: dict):
        call_counter.increment("SubmissionController.submit")
        log("SubmissionController", "submit(data)")

        # Validate
        is_valid = self._validator.validateFormat(data)
        if not is_valid:
            log("SubmissionController", "Returning error — invalid submission")
            return {"status": "error", "message": "Submission format is invalid."}

        # Save
        submission_id = self._database.saveSubmission(data)

        # Get reviewers (one call — filters internally)
        available = self._reviewer_manager.getAvailableReviewers(submission_id)
        if not available:
            return {"status": "error", "message": "No reviewers available."}

        # Attach simulated scores
        import random
        score_pool = data.get("simulated_scores", None)
        for i, reviewer in enumerate(available):
            if score_pool and i < len(score_pool):
                reviewer.score = score_pool[i]
            else:
                reviewer.score = round(random.uniform(3.0, 10.0), 1)

        # Assign all at once (one call replaces N-call loop)
        assigned = available[:NUM_REVIEWERS]
        self._reviewer_manager.assignReviewers(assigned, submission_id)

        # Evaluate
        self._evaluation_manager.startEvaluation(
            submission_id, data.get("author", "Unknown"), assigned
        )

        return {"status": "success", "submission_id": submission_id}
