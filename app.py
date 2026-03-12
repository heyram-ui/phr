"""
=================================================================================
COMPLETE HEALTH RISK PREDICTION SYSTEM - INTEGRATED VERSION
=================================================================================
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash, make_response
from flask_cors import CORS
import hashlib
from datetime import datetime, date
import json
from flask_mail import Mail, Message
import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
import pickle
import numpy as np
import os
from dotenv import load_dotenv
from io import BytesIO

# Flexible Import: Works if disease_predictor is in the same folder OR in a subfolder
try:
    from disease_prediction.disease_predictor import get_top_diseases, get_by_category
except ImportError:
    from disease_predictor import get_top_diseases, get_by_category

load_dotenv()

# =============================================================================
# FLASK APP — defined FIRST before anything else
# =============================================================================

app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key_change_in_production')

GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

# =============================================================================
# BP ESTIMATOR
# =============================================================================

try:
    from bp_estimator import estimate_blood_pressure, interpret_bp_result
    BP_ESTIMATOR_AVAILABLE = True
    print("✅ BP Estimator Loaded Successfully")
except ImportError:
    BP_ESTIMATOR_AVAILABLE = False
    print("⚠️  BP Estimator not available")
except Exception as e:
    BP_ESTIMATOR_AVAILABLE = False
    print(f"⚠️  BP Estimator error: {e}")

# =============================================================================
# DATABASE
# =============================================================================

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=os.getenv('DB_PORT', '5432'),
            sslmode=os.getenv('DB_SSLMODE', 'prefer')
        )
        return conn
    except Exception as e:
        print(f"❌ DB Connection Error: {e}")
        return None

def init_db():
    conn = get_db_connection()
    if not conn:
        print("❌ Database setup skipped.")
        return
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            age INTEGER,
            emergency_contact TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS assessments (
            id SERIAL PRIMARY KEY,
            user_id INTEGER,
            bp_sys INTEGER,
            bp_dias INTEGER,
            bp_estimated BOOLEAN DEFAULT FALSE,
            bp_confidence INTEGER,
            glucose REAL,
            bmi REAL,
            smoking INTEGER,
            alcohol TEXT,
            sleep_hours REAL,
            screen_time REAL,
            activity_mins INTEGER,
            stress_level INTEGER,
            risk_heart_rate TEXT,
            risk_diabetes TEXT,
            risk_hypertension TEXT,
            risk_sleep_apnea TEXT,
            risk_anxiety TEXT,
            risk_obesity TEXT,
            overall_score INTEGER,
            overall_risk TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS feedback (
            id SERIAL PRIMARY KEY,
            user_id INTEGER,
            name TEXT,
            rating INTEGER,
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS recovery_logs (
            id SERIAL PRIMARY KEY,
            user_id INTEGER,
            disease_name TEXT,
            date DATE,
            diet_quality INTEGER,
            exercise_mins INTEGER,
            symptom_severity INTEGER,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        conn.commit()
        print("✅ Database Initialized Successfully")
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        conn.rollback()
    finally:
        conn.close()

# =============================================================================
# ML MODEL
# =============================================================================

try:
    with open('health_model.pkl', 'rb') as f:
        artifacts     = pickle.load(f)
        ml_model      = artifacts['model']
        label_encoder = artifacts['encoder']
    print("✅ ML Model Loaded")
except FileNotFoundError:
    print("⚠️  health_model.pkl not found. Using rule-based fallback.")
    ml_model      = None
    label_encoder = None
except Exception as e:
    print(f"⚠️  ML Model loading error: {e}")
    ml_model      = None
    label_encoder = None

# =============================================================================
# HEALTH KNOWLEDGE BASE
# =============================================================================

HEALTH_KNOWLEDGE_BASE = {
    'Diabetes Type 2': {
        'title': 'Type 2 Diabetes', 'icon': 'fa-tint', 'color': 'warning',
        'symptoms': ['Thirst', 'Frequent Urination', 'Blurry Vision', 'Fatigue'],
        'struggle': 'Energy crashes, dizziness, constant hunger.',
        'daily_plan': {
            'Phase 1': 'Strict Low Carb Diet. 15 mins walking.',
            'Phase 2': 'Intermittent Fasting (16:8).',
            'Phase 3': 'Strength training 3x week.'
        },
        'recovery': {
            'yoga': [{'name': 'Kapalbhati'}, {'name': 'Dhanurasana'}],
            'diet': {'good': ['Leafy Greens', 'Bitter Gourd'], 'bad': ['Sugar', 'Rice']}
        }
    },
    'Heart Disease': {
        'title': 'Heart Disease', 'icon': 'fa-heartbeat', 'color': 'danger',
        'symptoms': ['Chest Pain', 'Shortness of Breath', 'Palpitations', 'Fatigue'],
        'struggle': 'Difficulty climbing stairs, tiredness.',
        'daily_plan': {
            'Phase 1': 'Complete Rest. No salt.',
            'Phase 2': 'Light Yoga (Pranayama).',
            'Phase 3': 'Brisk walking 45 mins.'
        },
        'recovery': {
            'yoga': [{'name': 'Tadasana'}, {'name': 'Shavasana'}],
            'diet': {'good': ['Oats', 'Salmon', 'Berries'], 'bad': ['Fried foods', 'Salt']}
        }
    },
    'Sleep Insomnia': {
        'title': 'Insomnia', 'icon': 'fa-bed', 'color': 'primary',
        'symptoms': ["Can't Sleep", 'Irritability', 'Headaches', 'Focus issues'],
        'struggle': 'Chronic fatigue, brain fog.',
        'daily_plan': {
            'Phase 1': 'No Screens after 8 PM.',
            'Phase 2': 'Wake up at same time daily.',
            'Phase 3': 'Magnesium supplements.'
        },
        'recovery': {
            'yoga': [{'name': 'Yoga Nidra'}, {'name': 'Viparita Karani'}],
            'diet': {'good': ['Warm Milk', 'Almonds'], 'bad': ['Caffeine', 'Phone']}
        }
    },
    'Hypertension': {
        'title': 'Hypertension', 'icon': 'fa-tachometer-alt', 'color': 'danger',
        'symptoms': ['Headache', 'Nosebleed', 'Vision issues', 'Chest pain'],
        'struggle': 'Dizziness, flushing.',
        'daily_plan': {
            'Phase 1': 'DASH Diet (Low Sodium).',
            'Phase 2': 'Slow breathing exercises.',
            'Phase 3': 'Weight management.'
        },
        'recovery': {
            'yoga': [{'name': 'Balasana'}, {'name': 'Sukhasana'}],
            'diet': {'good': ['Bananas', 'Beetroot'], 'bad': ['Pickles', 'Salt']}
        }
    },
    'Migraine': {
        'title': 'Migraine', 'icon': 'fa-brain', 'color': 'info',
        'symptoms': ['Throbbing Headache', 'Sensitivity to Light', 'Nausea'],
        'struggle': 'Cannot tolerate light/sound.',
        'daily_plan': {
            'Phase 1': 'Dark room rest. Hydration.',
            'Phase 2': 'Avoid caffeine/chocolate.',
            'Phase 3': 'Regular sleep schedule.'
        },
        'recovery': {
            'yoga': [{'name': 'Shishuasana'}, {'name': 'Setu Bandhasana'}],
            'diet': {'good': ['Ginger Tea', 'Water'], 'bad': ['Cheese', 'Wine']}
        }
    },
    'Obesity': {
        'title': 'Obesity', 'icon': 'fa-weight', 'color': 'warning',
        'symptoms': ['Breathlessness', 'Joint pain', 'Snoring'],
        'struggle': 'Low stamina, body pain.',
        'daily_plan': {
            'Phase 1': 'Calorie Deficit. High Protein.',
            'Phase 2': '10k Steps Daily.',
            'Phase 3': 'Strength Training.'
        },
        'recovery': {
            'yoga': [{'name': 'Surya Namaskar'}, {'name': 'Virabhadrasana'}],
            'diet': {'good': ['High Protein', 'Fiber'], 'bad': ['Sugary drinks', 'Junk']}
        }
    },
    'Common Cold': {
        'title': 'Common Cold', 'icon': 'fa-snowflake', 'color': 'info',
        'symptoms': ['Runny Nose', 'Sore Throat', 'Fever', 'Cough'],
        'struggle': 'Weakness, congestion.',
        'daily_plan': {
            'Phase 1': 'Bed rest. Ginger tea.',
            'Phase 2': 'Steam inhalation.',
            'Phase 3': 'Vitamin C supplements.'
        },
        'recovery': {
            'yoga': [{'name': 'Matsyasana'}, {'name': 'Viparita Karani'}],
            'diet': {'good': ['Soup', 'Garlic'], 'bad': ['Cold drinks', 'Dairy']}
        }
    }
}

# =============================================================================
# HEALTH PREDICTOR ENGINE
# =============================================================================

class HealthPredictor:
    def predict(self, data):
        risks = {}
        score = 0

        if data.get('bmi', 0) > 30:
            risks['obesity'] = {'level': 'High', 'color': 'red'}
            score += 15

        if data.get('bp_sys', 120) > 140:
            risks['hypertension'] = {'level': 'High', 'color': 'red'}
            score += 20
        elif data.get('bp_sys', 120) > 130:
            risks['hypertension'] = {'level': 'Medium', 'color': 'orange'}
            score += 10

        if data.get('stress', 0) > 7:
            risks['mental'] = {'level': 'High', 'color': 'orange'}
            score += 15

        if data.get('sleep_hours', 7) < 6:
            risks['sleep'] = {'level': 'High', 'color': 'red'}
            score += 15

        if ml_model and label_encoder:
            try:
                df = pd.DataFrame([{
                    'age':           data.get('age', 30),
                    'bmi':           data.get('bmi', 25),
                    'sleep_hours':   data.get('sleep_hours', 7),
                    'activity_mins': data.get('activity_mins', 30),
                    'stress_level':  data.get('stress', 5),
                    'bp_sys':        data.get('bp_sys', 120),
                    'bp_dias':       data.get('bp_dias', 80),
                    'screen_time':   data.get('screen_time', 6)
                }])
                pred = label_encoder.inverse_transform([ml_model.predict(df)[0]])[0]
                if pred == 'Diabetes Type 2':
                    risks['diabetes'] = {'level': 'High', 'color': 'red'}
                    score += 25
                elif pred == 'Heart Disease':
                    risks['heart'] = {'level': 'High', 'color': 'red'}
                    score += 30
                elif pred == 'Sleep Insomnia':
                    risks['sleep'] = {'level': 'High', 'color': 'red'}
                    score += 20
            except Exception as e:
                print(f"ML prediction error: {e}")

        for risk_type in ['diabetes', 'heart', 'sleep', 'hypertension', 'obesity', 'mental']:
            if risk_type not in risks:
                risks[risk_type] = {'level': 'Low', 'color': 'green'}

        return risks, min(score + 10, 100), {}

predictor = HealthPredictor()

# =============================================================================
# MAIL
# =============================================================================

app.config['MAIL_SERVER']   = 'smtp.gmail.com'
app.config['MAIL_PORT']     = 587
app.config['MAIL_USE_TLS']  = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
mail = Mail(app)

# =============================================================================
# ROUTES — AUTHENTICATION
# =============================================================================

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        conn = get_db_connection()
        if not conn:
            flash("System Error: Cannot connect to Database.", "danger")
            return render_template('auth/register.html')
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users (name, email, password, age, emergency_contact) VALUES (%s, %s, %s, %s, %s)",
                (
                    request.form['name'],
                    request.form['email'],
                    hashlib.sha256(request.form['password'].encode()).hexdigest(),
                    request.form['age'],
                    request.form.get('emergency_contact')
                )
            )
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            conn.rollback()
            flash('Email already registered or database error.', 'danger')
            print(f"Registration error: {e}")
        finally:
            conn.close()
    return render_template('auth/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn = get_db_connection()
        if not conn:
            flash("Database connection failed.", "danger")
            return render_template('auth/login.html')
        try:
            c = conn.cursor()
            c.execute(
                "SELECT * FROM users WHERE email=%s AND password=%s",
                (
                    request.form['email'],
                    hashlib.sha256(request.form['password'].encode()).hexdigest()
                )
            )
            user = c.fetchone()
            if user:
                session['user_id']   = user[0]
                session['user_name'] = user[1]
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid credentials!', 'danger')
        except Exception as e:
            flash('Login error occurred.', 'danger')
            print(f"Login error: {e}")
        finally:
            conn.close()
    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))

# =============================================================================
# ROUTES — DASHBOARD
# =============================================================================

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    dates, scores, history = [], [], []
    recovery_plan = None

    if conn:
        try:
            c = conn.cursor()
            c.execute(
                "SELECT * FROM assessments WHERE user_id=%s ORDER BY created_at DESC LIMIT 10",
                (session['user_id'],)
            )
            history = c.fetchall()

            if history:
                dates  = [h[22].strftime("%Y-%m-%d") for h in reversed(history)]
                scores = [h[20] for h in reversed(history)]

                latest  = history[0]
                primary = None
                if latest[15] == 'High':   primary = 'Diabetes Type 2'
                elif latest[14] == 'High': primary = 'Heart Disease'
                elif latest[17] == 'High': primary = 'Sleep Insomnia'
                elif latest[16] == 'High': primary = 'Hypertension'

                if primary and primary in HEALTH_KNOWLEDGE_BASE:
                    data = HEALTH_KNOWLEDGE_BASE[primary]
                    recovery_plan = {
                        'issue':   data['title'],
                        'insight': f"High risk detected. Recommended Plan: {data['title']}",
                        'yoga':    [y['name'] for y in data['recovery']['yoga']],
                        'diet':    data['recovery']['diet']['good']
                    }
        except Exception as e:
            print(f"Dashboard data error: {e}")
        finally:
            conn.close()

    return render_template(
        'dashboard/index.html',
        user={'name': session['user_name']},
        dates=dates,
        scores=scores,
        last_risk=history[0][21] if history else 'N/A',
        avg_score=sum(scores) / len(scores) if scores else 0,
        total_assessments=len(history),
        recovery=recovery_plan
    )

@app.route('/find_disease', methods=['GET'])
def find_disease():
    if 'user_id' not in session:
        flash("Please login to access the disease analyser.", "warning")
        return redirect(url_for('login'))
    
    # This renders the HTML form you provided earlier
    return render_template('find_disease.html')
# =============================================================================
# ROUTES — HEALTH ASSESSMENT
# =============================================================================

@app.route('/assess', methods=['GET', 'POST'])
def assess():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            form_data     = {k: request.form[k] for k in request.form}
            has_bp        = form_data.get('has_bp_measurement') == 'yes'
            bp_estimated  = False
            bp_confidence = 100

            if has_bp and form_data.get('bp_sys') and form_data.get('bp_dias'):
                bp_sys  = int(form_data['bp_sys'])
                bp_dias = int(form_data['bp_dias'])
            else:
                if BP_ESTIMATOR_AVAILABLE:
                    bp_input = {
                        'age':                         int(form_data.get('age', 30)),
                        'weight':                      float(form_data.get('weight', 70)),
                        'height':                      float(form_data.get('height', 170)),
                        'exercise_minutes':            int(form_data.get('activity_mins', 30)),
                        'sleep_hours':                 float(form_data.get('sleep_hours', 7)),
                        'stress_level':                int(form_data.get('stress', 5)),
                        'smoking':                     form_data.get('smoking') == 'yes',
                        'alcohol_frequency':           form_data.get('alcohol', 'never'),
                        'salt_intake':                 form_data.get('salt_intake', 'medium'),
                        'family_history_hypertension': form_data.get('family_history_bp') == 'yes',
                        'sedentary_hours':             int(form_data.get('sedentary_hours', 8)),
                        'water_intake':                int(form_data.get('water_intake', 8))
                    }
                    bp_result     = estimate_blood_pressure(bp_input)
                    bp_sys        = bp_result['systolic']
                    bp_dias       = bp_result['diastolic']
                    bp_estimated  = True
                    bp_confidence = bp_result['confidence']
                    flash(f'BP estimated: {bp_sys}/{bp_dias} mmHg (Confidence: {bp_confidence}%)', 'info')
                else:
                    bp_sys  = 120
                    bp_dias = 80
                    flash('BP estimation not available. Using default values.', 'warning')

            prediction_data = {
                'bmi':           float(form_data.get('bmi', 25)),
                'sleep_hours':   float(form_data.get('sleep_hours', 7)),
                'activity_mins': int(form_data.get('activity_mins', 30)),
                'stress':        int(form_data.get('stress', 5)),
                'bp_sys':        bp_sys,
                'bp_dias':       bp_dias,
                'screen_time':   float(form_data.get('screen_time', 6)),
                'age':           int(form_data.get('age', 30))
            }

            risks, score, recs = predictor.predict(prediction_data)

            conn = get_db_connection()
            if conn:
                try:
                    cur = conn.cursor()
                    cur.execute(
                        """INSERT INTO assessments
                        (user_id, bp_sys, bp_dias, bp_estimated, bp_confidence, bmi,
                        sleep_hours, screen_time, activity_mins, stress_level,
                        overall_score, overall_risk, risk_heart_rate, risk_diabetes,
                        risk_hypertension, risk_sleep_apnea, risk_obesity, created_at)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())""",
                        (
                            session['user_id'], bp_sys, bp_dias, bp_estimated, bp_confidence,
                            prediction_data['bmi'], prediction_data['sleep_hours'],
                            prediction_data['screen_time'], prediction_data['activity_mins'],
                            prediction_data['stress'], score,
                            'High' if score > 70 else 'Medium' if score > 40 else 'Low',
                            risks['heart']['level'],        risks['diabetes']['level'],
                            risks['hypertension']['level'], risks['sleep']['level'],
                            risks['obesity']['level']
                        )
                    )
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    print(f"Database save error: {e}")
                finally:
                    conn.close()

            diseases_view = [
                {'name': 'Heart Disease',  'risk_level': risks['heart']['level'],        'color': risks['heart']['color']},
                {'name': 'Diabetes',       'risk_level': risks['diabetes']['level'],     'color': risks['diabetes']['color']},
                {'name': 'Hypertension',   'risk_level': risks['hypertension']['level'], 'color': risks['hypertension']['color']},
                {'name': 'Sleep Disorder', 'risk_level': risks['sleep']['level'],        'color': risks['sleep']['color']},
                {'name': 'Obesity',        'risk_level': risks['obesity']['level'],      'color': risks['obesity']['color']}
            ]

            return render_template(
                'prediction/result.html',
                overall_score=score,
                overall_risk='High' if score > 70 else 'Medium' if score > 40 else 'Low',
                diseases=diseases_view,
                bp_sys=bp_sys, bp_dias=bp_dias,
                bp_estimated=bp_estimated, bp_confidence=bp_confidence,
                recommendations=recs
            )

        except Exception as e:
            flash(f'Assessment error: {str(e)}', 'danger')
            print(f"Assessment error: {e}")
            return redirect(url_for('assess'))

    pre = session.get('pre_checkup', {})
    return render_template('prediction/form.html', bp_estimator_available=BP_ESTIMATOR_AVAILABLE, pre=pre)

# =============================================================================
# ROUTES — 64 DISEASE PREDICTION
# =============================================================================

@app.route('/predict_disease', methods=['POST'])
def predict_disease():
    if 'user_id' not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('login'))

    try:
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        bmi    = round(weight / ((height / 100) ** 2), 1)

        user_data = {
            'age':           float(request.form['age']),
            'bmi':           bmi,
            'bp_sys':        float(request.form['bp_sys']),
            'bp_dias':       float(request.form['bp_dias']),
            'glucose':       float(request.form['glucose']),
            'sleep_hours':   float(request.form['sleep_hours']),
            'screen_time':   float(request.form['screen_time']),
            'activity_mins': float(request.form['activity_mins']),
            'smoking':       1 if request.form.get('smoking') == 'yes' else 0,
            'alcohol':       request.form.get('alcohol', 'none'),
            'stress_level':  request.form.get('stress_level', 'Low'),
        }

        top_diseases = get_top_diseases(user_data, top_n=10)
        by_category  = get_by_category(user_data)

        return render_template(
            "disease_result.html",
            user_data    = user_data,
            top_diseases = top_diseases,
            by_category  = by_category
        )

    except Exception as e:
        flash(f"Error analysing diseases: {str(e)}", "danger")
        return redirect(url_for('dashboard'))

# =============================================================================
# ROUTES — OTHER PAGES
# =============================================================================

@app.route('/who-regulations')
def who_regulations():
    return render_template('pages/who.html')

@app.route('/recommendations')
def recommendations():
    return render_template('pages/recommendations.html')

@app.route('/calculators', methods=['GET', 'POST'])
def calculators():
    if request.method == 'POST':
        try:
            age      = int(request.form.get('age', 30))
            weight   = float(request.form.get('weight', 70))
            height   = float(request.form.get('height', 170))
            sleep    = float(request.form.get('sleep_hours', 7))
            exercise = int(request.form.get('activity_mins', 30))
            screen   = float(request.form.get('screen_time', 6))
            stress   = int(request.form.get('stress', 5))
            smoking  = request.form.get('smoking', 'no')
            alcohol  = request.form.get('alcohol', 'never')
            salt     = request.form.get('salt_intake', 'medium')
            family_bp = request.form.get('family_history_bp', 'no')
            glucose_fasting = float(request.form.get('glucose', 0) or 0)

            h_m = height / 100
            bmi = round(weight / (h_m * h_m), 1)
            if bmi < 18.5:   bmi_cat = 'Underweight'
            elif bmi < 25:   bmi_cat = 'Normal'
            elif bmi < 30:   bmi_cat = 'Overweight'
            else:            bmi_cat = 'Obese'

            if glucose_fasting == 0:       glucose_cat = 'Not Provided'
            elif glucose_fasting < 70:     glucose_cat = 'Low (Hypoglycemia)'
            elif glucose_fasting <= 99:    glucose_cat = 'Normal'
            elif glucose_fasting <= 125:   glucose_cat = 'Pre-Diabetic'
            else:                          glucose_cat = 'Diabetic Range'

            bp_sys, bp_dias = 120, 80
            if BP_ESTIMATOR_AVAILABLE:
                try:
                    bp_result = estimate_blood_pressure({
                        'age': age, 'weight': weight, 'height': height,
                        'exercise_minutes': exercise, 'sleep_hours': sleep,
                        'stress_level': stress,
                        'smoking': smoking == 'yes',
                        'alcohol_frequency': alcohol,
                        'salt_intake': salt,
                        'family_history_hypertension': family_bp == 'yes',
                        'sedentary_hours': max(0, 16 - exercise // 60 - int(sleep)),
                        'water_intake': 8
                    })
                    bp_sys  = bp_result['systolic']
                    bp_dias = bp_result['diastolic']
                except:
                    pass

            if bp_sys >= 140:   bp_cat = 'High (Hypertension Stage 2)'
            elif bp_sys >= 130: bp_cat = 'Elevated (Stage 1)'
            elif bp_sys >= 120: bp_cat = 'Elevated'
            else:               bp_cat = 'Normal'

            session['pre_checkup'] = {
                'age': age, 'weight': weight, 'height': height,
                'bmi': bmi, 'bmi_cat': bmi_cat,
                'bp_sys': bp_sys, 'bp_dias': bp_dias, 'bp_cat': bp_cat,
                'glucose': glucose_fasting, 'glucose_cat': glucose_cat,
                'sleep_hours': sleep, 'activity_mins': exercise,
                'screen_time': screen, 'stress': stress,
                'smoking': smoking, 'alcohol': alcohol,
                'salt_intake': salt, 'family_history_bp': family_bp,
            }

            return render_template('pages/calculators.html',
                                   result=session['pre_checkup'], calculated=True)
        except Exception as e:
            flash(f'Calculation error: {str(e)}', 'danger')

    pre = session.get('pre_checkup', {})
    return render_template('pages/calculators.html', result=pre, calculated=bool(pre))

@app.route('/encyclopedia')
def encyclopedia():
    return render_template('pages/encyclopedia.html', diseases=HEALTH_KNOWLEDGE_BASE)

@app.route('/tracker', methods=['GET', 'POST'])
def tracker():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    disease = session.get('active_disease', 'Heart Disease')
    plan    = HEALTH_KNOWLEDGE_BASE.get(disease, HEALTH_KNOWLEDGE_BASE['Heart Disease']).get('daily_plan', {})
    conn    = get_db_connection()

    if request.method == 'POST':
        if conn:
            try:
                conn.cursor().execute(
                    """INSERT INTO recovery_logs
                    (user_id, disease_name, date, diet_quality, exercise_mins, symptom_severity, notes)
                    VALUES (%s, %s, CURRENT_DATE, %s, %s, %s, %s)""",
                    (
                        session['user_id'], disease,
                        request.form['diet'], request.form['exercise'],
                        request.form['severity'], request.form['notes']
                    )
                )
                conn.commit()
                flash("Daily Log Saved!", "success")
            except Exception as e:
                conn.rollback()
                flash("Error saving log.", "danger")
                print(f"Tracker save error: {e}")
            finally:
                conn.close()
        return redirect(url_for('tracker'))

    dates, severity = [], []
    if conn:
        try:
            c = conn.cursor()
            c.execute(
                "SELECT date, symptom_severity FROM recovery_logs WHERE user_id=%s ORDER BY date ASC LIMIT 7",
                (session['user_id'],)
            )
            hist     = c.fetchall()
            dates    = [h[0].strftime('%a') for h in hist]
            severity = [h[1] for h in hist]
        except Exception as e:
            print(f"Tracker data error: {e}")
        finally:
            conn.close()

    return render_template(
        'pages/tracker.html',
        disease=disease, plan=plan,
        dates=dates, severity=severity,
        date=date.today().strftime('%A, %B %d')
    )

@app.route('/symptom-checker', methods=['GET', 'POST'])
def symptom_checker():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    diagnosis = None
    if request.method == 'POST':
        selected = request.form.getlist('symptoms')
        best_match, max_matches = None, 0
        for disease_key, data in HEALTH_KNOWLEDGE_BASE.items():
            match_count = sum(1 for symptom in data['symptoms'] if symptom in selected)
            if match_count > max_matches:
                max_matches, best_match = match_count, disease_key
        if best_match:
            session['active_disease'] = best_match
            diagnosis = {
                'name': HEALTH_KNOWLEDGE_BASE[best_match]['title'],
                'plan': HEALTH_KNOWLEDGE_BASE[best_match]['daily_plan']
            }

    all_symptoms = sorted(list(set([s for d in HEALTH_KNOWLEDGE_BASE.values() for s in d['symptoms']])))
    return render_template('pages/symptom_checker.html', symptoms=all_symptoms, diagnosis=diagnosis)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    user = None
    if conn:
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE id=%s", (session['user_id'],))
            user = c.fetchone()
        except Exception as e:
            print(f"Profile error: {e}")
        finally:
            conn.close()
    return render_template('profile/index.html', user=user, google_maps_key=GOOGLE_MAPS_API_KEY)

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    if conn:
        try:
            c = conn.cursor()
            c.execute(
                "INSERT INTO feedback (user_id, rating, comment) VALUES (%s, %s, %s)",
                (session['user_id'], request.form.get('rating'), request.form.get('comment'))
            )
            conn.commit()
            flash("Thank you for your feedback!", "success")
        except Exception as e:
            conn.rollback()
            flash("Error submitting feedback.", "danger")
            print(f"Feedback error: {e}")
        finally:
            conn.close()
    return redirect(url_for('dashboard'))

# =============================================================================
# ROUTES — NEARBY HOSPITALS & PHARMACIES
# =============================================================================

@app.route('/nearby', methods=['GET', 'POST'])
def nearby():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    hospitals, pharmacies, error_message = [], [], None

    if request.method == 'POST':
        try:
            if not GOOGLE_MAPS_API_KEY:
                error_message = "Google Maps API key not configured."
            else:
                import googlemaps
                latitude    = float(request.form.get('latitude',  13.0827))
                longitude   = float(request.form.get('longitude', 80.2707))
                radius      = int(request.form.get('radius', 5000))
                search_type = request.form.get('search_type', 'both')
                gmaps       = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

                def fetch_places(place_type):
                    result = gmaps.places_nearby(location=(latitude, longitude), radius=radius, type=place_type)
                    places = []
                    for place in result.get('results', [])[:10]:
                        photo_ref = None
                        if place.get('photos'):
                            photo_ref = place['photos'][0].get('photo_reference')
                        places.append({
                            'name':      place.get('name'),
                            'address':   place.get('vicinity'),
                            'rating':    place.get('rating', 'N/A'),
                            'open_now':  place.get('opening_hours', {}).get('open_now', None),
                            'lat':       place['geometry']['location']['lat'],
                            'lng':       place['geometry']['location']['lng'],
                            'place_id':  place.get('place_id'),
                            'photo_ref': photo_ref,
                            'type':      place_type
                        })
                    return places

                if search_type in ('hospital', 'both'):
                    hospitals  = fetch_places('hospital')
                if search_type in ('pharmacy', 'both'):
                    pharmacies = fetch_places('pharmacy')
                if not hospitals and not pharmacies:
                    error_message = "No results found. Try increasing the search radius."

        except ImportError:
            error_message = "googlemaps not installed. Run: pip install googlemaps"
        except Exception as e:
            error_message = f"Search Error: {str(e)}"

    return render_template('pages/nearby.html',
                           hospitals=hospitals, pharmacies=pharmacies,
                           error=error_message, api_key=GOOGLE_MAPS_API_KEY)

@app.route('/nearby-hospitals', methods=['GET', 'POST'])
def nearby_hospitals():
    return redirect(url_for('nearby'))

# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.route('/api/nearby-places', methods=['POST'])
def api_nearby_places():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    if not GOOGLE_MAPS_API_KEY:
        return jsonify({'success': False, 'error': 'Google Maps API not configured'}), 500
    try:
        import googlemaps
        data        = request.json or {}
        latitude    = float(data.get('latitude',  13.0827))
        longitude   = float(data.get('longitude', 80.2707))
        radius      = int(data.get('radius', 5000))
        search_type = data.get('type', 'both')
        gmaps       = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

        def fetch(place_type):
            result = gmaps.places_nearby(location=(latitude, longitude), radius=radius, type=place_type)
            places = []
            for place in result.get('results', [])[:15]:
                photo_ref = None
                if place.get('photos'):
                    photo_ref = place['photos'][0].get('photo_reference')
                places.append({
                    'name':      place.get('name'),
                    'address':   place.get('vicinity'),
                    'rating':    place.get('rating', 'N/A'),
                    'open_now':  place.get('opening_hours', {}).get('open_now', None),
                    'lat':       place['geometry']['location']['lat'],
                    'lng':       place['geometry']['location']['lng'],
                    'place_id':  place.get('place_id'),
                    'photo_ref': photo_ref,
                    'type':      place_type
                })
            return places

        hospitals  = fetch('hospital') if search_type in ('hospital', 'both') else []
        pharmacies = fetch('pharmacy') if search_type in ('pharmacy', 'both') else []

        return jsonify({'success': True, 'hospitals': hospitals,
                        'pharmacies': pharmacies, 'total': len(hospitals) + len(pharmacies)})
    except ImportError:
        return jsonify({'success': False, 'error': 'googlemaps not installed'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/place-details', methods=['GET'])
def api_place_details():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    place_id = request.args.get('place_id')
    if not place_id:
        return jsonify({'success': False, 'error': 'place_id required'}), 400
    if not GOOGLE_MAPS_API_KEY:
        return jsonify({'success': False, 'error': 'API not configured'}), 500
    try:
        import googlemaps
        gmaps   = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
        details = gmaps.place(place_id=place_id, fields=['name', 'formatted_address',
                              'formatted_phone_number', 'website', 'opening_hours',
                              'rating', 'user_ratings_total'])
        return jsonify({'success': True, 'details': details.get('result', {})})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/estimate-bp', methods=['POST'])
def api_estimate_bp():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    if not BP_ESTIMATOR_AVAILABLE:
        return jsonify({'success': False, 'error': 'BP estimator not available'}), 500
    try:
        data = request.json
        bp_input = {
            'age':                         int(data.get('age', 30)),
            'weight':                      float(data.get('weight', 70)),
            'height':                      float(data.get('height', 170)),
            'exercise_minutes':            int(data.get('exercise_minutes', 30)),
            'sleep_hours':                 float(data.get('sleep_hours', 7)),
            'stress_level':                int(data.get('stress_level', 5)),
            'smoking':                     data.get('smoking', False),
            'alcohol_frequency':           data.get('alcohol', 'never'),
            'salt_intake':                 data.get('salt_intake', 'medium'),
            'family_history_hypertension': data.get('family_history_bp', False),
            'sedentary_hours':             int(data.get('sedentary_hours', 8)),
            'water_intake':                int(data.get('water_intake', 8))
        }
        bp_result         = estimate_blood_pressure(bp_input)
        bp_interpretation = interpret_bp_result(bp_result)
        return jsonify({'success': True, 'bp_estimate': bp_result, 'interpretation': bp_interpretation})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/test')
def api_test():
    return jsonify({
        'success':   True,
        'message':   'Health Risk Prediction API is running!',
        'timestamp': datetime.now().isoformat(),
        'features': {
            'bp_estimator':     BP_ESTIMATOR_AVAILABLE,
            'ml_model':         ml_model is not None,
            'google_maps':      GOOGLE_MAPS_API_KEY is not None,
            'disease_analysis': True
        }
    })

# =============================================================================
# MISCELLANEOUS
# =============================================================================

@app.route('/download_report')
def download_report():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    flash("PDF Download Feature - Coming Soon!", "info")
    return redirect(url_for('dashboard'))

# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

# =============================================================================
# RUN
# =============================================================================

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("🚀 HEALTH RISK PREDICTION SYSTEM - STARTING")
    print("=" * 70)

    init_db()

    print("\n📊 SYSTEM STATUS:")
    print(f"   {'✅' if ml_model              else '❌'} ML Model:        {'Loaded'     if ml_model              else 'Not Available'}")
    print(f"   {'✅' if BP_ESTIMATOR_AVAILABLE else '❌'} BP Estimator:    {'Ready'      if BP_ESTIMATOR_AVAILABLE else 'Not Available'}")
    print(f"   {'✅' if GOOGLE_MAPS_API_KEY   else '❌'} Google Maps:     {'Configured' if GOOGLE_MAPS_API_KEY   else 'Not Configured'}")
    print(f"   ✅ Disease Analysis: 64 diseases loaded")

    print("\n📍 ACCESS AT:  http://localhost:5000")
    print("🔍 API TEST:   http://localhost:5000/api/test")
    print("=" * 70 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)