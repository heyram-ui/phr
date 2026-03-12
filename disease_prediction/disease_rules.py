# disease_prediction/disease_rules.py

DISEASE_RULES = {

    # ══════════════════════════════════
    # 1. CARDIOVASCULAR (8 diseases)
    # ══════════════════════════════════

    "Heart Disease": {
        "category": "Cardiovascular", "icon": "❤️",
        "conditions": [
            {"field": "bp_sys",        "operator": ">",  "value": 140, "weight": 25},
            {"field": "bp_dias",       "operator": ">",  "value": 90,  "weight": 15},
            {"field": "bmi",           "operator": ">",  "value": 30,  "weight": 15},
            {"field": "smoking",       "operator": "==", "value": 1,   "weight": 20},
            {"field": "activity_mins", "operator": "<",  "value": 30,  "weight": 15},
            {"field": "age",           "operator": ">",  "value": 50,  "weight": 10},
        ]
    },
    "Hypertension": {
        "category": "Cardiovascular", "icon": "🩺",
        "conditions": [
            {"field": "bp_sys",        "operator": ">",  "value": 130,    "weight": 35},
            {"field": "bp_dias",       "operator": ">",  "value": 85,     "weight": 25},
            {"field": "stress_level",  "operator": "==", "value": "High", "weight": 20},
            {"field": "alcohol",       "operator": "==", "value": "heavy","weight": 10},
            {"field": "activity_mins", "operator": "<",  "value": 20,     "weight": 10},
        ]
    },
    "Stroke Risk": {
        "category": "Cardiovascular", "icon": "🧠",
        "conditions": [
            {"field": "bp_sys",        "operator": ">",  "value": 150, "weight": 30},
            {"field": "smoking",       "operator": "==", "value": 1,   "weight": 25},
            {"field": "age",           "operator": ">",  "value": 55,  "weight": 20},
            {"field": "bmi",           "operator": ">",  "value": 35,  "weight": 15},
            {"field": "activity_mins", "operator": "<",  "value": 15,  "weight": 10},
        ]
    },
    "Coronary Artery Disease": {
        "category": "Cardiovascular", "icon": "🫀",
        "conditions": [
            {"field": "bp_sys",        "operator": ">",  "value": 140, "weight": 25},
            {"field": "smoking",       "operator": "==", "value": 1,   "weight": 25},
            {"field": "glucose",       "operator": ">",  "value": 110, "weight": 20},
            {"field": "bmi",           "operator": ">",  "value": 30,  "weight": 15},
            {"field": "age",           "operator": ">",  "value": 50,  "weight": 15},
        ]
    },
    "Heart Failure Risk": {
        "category": "Cardiovascular", "icon": "💔",
        "conditions": [
            {"field": "bp_sys",        "operator": ">",  "value": 160,    "weight": 30},
            {"field": "bmi",           "operator": ">",  "value": 35,     "weight": 25},
            {"field": "activity_mins", "operator": "<",  "value": 15,     "weight": 20},
            {"field": "age",           "operator": ">",  "value": 60,     "weight": 15},
            {"field": "alcohol",       "operator": "==", "value": "heavy","weight": 10},
        ]
    },
    "Peripheral Artery Disease": {
        "category": "Cardiovascular", "icon": "🦵",
        "conditions": [
            {"field": "smoking",       "operator": "==", "value": 1,   "weight": 35},
            {"field": "glucose",       "operator": ">",  "value": 126, "weight": 25},
            {"field": "bp_sys",        "operator": ">",  "value": 140, "weight": 20},
            {"field": "age",           "operator": ">",  "value": 55,  "weight": 20},
        ]
    },
    "Atrial Fibrillation": {
        "category": "Cardiovascular", "icon": "📉",
        "conditions": [
            {"field": "age",           "operator": ">",  "value": 60,     "weight": 30},
            {"field": "bp_sys",        "operator": ">",  "value": 140,    "weight": 25},
            {"field": "alcohol",       "operator": "==", "value": "heavy","weight": 25},
            {"field": "bmi",           "operator": ">",  "value": 30,     "weight": 20},
        ]
    },
    "Deep Vein Thrombosis": {
        "category": "Cardiovascular", "icon": "🩸",
        "conditions": [
            {"field": "activity_mins", "operator": "<", "value": 15, "weight": 35},
            {"field": "screen_time",   "operator": ">", "value": 8,  "weight": 30},
            {"field": "bmi",           "operator": ">", "value": 30, "weight": 20},
            {"field": "age",           "operator": ">", "value": 50, "weight": 15},
        ]
    },

    # ══════════════════════════════════
    # 2. METABOLIC (7 diseases)
    # ══════════════════════════════════

    "Type 2 Diabetes": {
        "category": "Metabolic", "icon": "🩸",
        "conditions": [
            {"field": "glucose",       "operator": ">",  "value": 126,    "weight": 40},
            {"field": "bmi",           "operator": ">",  "value": 30,     "weight": 20},
            {"field": "activity_mins", "operator": "<",  "value": 30,     "weight": 20},
            {"field": "age",           "operator": ">",  "value": 45,     "weight": 10},
            {"field": "sleep_hours",   "operator": "<",  "value": 6,      "weight": 10},
        ]
    },
    "Pre-Diabetes": {
        "category": "Metabolic", "icon": "⚠️",
        "conditions": [
            {"field": "glucose",       "operator": ">",  "value": 100,    "weight": 40},
            {"field": "bmi",           "operator": ">",  "value": 27,     "weight": 25},
            {"field": "activity_mins", "operator": "<",  "value": 30,     "weight": 20},
            {"field": "stress_level",  "operator": "==", "value": "High", "weight": 15},
        ]
    },
    "Obesity": {
        "category": "Metabolic", "icon": "⚖️",
        "conditions": [
            {"field": "bmi",           "operator": ">", "value": 30, "weight": 50},
            {"field": "activity_mins", "operator": "<", "value": 20, "weight": 25},
            {"field": "screen_time",   "operator": ">", "value": 6,  "weight": 15},
            {"field": "sleep_hours",   "operator": "<", "value": 6,  "weight": 10},
        ]
    },
    "Metabolic Syndrome": {
        "category": "Metabolic", "icon": "🔬",
        "conditions": [
            {"field": "bmi",           "operator": ">",  "value": 30,     "weight": 25},
            {"field": "bp_sys",        "operator": ">",  "value": 130,    "weight": 25},
            {"field": "glucose",       "operator": ">",  "value": 100,    "weight": 25},
            {"field": "activity_mins", "operator": "<",  "value": 20,     "weight": 15},
            {"field": "alcohol",       "operator": "==", "value": "heavy","weight": 10},
        ]
    },
    "Thyroid Disorder": {
        "category": "Metabolic", "icon": "🦋",
        "conditions": [
            {"field": "stress_level",  "operator": "==", "value": "High", "weight": 30},
            {"field": "bmi",           "operator": ">",  "value": 28,     "weight": 25},
            {"field": "sleep_hours",   "operator": "<",  "value": 6,      "weight": 25},
            {"field": "activity_mins", "operator": "<",  "value": 20,     "weight": 20},
        ]
    },
    "High Cholesterol": {
        "category": "Metabolic", "icon": "🧈",
        "conditions": [
            {"field": "bmi",           "operator": ">",  "value": 28,     "weight": 30},
            {"field": "activity_mins", "operator": "<",  "value": 20,     "weight": 25},
            {"field": "smoking",       "operator": "==", "value": 1,      "weight": 20},
            {"field": "age",           "operator": ">",  "value": 40,     "weight": 15},
            {"field": "alcohol",       "operator": "==", "value": "heavy","weight": 10},
        ]
    },
    "Gout": {
        "category": "Metabolic", "icon": "🦶",
        "conditions": [
            {"field": "alcohol",       "operator": "==", "value": "heavy","weight": 35},
            {"field": "bmi",           "operator": ">",  "value": 30,     "weight": 30},
            {"field": "glucose",       "operator": ">",  "value": 110,    "weight": 20},
            {"field": "age",           "operator": ">",  "value": 40,     "weight": 15},
        ]
    },

    # ══════════════════════════════════
    # 3. SLEEP DISORDERS (5 diseases)
    # ══════════════════════════════════

    "Insomnia": {
        "category": "Sleep Disorder", "icon": "😴",
        "conditions": [
            {"field": "sleep_hours",   "operator": "<",  "value": 6,      "weight": 40},
            {"field": "stress_level",  "operator": "==", "value": "High", "weight": 30},
            {"field": "screen_time",   "operator": ">",  "value": 5,      "weight": 20},
            {"field": "activity_mins", "operator": "<",  "value": 20,     "weight": 10},
        ]
    },
    "Sleep Apnea": {
        "category": "Sleep Disorder", "icon": "😮",
        "conditions": [
            {"field": "bmi",           "operator": ">",  "value": 30,     "weight": 35},
            {"field": "sleep_hours",   "operator": "<",  "value": 6,      "weight": 25},
            {"field": "age",           "operator": ">",  "value": 40,     "weight": 20},
            {"field": "alcohol",       "operator": "==", "value": "heavy","weight": 20},
        ]
    },
    "Hypersomnia": {
        "category": "Sleep Disorder", "icon": "🛌",
        "conditions": [
            {"field": "sleep_hours",   "operator": ">",  "value": 10,     "weight": 40},
            {"field": "activity_mins", "operator": "<",  "value": 15,     "weight": 30},
            {"field": "stress_level",  "operator": "==", "value": "High", "weight": 30},
        ]
    },
    "Restless Leg Syndrome": {
        "category": "Sleep Disorder", "icon": "🦵",
        "conditions": [
            {"field": "sleep_hours",   "operator": "<",  "value": 6,      "weight": 35},
            {"field": "activity_mins", "operator": "<",  "value": 20,     "weight": 30},
            {"field": "stress_level",  "operator": "==", "value": "High", "weight": 20},
            {"field": "age",           "operator": ">",  "value": 40,     "weight": 15},
        ]
    },
    "Circadian Rhythm Disorder": {
        "category": "Sleep Disorder", "icon": "🌙",
        "conditions": [
            {"field": "screen_time",   "operator": ">",  "value": 7,      "weight": 40},
            {"field": "sleep_hours",   "operator": "<",  "value": 6,      "weight": 35},
            {"field": "stress_level",  "operator": "==", "value": "High", "weight": 25},
        ]
    },

    # ══════════════════════════════════
    # 4. MENTAL HEALTH (6 diseases)
    # ══════════════════════════════════

    "Depression": {
        "category": "Mental Health", "icon": "😔",
        "conditions": [
            {"field": "stress_level",  "operator": "==", "value": "High", "weight": 35},
            {"field": "sleep_hours",   "operator": "<",  "value": 6,      "weight": 25},
            {"field": "activity_mins", "operator": "<",  "value": 20,     "weight": 20},
            {"field": "screen_time",   "operator": ">",  "value": 7,      "weight": 20},
        ]
    },
    "Anxiety Disorder": {
        "category": "Mental Health", "icon": "😰",
        "conditions": [
            {"field": "stress_level",  "operator": "==", "value": "High", "weight": 40},
            {"field": "sleep_hours",   "operator": "<",  "value": 6,      "weight": 25},
            {"field": "screen_time",   "operator": ">",  "value": 6,      "weight": 20},
            {"field": "activity_mins", "operator": "<",  "value": 20,     "weight": 15},
        ]
    },
    "Burnout Syndrome": {
        "category": "Mental Health", "icon": "🔥",
        "conditions": [
            {"field": "stress_level",  "operator": "==", "value": "High", "weight": 40},
            {"field": "screen_time",   "operator": ">",  "value": 8,      "weight": 30},
            {"field": "sleep_hours",   "operator": "<",  "value": 6,      "weight": 30},
        ]
    },
    "PTSD Risk": {
        "category": "Mental Health", "icon": "🧠",
        "conditions": [
            {"field": "stress_level",  "operator": "==", "value": "High", "weight": 45},
            {"field": "sleep_hours",   "operator": "<",  "value": 5,      "weight": 30},
            {"field": "activity_mins", "operator": "<",  "value": 15,     "weight": 25},
        ]
    },
    "Bipolar Disorder Risk": {
        "category": "Mental Health", "icon": "🔄",
        "conditions": [
            {"field": "sleep_hours",   "operator": "<",  "value": 5,      "weight": 35},
            {"field": "stress_level",  "operator": "==", "value": "High", "weight": 35},
            {"field": "alcohol",       "operator": "==", "value": "heavy","weight": 30},
        ]
    },
    "Social Isolation Risk": {
        "category": "Mental Health", "icon": "👤",
        "conditions": [
            {"field": "screen_time",   "operator": ">",  "value": 8,      "weight": 40},
            {"field": "activity_mins", "operator": "<",  "value": 15,     "weight": 35},
            {"field": "stress_level",  "operator": "==", "value": "High", "weight": 25},
        ]
    },

    # ══════════════════════════════════
    # 5. RESPIRATORY (5 diseases)
    # ══════════════════════════════════

    "Asthma Risk": {
        "category": "Respiratory", "icon": "🫁",
        "conditions": [
            {"field": "smoking",       "operator": "==", "value": 1,  "weight": 40},
            {"field": "activity_mins", "operator": "<",  "value": 20, "weight": 25},
            {"field": "bmi",           "operator": ">",  "value": 30, "weight": 20},
            {"field": "age",           "operator": ">",  "value": 40, "weight": 15},
        ]
    },
    "COPD Risk": {
        "category": "Respiratory", "icon": "💨",
        "conditions": [
            {"field": "smoking",       "operator": "==", "value": 1,  "weight": 50},
            {"field": "age",           "operator": ">",  "value": 45, "weight": 25},
            {"field": "activity_mins", "operator": "<",  "value": 15, "weight": 25},
        ]
    },
    "Pulmonary Hypertension": {
        "category": "Respiratory", "icon": "🌬️",
        "conditions": [
            {"field": "bp_sys",        "operator": ">",  "value": 150, "weight": 30},
            {"field": "bmi",           "operator": ">",  "value": 30,  "weight": 25},
            {"field": "smoking",       "operator": "==", "value": 1,   "weight": 25},
            {"field": "activity_mins", "operator": "<",  "value": 15,  "weight": 20},
        ]
    },
    "Bronchitis Risk": {
        "category": "Respiratory", "icon": "🤧",
        "conditions": [
            {"field": "smoking",       "operator": "==", "value": 1, "weight": 45},
            {"field": "activity_mins", "operator": "<",  "value": 20,"weight": 30},
            {"field": "sleep_hours",   "operator": "<",  "value": 6, "weight": 25},
        ]
    },
    "Respiratory Infections Risk": {
        "category": "Respiratory", "icon": "🤒",
        "conditions": [
            {"field": "sleep_hours",   "operator": "<",  "value": 6,      "weight": 35},
            {"field": "stress_level",  "operator": "==", "value": "High", "weight": 30},
            {"field": "activity_mins", "operator": "<",  "value": 20,     "weight": 20},
            {"field": "smoking",       "operator": "==", "value": 1,      "weight": 15},
        ]
    },

    # ══════════════════════════════════
    # 6. MUSCULOSKELETAL (5 diseases)
    # ══════════════════════════════════

    "Chronic Back Pain": {
        "category": "Musculoskeletal", "icon": "🦴",
        "conditions": [
            {"field": "screen_time",   "operator": ">", "value": 7,  "weight": 35},
            {"field": "activity_mins", "operator": "<", "value": 20, "weight": 30},
            {"field": "bmi",           "operator": ">", "value": 30, "weight": 20},
            {"field": "age",           "operator": ">", "value": 40, "weight": 15},
        ]
    },
    "Osteoporosis Risk": {
        "category": "Musculoskeletal", "icon": "🦴",
        "conditions": [
            {"field": "activity_mins", "operator": "<",  "value": 20, "weight": 35},
            {"field": "age",           "operator": ">",  "value": 50, "weight": 35},
            {"field": "smoking",       "operator": "==", "value": 1,  "weight": 30},
        ]
    },
    "Arthritis Risk": {
        "category": "Musculoskeletal", "icon": "🤲",
        "conditions": [
            {"field": "bmi",           "operator": ">",  "value": 30, "weight": 30},
            {"field": "age",           "operator": ">",  "value": 50, "weight": 30},
            {"field": "activity_mins", "operator": "<",  "value": 20, "weight": 25},
            {"field": "smoking",       "operator": "==", "value": 1,  "weight": 15},
        ]
    },
    "Fibromyalgia Risk": {
        "category": "Musculoskeletal", "icon": "😣",
        "conditions": [
            {"field": "stress_level",  "operator": "==", "value": "High", "weight": 35},
            {"field": "sleep_hours",   "operator": "<",  "value": 6,      "weight": 35},
            {"field": "activity_mins", "operator": "<",  "value": 20,     "weight": 30},
        ]
    },
    "Neck Pain / Cervical Spondylosis": {
        "category": "Musculoskeletal", "icon": "🧍",
        "conditions": [
            {"field": "screen_time",   "operator": ">", "value": 7,  "weight": 45},
            {"field": "activity_mins", "operator": "<", "value": 20, "weight": 30},
            {"field": "age",           "operator": ">", "value": 35, "weight": 25},
        ]
    },

    # ══════════════════════════════════
    # 7. DIGESTIVE (5 diseases)
    # ══════════════════════════════════

    "Fatty Liver Disease": {
        "category": "Digestive", "icon": "🫀",
        "conditions": [
            {"field": "alcohol",       "operator": "==", "value": "heavy","weight": 35},
            {"field": "bmi",           "operator": ">",  "value": 30,     "weight": 30},
            {"field": "glucose",       "operator": ">",  "value": 110,    "weight": 20},
            {"field": "activity_mins", "operator": "<",  "value": 20,     "weight": 15},
        ]
    },
    "Gastric Ulcer Risk": {
        "category": "Digestive", "icon": "🤢",
        "conditions": [
            {"field": "stress_level",  "operator": "==", "value": "High", "weight": 40},
            {"field": "smoking",       "operator": "==", "value": 1,      "weight": 30},
            {"field": "alcohol",       "operator": "==", "value": "heavy","weight": 30},
        ]
    },
    "IBS - Irritable Bowel Syndrome": {
        "category": "Digestive", "icon": "😖",
        "conditions": [
            {"field": "stress_level",  "operator": "==", "value": "High", "weight": 45},
            {"field": "sleep_hours",   "operator": "<",  "value": 6,      "weight": 30},
            {"field": "activity_mins", "operator": "<",  "value": 20,     "weight": 25},
        ]
    },
    "Acid Reflux / GERD": {
        "category": "Digestive", "icon": "🔥",
        "conditions": [
            {"field": "bmi",           "operator": ">",  "value": 28,     "weight": 30},
            {"field": "stress_level",  "operator": "==", "value": "High", "weight": 30},
            {"field": "alcohol",       "operator": "==", "value": "heavy","weight": 25},
            {"field": "sleep_hours",   "operator": "<",  "value": 6,      "weight": 15},
        ]
    },
    "Liver Cirrhosis Risk": {
        "category": "Digestive", "icon": "🫁",
        "conditions": [
            {"field": "alcohol",       "operator": "==", "value": "heavy","weight": 50},
            {"field": "bmi",           "operator": ">",  "value": 30,     "weight": 25},
            {"field": "age",           "operator": ">",  "value": 45,     "weight": 25},
        ]
    },

    # ══════════════════════════════════
    # 8. VISION (3 diseases)
    # ══════════════════════════════════

    "Eye Strain / Digital Eye Fatigue": {
        "category": "Vision", "icon": "👁️",
        "conditions": [
            {"field": "screen_time",   "operator": ">", "value": 6,  "weight": 50},
            {"field": "sleep_hours",   "operator": "<", "value": 6,  "weight": 30},
            {"field": "activity_mins", "operator": "<", "value": 15, "weight": 20},
        ]
    },
    "Diabetic Retinopathy Risk": {
        "category": "Vision", "icon": "👁️",
        "conditions": [
            {"field": "glucose",       "operator": ">", "value": 126, "weight": 50},
            {"field": "bp_sys",        "operator": ">", "value": 140, "weight": 30},
            {"field": "age",           "operator": ">", "value": 40,  "weight": 20},
        ]
    },
    "Glaucoma Risk": {
        "category": "Vision", "icon": "🔵",
        "conditions": [
            {"field": "age",           "operator": ">", "value": 50, "weight": 35},
            {"field": "bp_sys",        "operator": ">", "value": 140,"weight": 30},
            {"field": "screen_time",   "operator": ">", "value": 7,  "weight": 20},
            {"field": "activity_mins", "operator": "<", "value": 15, "weight": 15},
        ]
    },

    # ══════════════════════════════════
    # 9. KIDNEY (3 diseases)
    # ══════════════════════════════════

    "Chronic Kidney Disease": {
        "category": "Kidney", "icon": "🫘",
        "conditions": [
            {"field": "bp_sys",        "operator": ">",  "value": 140, "weight": 35},
            {"field": "glucose",       "operator": ">",  "value": 126, "weight": 35},
            {"field": "age",           "operator": ">",  "value": 50,  "weight": 20},
            {"field": "smoking",       "operator": "==", "value": 1,   "weight": 10},
        ]
    },
    "Kidney Stones Risk": {
        "category": "Kidney", "icon": "🪨",
        "conditions": [
            {"field": "activity_mins", "operator": "<", "value": 20,  "weight": 30},
            {"field": "bmi",           "operator": ">", "value": 30,  "weight": 30},
            {"field": "glucose",       "operator": ">", "value": 110, "weight": 25},
            {"field": "age",           "operator": ">", "value": 40,  "weight": 15},
        ]
    },
    "Urinary Tract Infection Risk": {
        "category": "Kidney", "icon": "💧",
        "conditions": [
            {"field": "sleep_hours",   "operator": "<",  "value": 6,      "weight": 35},
            {"field": "stress_level",  "operator": "==", "value": "High", "weight": 35},
            {"field": "activity_mins", "operator": "<",  "value": 15,     "weight": 30},
        ]
    },

    # ══════════════════════════════════
    # 10. IMMUNE SYSTEM (3 diseases)
    # ══════════════════════════════════

    "Weakened Immunity": {
        "category": "Immune System", "icon": "🛡️",
        "conditions": [
            {"field": "sleep_hours",   "operator": "<",  "value": 6,      "weight": 35},
            {"field": "stress_level",  "operator": "==", "value": "High", "weight": 30},
            {"field": "activity_mins", "operator": "<",  "value": 20,     "weight": 20},
            {"field": "alcohol",       "operator": "==", "value": "heavy","weight": 15},
        ]
    },
    "Autoimmune Disorder Risk": {
        "category": "Immune System", "icon": "⚔️",
        "conditions": [
            {"field": "stress_level",  "operator": "==", "value": "High", "weight": 40},
            {"field": "sleep_hours",   "operator": "<",  "value": 6,      "weight": 35},
            {"field": "smoking",       "operator": "==", "value": 1,      "weight": 25},
        ]
    },
    "Chronic Inflammation": {
        "category": "Immune System", "icon": "🔴",
        "conditions": [
            {"field": "bmi",           "operator": ">",  "value": 30,     "weight": 30},
            {"field": "activity_mins", "operator": "<",  "value": 20,     "weight": 25},
            {"field": "sleep_hours",   "operator": "<",  "value": 6,      "weight": 25},
            {"field": "smoking",       "operator": "==", "value": 1,      "weight": 20},
        ]
    },

    # ══════════════════════════════════
    # 11. NEUROLOGICAL (4 diseases)
    # ══════════════════════════════════

    "Migraine": {
        "category": "Neurological", "icon": "🤕",
        "conditions": [
            {"field": "stress_level",  "operator": "==", "value": "High", "weight": 40},
            {"field": "sleep_hours",   "operator": "<",  "value": 6,      "weight": 30},
            {"field": "screen_time",   "operator": ">",  "value": 6,      "weight": 30},
        ]
    },
    "Alzheimer's Risk": {
        "category": "Neurological", "icon": "🧩",
        "conditions": [
            {"field": "age",           "operator": ">",  "value": 60,     "weight": 35},
            {"field": "activity_mins", "operator": "<",  "value": 20,     "weight": 25},
            {"field": "sleep_hours",   "operator": "<",  "value": 6,      "weight": 25},
            {"field": "smoking",       "operator": "==", "value": 1,      "weight": 15},
        ]
    },
    "Parkinson's Risk": {
        "category": "Neurological", "icon": "🤲",
        "conditions": [
            {"field": "age",           "operator": ">", "value": 60, "weight": 40},
            {"field": "activity_mins", "operator": "<", "value": 20, "weight": 30},
            {"field": "sleep_hours",   "operator": "<", "value": 6,  "weight": 30},
        ]
    },
    "Memory Loss / Cognitive Decline": {
        "category": "Neurological", "icon": "🧠",
        "conditions": [
            {"field": "sleep_hours",   "operator": "<",  "value": 6,      "weight": 35},
            {"field": "screen_time",   "operator": ">",  "value": 8,      "weight": 25},
            {"field": "stress_level",  "operator": "==", "value": "High", "weight": 25},
            {"field": "activity_mins", "operator": "<",  "value": 20,     "weight": 15},
        ]
    },

    # ══════════════════════════════════
    # 12. CANCER RISK (4 diseases)
    # ══════════════════════════════════

    "Lung Cancer Risk": {
        "category": "Cancer Risk", "icon": "🫁",
        "conditions": [
            {"field": "smoking",       "operator": "==", "value": 1,  "weight": 60},
            {"field": "age",           "operator": ">",  "value": 50, "weight": 25},
            {"field": "activity_mins", "operator": "<",  "value": 15, "weight": 15},
        ]
    },
    "Colon Cancer Risk": {
        "category": "Cancer Risk", "icon": "🔬",
        "conditions": [
            {"field": "activity_mins", "operator": "<",  "value": 20,     "weight": 30},
            {"field": "bmi",           "operator": ">",  "value": 30,     "weight": 25},
            {"field": "alcohol",       "operator": "==", "value": "heavy","weight": 25},
            {"field": "age",           "operator": ">",  "value": 50,     "weight": 20},
        ]
    },
    "Breast Cancer Risk": {
        "category": "Cancer Risk", "icon": "🎗️",
        "conditions": [
            {"field": "bmi",           "operator": ">",  "value": 30,     "weight": 30},
            {"field": "alcohol",       "operator": "==", "value": "heavy","weight": 30},
            {"field": "activity_mins", "operator": "<",  "value": 20,     "weight": 25},
            {"field": "age",           "operator": ">",  "value": 45,     "weight": 15},
        ]
    },
    "Skin Cancer Risk": {
        "category": "Cancer Risk", "icon": "☀️",
        "conditions": [
            {"field": "age",           "operator": ">",  "value": 40, "weight": 35},
            {"field": "smoking",       "operator": "==", "value": 1,  "weight": 30},
            {"field": "activity_mins", "operator": "<",  "value": 15, "weight": 35},
        ]
    },

    # ══════════════════════════════════
    # 13. HORMONAL (3 diseases)
    # ══════════════════════════════════

    "PCOS Risk": {
        "category": "Hormonal", "icon": "⚡",
        "conditions": [
            {"field": "bmi",           "operator": ">",  "value": 27,     "weight": 35},
            {"field": "stress_level",  "operator": "==", "value": "High", "weight": 30},
            {"field": "activity_mins", "operator": "<",  "value": 20,     "weight": 20},
            {"field": "sleep_hours",   "operator": "<",  "value": 6,      "weight": 15},
        ]
    },
    "Adrenal Fatigue": {
        "category": "Hormonal", "icon": "😩",
        "conditions": [
            {"field": "stress_level",  "operator": "==", "value": "High", "weight": 45},
            {"field": "sleep_hours",   "operator": "<",  "value": 6,      "weight": 35},
            {"field": "activity_mins", "operator": "<",  "value": 15,     "weight": 20},
        ]
    },
    "Hormonal Imbalance": {
        "category": "Hormonal", "icon": "⚖️",
        "conditions": [
            {"field": "stress_level",  "operator": "==", "value": "High", "weight": 30},
            {"field": "sleep_hours",   "operator": "<",  "value": 6,      "weight": 30},
            {"field": "bmi",           "operator": ">",  "value": 28,     "weight": 25},
            {"field": "activity_mins", "operator": "<",  "value": 20,     "weight": 15},
        ]
    },

    # ══════════════════════════════════
    # 14. LIFESTYLE (3 diseases)
    # ══════════════════════════════════

    "Vitamin D Deficiency": {
        "category": "Lifestyle", "icon": "☀️",
        "conditions": [
            {"field": "activity_mins", "operator": "<", "value": 20, "weight": 40},
            {"field": "screen_time",   "operator": ">", "value": 8,  "weight": 35},
            {"field": "sleep_hours",   "operator": "<", "value": 6,  "weight": 25},
        ]
    },
    "Dehydration Risk": {
        "category": "Lifestyle", "icon": "💧",
        "conditions": [
            {"field": "screen_time",   "operator": ">",  "value": 7,      "weight": 35},
            {"field": "stress_level",  "operator": "==", "value": "High", "weight": 35},
            {"field": "activity_mins", "operator": "<",  "value": 20,     "weight": 30},
        ]
    },
    "Sedentary Lifestyle Syndrome": {
        "category": "Lifestyle", "icon": "🛋️",
        "conditions": [
            {"field": "activity_mins", "operator": "<", "value": 15, "weight": 40},
            {"field": "screen_time",   "operator": ">", "value": 8,  "weight": 35},
            {"field": "bmi",           "operator": ">", "value": 28, "weight": 25},
        ]
    },

}