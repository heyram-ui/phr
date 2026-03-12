"""
=================================================================================
BP ESTIMATOR  —  bp_estimator.py
Drop this file next to app.py.
=================================================================================
estimate_blood_pressure(data) -> dict
    systolic    : int
    diastolic   : int
    confidence  : int   (0-100)
    category    : str
    message     : str

interpret_bp_result(result) -> str   (human-readable sentence)
=================================================================================
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def _bmi(weight_kg: float, height_cm: float) -> float:
    if height_cm <= 0:
        return 22.0
    h_m = height_cm / 100.0
    return weight_kg / (h_m ** 2)


# ---------------------------------------------------------------------------
# Category classification
# ---------------------------------------------------------------------------

def _bp_category(systolic: int, diastolic: int) -> str:
    if systolic < 90 or diastolic < 60:
        return "Hypotension"
    if systolic < 120 and diastolic < 80:
        return "Normal"
    if systolic < 130 and diastolic < 80:
        return "Elevated"
    if systolic < 140 or diastolic < 90:
        return "Stage 1 Hypertension"
    if systolic < 180 and diastolic < 120:
        return "Stage 2 Hypertension"
    return "Hypertensive Crisis"


# ---------------------------------------------------------------------------
# Main estimator
# ---------------------------------------------------------------------------

def estimate_blood_pressure(data: dict) -> dict:
    """
    Rule-based / heuristic BP estimator.

    Parameters
    ----------
    data : dict
        age                         : int   (years)
        weight                      : float (kg)
        height                      : float (cm)
        exercise_minutes            : int   (minutes/day)
        sleep_hours                 : float (hours/night)
        stress_level                : int   (1-10)
        smoking                     : bool
        alcohol_frequency           : str   ('never'|'occasionally'|'regularly'|'daily')
        salt_intake                 : str   ('low'|'medium'|'high')
        family_history_hypertension : bool
        sedentary_hours             : int   (hours/day)
        water_intake                : int   (glasses/day)

    Returns
    -------
    dict with keys: systolic, diastolic, confidence, category, message
    """

    age       = int(data.get("age", 30))
    weight    = float(data.get("weight", 70))
    height    = float(data.get("height", 170))
    exercise  = int(data.get("exercise_minutes", 30))
    sleep     = float(data.get("sleep_hours", 7))
    stress    = int(data.get("stress_level", 5))
    smoking   = bool(data.get("smoking", False))
    alcohol   = str(data.get("alcohol_frequency", "never")).lower()
    salt      = str(data.get("salt_intake", "medium")).lower()
    family    = bool(data.get("family_history_hypertension", False))
    sedentary = int(data.get("sedentary_hours", 8))
    water     = int(data.get("water_intake", 8))

    bmi = _bmi(weight, height)

    # ── Baseline (healthy young adult) ──────────────────────────────────────
    sys  = 112.0
    dias = 72.0

    # ── Age adjustment ───────────────────────────────────────────────────────
    # +0.5 mmHg systolic / +0.25 diastolic per year over 25
    age_over = max(0, age - 25)
    sys  += age_over * 0.50
    dias += age_over * 0.25

    # ── BMI adjustment ────────────────────────────────────────────────────────
    if bmi >= 30:
        sys  += 12
        dias += 7
    elif bmi >= 25:
        sys  += 6
        dias += 3
    elif bmi < 18.5:
        sys  -= 4
        dias -= 2

    # ── Smoking ──────────────────────────────────────────────────────────────
    if smoking:
        sys  += 10
        dias += 6

    # ── Alcohol ──────────────────────────────────────────────────────────────
    alcohol_map = {"never": 0, "occasionally": 3, "regularly": 7, "daily": 12}
    al_bump = alcohol_map.get(alcohol, 0)
    sys  += al_bump
    dias += al_bump * 0.5

    # ── Salt intake ──────────────────────────────────────────────────────────
    salt_map = {"low": -4, "medium": 0, "high": 9}
    salt_bump = salt_map.get(salt, 0)
    sys  += salt_bump
    dias += salt_bump * 0.5

    # ── Stress ───────────────────────────────────────────────────────────────
    # stress 1-10 → +0 to +12 systolic
    stress_bump = max(0, stress - 3) * 1.6
    sys  += stress_bump
    dias += stress_bump * 0.5

    # ── Sleep ─────────────────────────────────────────────────────────────────
    if sleep < 5:
        sys  += 9
        dias += 5
    elif sleep < 6:
        sys  += 5
        dias += 3
    elif sleep > 9:
        sys  -= 2
        dias -= 1

    # ── Exercise ─────────────────────────────────────────────────────────────
    if exercise >= 60:
        sys  -= 10
        dias -= 6
    elif exercise >= 30:
        sys  -= 6
        dias -= 3
    elif exercise < 10:
        sys  += 5
        dias += 3

    # ── Sedentary hours ───────────────────────────────────────────────────────
    if sedentary >= 10:
        sys  += 5
        dias += 3
    elif sedentary <= 4:
        sys  -= 3
        dias -= 2

    # ── Water intake ──────────────────────────────────────────────────────────
    if water >= 8:
        sys  -= 3
        dias -= 2
    elif water <= 4:
        sys  += 4
        dias += 2

    # ── Family history ────────────────────────────────────────────────────────
    if family:
        sys  += 7
        dias += 4

    # ── Clamp to physiologically plausible range ──────────────────────────────
    sys  = int(_clamp(round(sys),  70, 200))
    dias = int(_clamp(round(dias), 40, 130))

    # Ensure sys > dias by a reasonable margin
    if sys <= dias + 20:
        sys = dias + 20

    # ── Confidence score ─────────────────────────────────────────────────────
    # More data → higher confidence; this estimator always has full data so 75-85
    confidence = 78
    if smoking and salt == "high" and family:
        confidence = 82        # consistent risk factors → more certain
    if bmi > 35 or stress >= 9:
        confidence = min(85, confidence + 3)

    category = _bp_category(sys, dias)

    return {
        "systolic":   sys,
        "diastolic":  dias,
        "confidence": confidence,
        "category":   category,
        "message":    _category_message(category),
    }


# ---------------------------------------------------------------------------
# Interpretation
# ---------------------------------------------------------------------------

_MESSAGES = {
    "Hypotension":          "Your estimated BP is low. Stay hydrated and avoid prolonged standing.",
    "Normal":               "Your estimated BP is in the healthy range. Keep up your current lifestyle.",
    "Elevated":             "Your BP is slightly elevated. Reduce salt and increase physical activity.",
    "Stage 1 Hypertension": "Stage 1 hypertension detected. Consider lifestyle changes and consult a doctor.",
    "Stage 2 Hypertension": "Stage 2 hypertension. Medical evaluation is strongly recommended.",
    "Hypertensive Crisis":  "Critical BP range. Seek medical attention immediately.",
}


def _category_message(category: str) -> str:
    return _MESSAGES.get(category, "Unable to classify blood pressure.")


def interpret_bp_result(result: dict) -> str:
    """
    Return a human-readable interpretation of an estimate_blood_pressure() result.
    """
    sys       = result.get("systolic",   120)
    dias      = result.get("diastolic",  80)
    cat       = result.get("category",   _bp_category(sys, dias))
    conf      = result.get("confidence", 75)
    msg       = result.get("message",    _category_message(cat))

    return (
        f"Estimated blood pressure: {sys}/{dias} mmHg — {cat}. "
        f"{msg} "
        f"(Estimation confidence: {conf}%)"
    )


# ---------------------------------------------------------------------------
# Quick self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    sample = {
        "age": 45,
        "weight": 85,
        "height": 175,
        "exercise_minutes": 20,
        "sleep_hours": 6,
        "stress_level": 7,
        "smoking": True,
        "alcohol_frequency": "occasionally",
        "salt_intake": "high",
        "family_history_hypertension": True,
        "sedentary_hours": 9,
        "water_intake": 5,
    }
    res = estimate_blood_pressure(sample)
    print("Result :", res)
    print("Interp :", interpret_bp_result(res))