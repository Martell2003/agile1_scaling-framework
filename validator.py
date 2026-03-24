from data_access import save_validation_record, load_validation_records
from datetime import datetime

CHECKLIST = [
    "Framework characterization is accurate and evidence-based",
    "SAW weight vectors are plausible and literature-supported",
    "Recommendations are coherent with organisational inputs",
    "Tool logic is internally consistent across test cases",
    "Rationale explanations are clear and understandable",
    "User interface is intuitive and easy to navigate"
]


def load_checklist() -> list[str]:
    return CHECKLIST


def save_feedback(responses: dict, comments: str) -> None:
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "responses": responses,
        "comments": comments,
        "summary": {
            "total_items": len(responses),
            "passed": sum(1 for v in responses.values() if v == "Pass"),
            "failed": sum(1 for v in responses.values() if v == "Fail")
        }
    }
    save_validation_record(record)


def get_validation_summary() -> dict:
    records = load_validation_records()
    if not records:
        return {"total_sessions": 0, "message": "No validation records found"}

    latest = records[-1]
    return {
        "total_sessions": len(records),
        "latest_timestamp": latest["timestamp"],
        "latest_summary": latest["summary"],
        "latest_comments": latest["comments"]
    }
