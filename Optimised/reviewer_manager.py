
from utils import call_counter, log
from reviewer import Reviewer

MAX_WORKLOAD = 4

# Reviewer store lives here now, not in the Database
_REVIEWER_STORE = [
    {"id": "R1", "name": "Dr. Alice Mokoena",  "conflicts": [],       "workload": 2},
    {"id": "R2", "name": "Prof. Brian Nkosi",   "conflicts": ["S001"], "workload": 5},
    {"id": "R3", "name": "Dr. Carol Dlamini",   "conflicts": [],       "workload": 1},
    {"id": "R4", "name": "Dr. David Sithole",   "conflicts": [],       "workload": 4},
]


class ReviewerManager:
    def __init__(self):
        # No database dependency needed anymore
        pass

    def getAvailableReviewers(self, submission_id: str) -> list:
        """
        Returns a filtered list of Reviewer objects in a single call.
        Combines what was three separate calls in the Original:
          fetchReviewers() + filterConflicts() + checkWorkload()
        All done here, internally, in one place.
        """
        call_counter.increment("ReviewerManager.getAvailableReviewers")
        log("ReviewerManager", "getAvailableReviewers()")

        reviewer_objects = [Reviewer(r) for r in _REVIEWER_STORE]

        # Filter out conflict of interest
        no_conflicts = [r for r in reviewer_objects if submission_id not in r.conflicts]
        log("ReviewerManager", f"After conflict filter: {len(no_conflicts)} reviewer(s) remain")

        # Filter out overloaded reviewers
        available = [r for r in no_conflicts if r.workload < MAX_WORKLOAD]
        log("ReviewerManager", f"After workload filter: {len(available)} reviewer(s) available")

        return available

    def assignReviewers(self, reviewers: list, submission_id: str):
        """
        Assigns all reviewers to the submission in one call.
        Optimisation: replaces the per-reviewer loop in SubmissionController.
        Original had SubmissionController call assignReview() on each reviewer
        separately inside a loop — that is the controller doing the reviewer's job.
        """
        call_counter.increment("ReviewerManager.assignReviewers")
        log("ReviewerManager", f"assignReviewers() — assigning {len(reviewers)} reviewer(s)")
        for reviewer in reviewers:
            reviewer.assignReview(submission_id)
