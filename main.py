
import time
from ui import UI
from utils import call_counter


def divider(title: str):
  
    print(f"  SCENARIO: {title}")
   


def run_scenario(scenario_name: str, data: dict):
    divider(scenario_name)
    call_counter.reset()

    ui = UI()
    start = time.perf_counter()
    ui.submitResearchOutput(data)
    elapsed = time.perf_counter() - start

    print("\n  --- Call Counter Report ---")
    for method, count in call_counter.report().items():
        print(f"      {method:<45} {count:>3} call(s)")
    print(f"\n  TOTAL method calls : {call_counter.total()}")
    print(f"  Execution time     : {elapsed * 1000:.4f} ms")


#  Scenario 1 – Invalid submission (missing 'content' field)
run_scenario(
    "1 — INVALID SUBMISSION",
    {
        "title": "Quantum Entanglement in Networks",
        "author": "Thabo Ndlovu",
        # 'content' is deliberately missing
    }
)

#  Scenario 2 – Valid, outcome: ACCEPTED

#  All three reviewers give high scores (average >= 7.0, spread <= 2.0)
run_scenario(
    "2 — VALID → ACCEPTED",
    {
        "title": "Deep Learning for Resource Allocation",
        "author": "Zanele Khumalo",
        "content": "This paper investigates deep reinforcement learning applied to cloud resource scheduling.",
        "simulated_scores": [8.5, 9.0, 8.0],   # avg=8.5, spread=1.0 → ACCEPTED
    }
)

#  Scenario 3 – Valid, outcome: REJECTED
#  All reviewers give low scores (average < 4.0)
run_scenario(
    "3 — VALID → REJECTED",
    {
        "title": "Blockchain for Everything",
        "author": "Sipho Dube",
        "content": "A very shallow exploration of blockchain with no experimental results.",
        "simulated_scores": [2.0, 3.5, 2.5],   # avg=2.67 → REJECTED
    }
)

#  Scenario 4 – Valid, outcome: REVISION NEEDED
#  Scores are mixed — above reject threshold but below accept threshold
run_scenario(
    "4 — VALID → REVISION NEEDED",
    {
        "title": "Federated Learning in Healthcare",
        "author": "Naledi Mosia",
        "content": "Explores federated learning for privacy-preserving medical data analysis.",
        "simulated_scores": [5.0, 7.5, 4.5],   # avg=5.67, spread=3.0 → REVISION
    }
)


print("  All scenarios complete.")

