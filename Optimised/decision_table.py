
ACCEPT_THRESHOLD = 7.0
REJECT_THRESHOLD = 4.0
CONSENSUS_MARGIN = 2.0


def determine_outcome(average: float, consensus: bool) -> str:

    rules = [
        (average >= ACCEPT_THRESHOLD and consensus,      "accepted"),
        (average >= ACCEPT_THRESHOLD and not consensus,  "revision"),
        (average < REJECT_THRESHOLD,                     "rejected"),
        (True,                                           "revision"),   # catch-all
    ]

    for condition, outcome in rules:
        if condition:
            return outcome

    return "revision"  # should never reach here
