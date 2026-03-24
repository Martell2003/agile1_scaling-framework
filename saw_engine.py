from data_access import load_framework_data, load_weight_vectors


def normalise_inputs(profile: dict) -> dict:
    normalised = {}

    # Higher score = better fit; divide by max possible value (5)
    normalised["cultural_maturity"] = profile["cultural_maturity"] / 5
    normalised["regulatory_constraint"] = profile["regulatory_constraint"] / 5
    normalised["technical_debt"] = profile["technical_debt"] / 5

    # Binary sector flag: Technology=1, Government=0
    normalised["sector"] = 1 if profile["sector"] == "Technology" else 0

    # Org size normalised against a defined maximum (5000 employees)
    normalised["org_size"] = min(profile["org_size"] / 5000, 1.0)

    # Organizational size as a separate normalised dimension
    normalised["organizational_size"] = min(profile["org_size"] / 5000, 1.0)

    # Governance model encoded as a numeric value
    governance_map = {"Centralized": 0.25, "Hybrid": 0.60, "Devolved": 1.0}
    normalised["governance_model"] = governance_map.get(
        profile["governance_model"], 0.5
    )

    # Team distribution — derived from org size as a proxy
    normalised["team_distribution"] = min(profile["org_size"] / 5000, 1.0)

    # Sector fit is a framework property not a user input,
    # so we set it to 1.0 and let the framework score carry the weight
    normalised["sector_fit"] = 1.0

    return normalised


def calculate_scores(profile: dict) -> list[dict]:
    normalised = normalise_inputs(profile)
    frameworks = load_framework_data()
    weight_vecs = load_weight_vectors()

    sector = profile["sector"]
    weights = weight_vecs[sector]

    results = []

    for fw_name, fw_scores in frameworks.items():
        # Handle sector_fit as a nested dict
        fw_flat = dict(fw_scores)
        fw_flat["sector_fit"] = fw_scores["sector_fit"][sector]

        composite = sum(
            weights[dim] * normalised[dim] * fw_flat[dim]
            for dim in weights
        )

        results.append({
            "framework": fw_name,
            "score": round(composite, 4)
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def generate_rationale(profile: dict, results: list[dict]) -> str:
    top = results[0]["framework"]
    score = results[0]["score"]
    sector = profile["sector"]
    maturity = profile["cultural_maturity"]
    regulation = profile["regulatory_constraint"]

    rationale_map = {
        "SAFe": (
            "SAFe is recommended for its structured governance and multi-team "
            "coordination capabilities. Its prescriptive Agile Release Train model "
            "aligns with your organisation's size, regulatory constraints, and "
            "governance requirements."
        ),
        "LeSS": (
            "LeSS is recommended for its minimalist, descaling approach. "
            "It is best suited to organisations with high cultural maturity "
            "and low governance overhead, where agility is already embedded "
            "in the team culture."
        ),
        "Scrum@Scale": (
            "Scrum@Scale is recommended for its modular, fractal structure. "
            "It offers flexibility across distributed teams while keeping core "
            "Scrum principles intact, balancing structure with adaptability."
        )
    }

    context = (
        f"Your profile — {sector} sector, cultural maturity {maturity}/5, "
        f"regulatory constraint {regulation}/5 — shaped this result."
    )

    return (
        f"Recommended Framework: {top} (Score: {score})\n\n"
        f"{rationale_map[top]}\n\n"
        f"{context}"
    )
