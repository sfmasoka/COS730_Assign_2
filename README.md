## Overview
This folder contains the baseline (unoptimised)
## Structure
```
Original/
├── main.py                  # Entry point — runs all 4 test scenarios
├── ui.py                    # UI class
├── submission_controller.py # SubmissionController class
├── validator.py             # Validator class
├── database.py              # Database class
├── reviewer_manager.py      # ReviewerManager class
├── reviewer.py              # Reviewer class
├── evaluation_manager.py    # EvaluationManager class
├── notification_service.py  # NotificationService class
└── utils.py                 # Shared CallCounter + logger
```

## How to Run
No external dependencies required — standard Python 3.8+.

```bash
cd Original
python main.py
```

## Test Scenarios
| Scenario | Input | Expected Outcome |
|---|---|---|
| 1 | Missing `content` field | Validation error returned |
| 2 | Scores: 8.5, 9.0, 8.0 | ACCEPTED |
| 3 | Scores: 2.0, 3.5, 2.5 | REJECTED |
| 4 | Scores: 5.0, 7.5, 4.5 | REVISION NEEDED |

