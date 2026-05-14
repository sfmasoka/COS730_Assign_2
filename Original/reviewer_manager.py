from utils import call_counter, log
from reviewer import Reviewer


class ReviewerManager:
    def __init__(self, database):
        self._database = database
        # A single Reviewer proxy instance used to call filter methods
        # (mirrors the diagram where ReviewerManager calls methods on Reviewer)
        self._reviewer_proxy = Reviewer({
            "id": "PROXY",
            "name": "ReviewerProxy",
            "conflicts": [],
            "workload": 0
        })

    def getAvailableReviewers(self, submission_id: str) -> list:
        """
        Full sequence as per diagram:
          1. Call Database.fetchReviewers()
          2. Call Reviewer.filterConflicts(reviewerList)
          3. Call Reviewer.checkWorkload(reviewerList)
          4. Return filteredReviewers
        """
        call_counter.increment("ReviewerManager.getAvailableReviewers")
        log("ReviewerManager", "getAvailableReviewers()")

        # Step 1 — fetch raw reviewer data from database
        raw_reviewers = self._database.fetchReviewers()

        # Wrap raw dicts into Reviewer objects
        reviewer_objects = [Reviewer(r) for r in raw_reviewers]

        # Step 2 — delegate conflict filtering to Reviewer proxy
        after_conflicts = self._reviewer_proxy.filterConflicts(reviewer_objects, submission_id)

        # Step 3 — delegate workload check to Reviewer proxy
        filtered_reviewers = self._reviewer_proxy.checkWorkload(after_conflicts)

        log("ReviewerManager", f"Returning {len(filtered_reviewers)} filteredReviewers to SubmissionController")
        return filtered_reviewers
