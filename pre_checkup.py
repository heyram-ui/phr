"""
=============================================================================
PRE-CHECKUP CALCULATOR
File: pre_checkup.py
Location: Paste in your PROJECT ROOT FOLDER (same place as app.py)
=============================================================================
Calculates: Systolic BP, Diastolic BP, BMI, Glucose Estimate
From: Simple daily routine questions user CAN answer
=============================================================================
"""

def calculate_bmi(weight_kg, height_cm):
    """
    Calculate BMI from weight and height
    User KNOWS their weight and height!
    """
    if height_cm <= 0 or weight_kg <= 0:
        return 22.0, 'Normal'
    
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    bmi = round(bmi, 1)
    
    if bmi < 18.5:
        category = 'Underweight'
    elif bmi < 25.0:
        category = 'Normal'
    elif bmi < 30.0:
        category = 'Overweight'
    else:
        category = 'Obese'
    
    return bmi, category


def estimate_glucose(user_data):
    """
    Estimate Blood Glucose from lifestyle factors
    User CANNOT measure glucose without equipment
    But we can ESTIMATE from their daily habits!
    
    Normal fasting glucose: 70-99 mg/dL
    Pre-diabetes: 100-125 mg/dL
    Diabetes: 126+ mg/dL
    """
    
    # Base glucose (normal fasting)
    base_glucose = 85.0
    glucose_score = 0
    
    # AGE FACTOR
    age = user_data.get('age', 30)
    if age > 60:
        glucose_score += 15
    elif age > 50:
        glucose_score += 10
    elif age > 40:
        glucose_score += 7
    elif age > 30:
        glucose_score += 3
    
    # BMI FACTOR (Strongest predictor of glucose!)
    bmi = user_data.get('bmi', 22)
    if bmi >= 35:
        glucose_score += 30
    elif bmi >= 30:
        glucose_score += 20
    elif bmi >= 27:
        glucose_score += 12
    elif bmi >= 25:
        glucose_score += 8
    elif bmi < 18.5:
        glucose_score -= 5
    
    # DIET FACTORS
    sugar_intake = user_data.get('sugar_intake', 'medium')
    if sugar_intake == 'very_high':
        glucose_score += 20
    elif sugar_intake == 'high':
        glucose_score += 12
    elif sugar_intake == 'medium':
        glucose_score += 5
    elif sugar_intake == 'low':
        glucose_score -= 5
    
    # Eating frequency
    meal_timing = user_data.get('meal_timing', 'regular')
    if meal_timing == 'irregular':
        glucose_score += 8
    elif meal_timing == 'skip_meals':
        glucose_score += 10
    elif meal_timing == 'regular':
        glucose_score -= 3
    
    # Carb intake
    carb_intake = user_data.get('carb_intake', 'medium')
    if carb_intake == 'very_high':
        glucose_score += 15
    elif carb_intake == 'high':
        glucose_score += 8
    elif carb_intake == 'low':
        glucose_score -= 5
    
    # LIFESTYLE FACTORS
    exercise_days = user_data.get('exercise_days', 3)
    if exercise_days == 0:
        glucose_score += 10
    elif exercise_days <= 2:
        glucose_score += 5
    elif exercise_days >= 5:
        glucose_score -= 8
    
    # Sleep
    sleep_hours = user_data.get('sleep_hours', 7)
    if sleep_hours < 6:
        glucose_score += 8
    elif sleep_hours < 7:
        glucose_score += 4
    elif 7 <= sleep_hours <= 9:
        glucose_score -= 3
    
    # Stress (stress raises glucose!)
    stress = user_data.get('stress_level', 5)
    if stress >= 8:
        glucose_score += 12
    elif stress >= 6:
        glucose_score += 6
    elif stress <= 3:
        glucose_score -= 3
    
    # FAMILY HISTORY (Genetic factor)
    family_diabetes = user_data.get('family_history_diabetes', False)
    if family_diabetes:
        glucose_score += 15
    
    # SYMPTOMS (Direct glucose indicators)
    # "Are you always thirsty?"
    always_thirsty = user_data.get('always_thirsty', False)
    if always_thirsty:
        glucose_score += 15
    
    # "Do you feel very tired after eating?"
    tired_after_eating = user_data.get('tired_after_eating', False)
    if tired_after_eating:
        glucose_score += 10
    
    # "Do you urinate frequently?"
    frequent_urination = user_data.get('frequent_urination', False)
    if frequent_urination:
        glucose_score += 12
    
    # "Do you have blurry vision?"
    blurry_vision = user_data.get('blurry_vision', False)
    if blurry_vision:
        glucose_score += 10
    
    # "Do you eat sweets/desserts daily?"
    daily_sweets = user_data.get('daily_sweets', False)
    if daily_sweets:
        glucose_score += 8
    
    # CALCULATE FINAL GLUCOSE
    estimated_glucose = base_glucose + glucose_score
    
    # Apply physiological limits
    estimated_glucose = max(60, min(int(estimated_glucose), 300))
    
    # Categorize
    if estimated_glucose < 70:
        glucose_category = 'Low (Hypoglycemia)'
        glucose_risk = 'Concern'
        glucose_color = 'blue'
    elif estimated_glucose <= 99:
        glucose_category = 'Normal'
        glucose_risk = 'Low'
        glucose_color = 'green'
    elif estimated_glucose <= 125:
        glucose_category = 'Pre-diabetes'
        glucose_risk = 'Medium'
        glucose_color = 'orange'
    else:
        glucose_category = 'High (Diabetes Risk)'
        glucose_risk = 'High'
        glucose_color = 'red'
    
    return {
        'glucose': estimated_glucose,
        'category': glucose_category,
        'risk': glucose_risk,
        'color': glucose_color,
        'estimated': True,
        'note': 'Estimated from lifestyle factors. For accurate reading, use glucometer after 8-hour fast.'
    }


def estimate_bp(user_data):
    """
    Estimate Systolic and Diastolic BP
    from daily routine questions
    """
    
    systolic_score = 0
    diastolic_score = 0
    
    # AGE FACTOR
    age = user_data.get('age', 30)
    if age > 60:
        systolic_score += 12
        diastolic_score += 7
    elif age > 50:
        systolic_score += 9
        diastolic_score += 5
    elif age > 40:
        systolic_score += 6
        diastolic_score += 3
    elif age > 30:
        systolic_score += 3
        diastolic_score += 1
    
    # GENDER
    gender = user_data.get('gender', 'Male')
    if gender == 'Male':
        systolic_score += 2
        diastolic_score += 1
    
    # BMI FACTOR (Key predictor!)
    bmi = user_data.get('bmi', 22)
    if bmi >= 35:
        systolic_score += 15
        diastolic_score += 10
    elif bmi >= 30:
        systolic_score += 10
        diastolic_score += 7
    elif bmi >= 27:
        systolic_score += 7
        diastolic_score += 4
    elif bmi >= 25:
        systolic_score += 5
        diastolic_score += 3
    elif bmi < 18.5:
        systolic_score -= 3
        diastolic_score -= 2
    
    # MORNING SYMPTOMS (Direct BP indicators!)
    morning_headache = user_data.get('morning_headache', False)
    if morning_headache:
        systolic_score += 8
        diastolic_score += 5
    
    dizzy_standing = user_data.get('dizzy_when_standing', False)
    if dizzy_standing:
        systolic_score -= 8  # LOW BP sign
        diastolic_score -= 5
    
    nosebleeds = user_data.get('frequent_nosebleeds', False)
    if nosebleeds:
        systolic_score += 7
        diastolic_score += 4
    
    vision_issues = user_data.get('blurry_vision', False)
    if vision_issues:
        systolic_score += 6
        diastolic_score += 4
    
    palpitations = user_data.get('heart_palpitations', False)
    if palpitations:
        systolic_score += 5
        diastolic_score += 3
    
    # LIFESTYLE FACTORS
    smoking = user_data.get('smoking', 'non_smoker')
    if smoking == 'regular':
        systolic_score += 10
        diastolic_score += 6
    elif smoking == 'occasional':
        systolic_score += 5
        diastolic_score += 3
    
    alcohol = user_data.get('alcohol', 'none')
    if alcohol == 'heavy':
        systolic_score += 10
        diastolic_score += 6
    elif alcohol == 'moderate':
        systolic_score += 4
        diastolic_score += 2
    
    salt_intake = user_data.get('salt_intake', 'medium')
    if salt_intake == 'very_high':
        systolic_score += 10
        diastolic_score += 6
    elif salt_intake == 'high':
        systolic_score += 7
        diastolic_score += 4
    elif salt_intake == 'low':
        systolic_score -= 5
        diastolic_score -= 3
    
    # EXERCISE FACTOR (Protective!)
    exercise_days = user_data.get('exercise_days', 3)
    if exercise_days == 0:
        systolic_score += 8
        diastolic_score += 5
    elif exercise_days <= 2:
        systolic_score += 4
        diastolic_score += 2
    elif exercise_days >= 5:
        systolic_score -= 6
        diastolic_score -= 4
    
    # SLEEP FACTOR
    sleep_hours = user_data.get('sleep_hours', 7)
    if sleep_hours < 5:
        systolic_score += 9
        diastolic_score += 6
    elif sleep_hours < 6:
        systolic_score += 6
        diastolic_score += 4
    elif sleep_hours < 7:
        systolic_score += 3
        diastolic_score += 2
    elif 7 <= sleep_hours <= 9:
        systolic_score -= 2
        diastolic_score -= 1
    
    # STRESS FACTOR
    stress = user_data.get('stress_level', 5)
    if stress >= 9:
        systolic_score += 12
        diastolic_score += 8
    elif stress >= 7:
        systolic_score += 8
        diastolic_score += 5
    elif stress >= 5:
        systolic_score += 4
        diastolic_score += 2
    elif stress <= 3:
        systolic_score -= 4
        diastolic_score -= 2
    
    # WATER INTAKE
    water_liters = user_data.get('water_liters', 2)
    if water_liters < 1:
        systolic_score += 5
        diastolic_score += 3
    elif water_liters >= 2.5:
        systolic_score -= 3
        diastolic_score -= 2
    
    # FAMILY HISTORY
    family_bp = user_data.get('family_history_bp', False)
    if family_bp:
        systolic_score += 7
        diastolic_score += 4
    
    # SEDENTARY LIFESTYLE
    sitting_hours = user_data.get('sitting_hours', 8)
    if sitting_hours >= 10:
        systolic_score += 6
        diastolic_score += 4
    elif sitting_hours >= 8:
        systolic_score += 3
        diastolic_score += 2
    
    # BASE BP (Normal healthy 30-year-old)
    base_systolic = 112 + (age - 30) * 0.4
    base_diastolic = 72 + (age - 30) * 0.25
    
    # CALCULATE ESTIMATED BP
    estimated_systolic = int(base_systolic + (systolic_score * 1.5))
    estimated_diastolic = int(base_diastolic + (diastolic_score * 1.2))
    
    # APPLY PHYSIOLOGICAL LIMITS
    estimated_systolic = max(85, min(estimated_systolic, 210))
    estimated_diastolic = max(55, min(estimated_diastolic, 130))
    
    # CATEGORIZE
    if estimated_systolic < 90 or estimated_diastolic < 60:
        category = 'Low BP'
        color = 'blue'
        risk = 'Concern'
    elif estimated_systolic < 120 and estimated_diastolic < 80:
        category = 'Normal'
        color = 'green'
        risk = 'Low'
    elif estimated_systolic < 130 and estimated_diastolic < 80:
        category = 'Elevated'
        color = 'yellow'
        risk = 'Low-Medium'
    elif estimated_systolic < 140 or estimated_diastolic < 90:
        category = 'Stage 1 Hypertension'
        color = 'orange'
        risk = 'Medium'
    elif estimated_systolic < 180 or estimated_diastolic < 120:
        category = 'Stage 2 Hypertension'
        color = 'red'
        risk = 'High'
    else:
        category = 'Hypertensive Crisis'
        color = 'darkred'
        risk = 'Critical'
    
    return {
        'systolic': estimated_systolic,
        'diastolic': estimated_diastolic,
        'bp_reading': f"{estimated_systolic}/{estimated_diastolic}",
        'category': category,
        'color': color,
        'risk': risk,
        'estimated': True,
        'confidence': 75,
        'note': 'Estimated from your daily routine. For accurate reading, use BP monitor.'
    }


def run_pre_checkup(form_data):
    """
    MAIN FUNCTION: Run complete pre-checkup
    Call this from app.py!
    
    Args:
        form_data: dict from HTML form (pre-checkup page)
    
    Returns:
        dict with BMI, BP, Glucose - ready to auto-fill main form!
    """
    
    # STEP 1: Calculate BMI (from weight + height)
    weight = float(form_data.get('weight', 70))
    height = float(form_data.get('height', 170))
    bmi, bmi_category = calculate_bmi(weight, height)
    
    # Add BMI to user data for other calculations
    form_data['bmi'] = bmi
    
    # STEP 2: Estimate Blood Pressure
    bp_result = estimate_bp(form_data)
    
    # STEP 3: Estimate Glucose
    glucose_result = estimate_glucose(form_data)
    
    # STEP 4: Return everything ready for main form
    return {
        # ✅ BMI - CALCULATED (exact)
        'bmi': bmi,
        'bmi_category': bmi_category,
        'bmi_calculated': True,
        
        # ✅ BP - ESTIMATED from routine
        'bp_sys': bp_result['systolic'],
        'bp_dias': bp_result['diastolic'],
        'bp_category': bp_result['category'],
        'bp_estimated': True,
        'bp_confidence': bp_result['confidence'],
        
        # ✅ GLUCOSE - ESTIMATED from lifestyle
        'glucose': glucose_result['glucose'],
        'glucose_category': glucose_result['category'],
        'glucose_estimated': True,
        
        # Summary for display
        'summary': {
            'bmi': f"{bmi} ({bmi_category})",
            'bp': f"{bp_result['bp_reading']} mmHg ({bp_result['category']})",
            'glucose': f"{glucose_result['glucose']} mg/dL ({glucose_result['category']})"
        },
        
        # Disclaimer
        'disclaimer': '⚠️ These are ESTIMATED values based on your daily routine. For accurate readings, use medical equipment.',
        
        # Raw results for detailed display
        'bp_detail': bp_result,
        'glucose_detail': glucose_result
    }