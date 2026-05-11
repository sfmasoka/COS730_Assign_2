
from utils import call_counter, log
from validator import Validator
from database import Database
from reviewer_manager import ReviewerManager
from evaluation_manager import EvaluationManager

NUM_REVIEWERS_TO_ASSIGN = 3   # how many reviewers get assigned per submission


class SubmissionController:
    def __init__(self):
        self._validator         = Validator()
        self._database          = Database()
        self._reviewer_manager  = ReviewerManager(self._database)
        self._evaluation_manager = EvaluationManager(self._database)

    def submit(self, data: dict):
        """
        Main pipeline as per sequence diagram.
        """
        call_counter.increment("SubmissionController.submit")
        log("SubmissionController", "submit(data)")

        # --- Validation ---
        is_valid = self._validator.validateFormat(data)

        # alt: invalid
        if not is_valid:
            log("SubmissionController", "Returning error to UI — invalid submission")
            return {"status": "error", "message": "Submission format is invalid."}

        # alt: valid — save submission
        submission_id = self._database.saveSubmission(data)

        # Get available reviewers
        filtered_reviewers = self.getAvailableReviewers(submission_id)

        if not filtered_reviewers:
            log("SubmissionController", "No reviewers available — aborting")
            return {"status": "error", "message": "No reviewers available for this submission."}

        # Assign simulated scores to each reviewer so evaluation has data
        import random
        score_pool = data.get("simulated_scores", None)
        for i, reviewer in enumerate(filtered_reviewers):
            if score_pool and i < len(score_pool):
                reviewer.score = score_pool[i]
            else:
                reviewer.score = round(random.uniform(3.0, 10.0), 1)

        # --- loop: assign reviewers ---
        assigned = filtered_reviewers[:NUM_REVIEWERS_TO_ASSIGN]
        for reviewer in assigned:
            self.assignReview(reviewer, submission_id)

        # --- Start evaluation ---
        self.startEvaluation(submission_id, data.get("author", "Unknown"), assigned)

        return {"status": "success", "submission_id": submission_id}

    def getAvailableReviewers(self, submission_id: str) -> list:
        call_counter.increment("SubmissionController.getAvailableReviewers")
        log("SubmissionController", "getAvailableReviewers()")
        return self._reviewer_manager.getAvailableReviewers(submission_id)

    def assignReview(self, reviewer, submission_id: str):
        call_counter.increment("SubmissionController.assignReview")
        log("SubmissionController", f"assignReview() — assigning {reviewer.name}")
        reviewer.assignReview(submission_id)

    def startEvaluation(self, submission_id: str, author: str, assigned_reviewers: list):
        call_counter.increment("SubmissionController.startEvaluation")
        log("SubmissionController", "startEvaluation()")
        self._evaluation_manager.startEvaluation(submission_id, author, assigned_reviewers)
