# disease_predictor.py

# Included directly to avoid relative ImportError crashes
DISEASE_RULES = {
    "Type 2 Diabetes": {
        "category": "Metabolic",
        "icon": "fa-tint",
        "conditions": [
            {"field": "glucose", "operator": ">=", "value": 125, "weight": 5},
            {"field": "bmi", "operator": ">=", "value": 30, "weight": 3},
            {"field": "age", "operator": ">", "value": 45, "weight": 2}
        ]
    },
    "Hypertension": {
        "category": "Cardiovascular",
        "icon": "fa-heartbeat",
        "conditions": [
            {"field": "bp_sys", "operator": ">=", "value": 130, "weight": 4},
            {"field": "bp_dias", "operator": ">=", "value": 85, "weight": 3},
            {"field": "stress_level", "operator": "==", "value": "High", "weight": 2}
        ]
    },
    "Sleep Apnea": {
        "category": "Sleep & Neuro",
        "icon": "fa-bed",
        "conditions": [
            {"field": "bmi", "operator": ">=", "value": 30, "weight": 4},
            {"field": "sleep_hours", "operator": "<=", "value": 5, "weight": 3}
        ]
    }
    # Add the rest of your 64 diseases here...
}

def calculate_disease_probabilities(user_data):
    results = []

    for disease_name, disease_info in DISEASE_RULES.items():
        total_weight   = 0
        matched_weight = 0
        matched_factors = []

        for condition in disease_info['conditions']:
            field    = condition['field']
            operator = condition['operator']
            value    = condition['value']
            weight   = condition['weight']

            total_weight += weight

            user_value = user_data.get(field)
            if user_value is None:
                continue

            matched = False
            if operator == ">"  and user_value > value:  matched = True
            if operator == "<"  and user_value < value:  matched = True
            if operator == ">=" and user_value >= value: matched = True
            if operator == "<=" and user_value <= value: matched = True
            if operator == "==" and user_value == value: matched = True

            if matched:
                matched_weight += weight
                matched_factors.append(field.replace('_', ' ').title())

        if total_weight > 0:
            probability = round((matched_weight / total_weight) * 100)
        else:
            probability = 0

        if probability > 0:
            results.append({
                "name":        disease_name,
                "category":    disease_info['category'],
                "icon":        disease_info['icon'],
                "probability": probability,
                "factors":     matched_factors,
                "risk_level":  get_risk_level(probability)
            })

    results.sort(key=lambda x: x['probability'], reverse=True)
    return results


def get_risk_level(probability):
    if probability >= 70:
        return {"label": "High Risk",   "color": "danger",  "badge": "🔴"}
    elif probability >= 40:
        return {"label": "Medium Risk", "color": "warning", "badge": "🟡"}
    else:
        return {"label": "Low Risk",    "color": "success", "badge": "🟢"}


def get_top_diseases(user_data, top_n=10):
    return calculate_disease_probabilities(user_data)[:top_n]


def get_by_category(user_data):
    all_results = calculate_disease_probabilities(user_data)
    grouped = {}
    for disease in all_results:
        cat = disease['category']
        if cat not in grouped:
            grouped[cat] = []
        grouped[cat].append(disease)
    return grouped