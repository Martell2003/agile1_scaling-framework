def validate_inputs(profile: dict) -> tuple[bool, str]:
    required = [
        "sector",
        "org_size",
        "governance_model",
        "cultural_maturity",
        "regulatory_constraint",
        "technical_debt"
    ]

    for field in required:
        if field not in profile or profile[field] is None:
            return False, f"Missing required field: {field}"

    score_fields = [
        "cultural_maturity",
        "regulatory_constraint",
        "technical_debt"
    ]

    for field in score_fields:
        if not (1 <= profile[field] <= 5):
            return False, f"{field} must be between 1 and 5"

    if profile["sector"] not in ["Technology", "Government"]:
        return False, "Sector must be Technology or Government"

    if not isinstance(profile["org_size"], (int, float)) or profile["org_size"] < 1:
        return False, "Organisation size must be a positive number"

    if profile["governance_model"] not in ["Centralized", "Devolved", "Hybrid"]:
        return False, "Governance model must be Centralized, Devolved, or Hybrid"

    return True, "Valid"
