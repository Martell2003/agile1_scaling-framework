import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def load_framework_data() -> dict:
    path = os.path.join(DATA_DIR, "framework_knowledge_base.json")
    with open(path, "r") as f:
        return json.load(f)

def load_weight_vectors() -> dict:
    path = os.path.join(DATA_DIR, "weight_vectors.json")
    with open(path, "r") as f:
        return json.load(f)

def load_case_studies() -> list:
    path = os.path.join(DATA_DIR, "case_studies.json")
    with open(path, "r") as f:
        data = json.load(f)
        return data["case_studies"]

def load_validation_records() -> list:
    path = os.path.join(DATA_DIR, "validation_records.json")
    with open(path, "r") as f:
        return json.load(f)

def save_validation_record(record: dict) -> None:
    path = os.path.join(DATA_DIR, "validation_records.json")
    with open(path, "r+") as f:
        data = json.load(f)
        data.append(record)
        f.seek(0)
        json.dump(data, f, indent=2)
        