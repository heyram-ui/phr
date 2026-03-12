import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle
import os

print("🔄 Initializing Multi-Disease Training Engine...")

# Standard Features for the App
common_columns = ['age', 'bmi', 'sleep_hours', 'activity_mins', 'stress_level', 'bp_sys', 'bp_dias', 'screen_time', 'Diagnosis']
master_data = pd.DataFrame(columns=common_columns)

# --- 1. LOAD DIABETES DATASET ---
if os.path.exists('diabetes_data.csv'):
    print("✅ Loading Diabetes Dataset...")
    try:
        df_d = pd.read_csv('diabetes_data.csv')
        
        # Clean column names (strip spaces)
        df_d.columns = df_d.columns.str.strip()
        
        temp_df = pd.DataFrame()
        # Handle Capitalization (Age vs age)
        if 'Age' in df_d.columns: temp_df['age'] = df_d['Age']
        elif 'age' in df_d.columns: temp_df['age'] = df_d['age']
        
        if 'BMI' in df_d.columns: temp_df['bmi'] = df_d['BMI']
        elif 'bmi' in df_d.columns: temp_df['bmi'] = df_d['bmi']
        
        # Glucose & BP
        if 'Glucose' in df_d.columns: temp_df['glucose'] = df_d['Glucose']
        if 'BloodPressure' in df_d.columns:
            temp_df['bp_dias'] = df_d['BloodPressure']
            temp_df['bp_sys'] = temp_df['bp_dias'] + 40 # Estimate
            
        # Fill Defaults
        temp_df['sleep_hours'] = 7.0
        temp_df['activity_mins'] = 30
        temp_df['stress_level'] = 5
        temp_df['screen_time'] = 6.0
        
        # Diagnosis Label
        if 'Outcome' in df_d.columns:
            temp_df['Diagnosis'] = df_d['Outcome'].apply(lambda x: 'Diabetes Type 2' if x == 1 else 'Healthy')
        
        master_data = pd.concat([master_data, temp_df], ignore_index=True)
        print(f"   -> Added {len(temp_df)} Diabetes records.")
    except Exception as e:
        print(f"   ⚠️ Error loading Diabetes data: {e}")

# --- 2. LOAD HEART DATASET (The Fix is Here) ---
if os.path.exists('heart_data.csv'):
    print("✅ Loading Heart Dataset...")
    try:
        # 1. Try reading with standard comma
        df_h = pd.read_csv('heart_data.csv')
        
        # 2. If 'age' column is missing, try Semicolon separator (Common Kaggle issue)
        if 'age' not in df_h.columns and 'Age' not in df_h.columns:
            print("   -> Detected semicolon separator. Reloading...")
            df_h = pd.read_csv('heart_data.csv', sep=';')

        # Clean column names
        df_h.columns = df_h.columns.str.strip()
        
        temp_df = pd.DataFrame()
        
        # Age (Convert days to years if needed)
        if 'age' in df_h.columns:
            temp_df['age'] = df_h['age'] // 365 if df_h['age'].mean() > 150 else df_h['age']
        elif 'Age' in df_h.columns:
             temp_df['age'] = df_h['Age'] // 365 if df_h['Age'].mean() > 150 else df_h['Age']
            
        # BMI Calculation (weight / height^2) if BMI column missing
        # Many heart datasets have 'weight' (kg) and 'height' (cm)
        if 'weight' in df_h.columns and 'height' in df_h.columns:
            # Convert height to meters
            temp_df['bmi'] = df_h['weight'] / ((df_h['height'] / 100) ** 2)
        else:
            temp_df['bmi'] = 28.0 # Default fallback
            
        # Blood Pressure
        if 'ap_hi' in df_h.columns: temp_df['bp_sys'] = df_h['ap_hi']
        if 'ap_lo' in df_h.columns: temp_df['bp_dias'] = df_h['ap_lo']
        
        # Activity
        if 'active' in df_h.columns:
            temp_df['activity_mins'] = df_h['active'] * 45
        else:
            temp_df['activity_mins'] = 30
            
        # Defaults
        temp_df['sleep_hours'] = 6.5
        temp_df['stress_level'] = 7
        temp_df['screen_time'] = 5.0
        
        # Diagnosis
        if 'cardio' in df_h.columns:
            temp_df['Diagnosis'] = df_h['cardio'].apply(lambda x: 'Heart Disease' if x == 1 else 'Healthy')
        elif 'target' in df_h.columns:
            temp_df['Diagnosis'] = df_h['target'].apply(lambda x: 'Heart Disease' if x == 1 else 'Healthy')

        # Filter meaningful data (remove bad columns)
        master_data = pd.concat([master_data, temp_df], ignore_index=True)
        print(f"   -> Added {len(temp_df)} Heart records.")
        
    except Exception as e:
         print(f"   ⚠️ Error loading Heart data: {e}")


# --- 3. LOAD SLEEP DATASET ---
if os.path.exists('sleep_data.csv'):
    print("✅ Loading Sleep Dataset...")
    try:
        df_s = pd.read_csv('sleep_data.csv')
        
        temp_df = pd.DataFrame()
        if 'Age' in df_s.columns: temp_df['age'] = df_s['Age']
        if 'Sleep Duration' in df_s.columns: temp_df['sleep_hours'] = df_s['Sleep Duration']
        if 'Physical Activity Level' in df_s.columns: temp_df['activity_mins'] = df_s['Physical Activity Level']
        if 'Stress Level' in df_s.columns: temp_df['stress_level'] = df_s['Stress Level']
        
        # BP Split
        if 'Blood Pressure' in df_s.columns:
            try:
                temp_df[['bp_sys', 'bp_dias']] = df_s['Blood Pressure'].str.split('/', expand=True).astype(float)
            except:
                temp_df['bp_sys'] = 120
                temp_df['bp_dias'] = 80
        
        # BMI Map
        bmi_map = {'Normal': 22, 'Overweight': 28, 'Obese': 33, 'Normal Weight': 22}
        if 'BMI Category' in df_s.columns:
            temp_df['bmi'] = df_s['BMI Category'].map(bmi_map).fillna(25)
        else:
            temp_df['bmi'] = 25
            
        temp_df['screen_time'] = 8.0
        
        # Diagnosis
        if 'Sleep Disorder' in df_s.columns:
            temp_df['Diagnosis'] = df_s['Sleep Disorder'].apply(lambda x: 'Sleep Insomnia' if str(x) != 'nan' and x != 'None' else 'Healthy')
            
        master_data = pd.concat([master_data, temp_df], ignore_index=True)
        print(f"   -> Added {len(temp_df)} Sleep records.")

    except Exception as e:
        print(f"   ⚠️ Error loading Sleep data: {e}")

# --- 4. ROBUST FALLBACK (Synthetic Data) ---
# If all downloads fail or data is corrupted, we generate data so your project WORKS.
if len(master_data) < 100:
    print("⚠️ Real datasets failed or empty. Generating Synthetic Data to save the day...")
    count = 1000
    data = {
        'age': np.random.randint(20, 75, count),
        'bmi': np.random.uniform(18.0, 38.0, count),
        'sleep_hours': np.random.uniform(3.5, 10.0, count),
        'activity_mins': np.random.randint(0, 150, count),
        'stress_level': np.random.randint(1, 10, count),
        'bp_sys': np.random.randint(90, 190, count),
        'bp_dias': np.random.randint(60, 120, count),
        'screen_time': np.random.uniform(1.0, 14.0, count)
    }
    df_syn = pd.DataFrame(data)
    
    def synthetic_rules(row):
        if row['bmi'] > 30 and row['activity_mins'] < 30: return 'Diabetes Type 2'
        if row['bp_sys'] > 140: return 'Heart Disease'
        if row['sleep_hours'] < 5.5 and row['stress_level'] > 6: return 'Sleep Insomnia'
        return 'Healthy'
        
    df_syn['Diagnosis'] = df_syn.apply(synthetic_rules, axis=1)
    master_data = pd.concat([master_data, df_syn], ignore_index=True)

# Final Cleanup
master_data = master_data[common_columns].dropna()

print(f"📊 Final Training Set: {len(master_data)} records.")
print(master_data['Diagnosis'].value_counts())

# --- TRAINING ---
print("🧠 Training Unified Model...")
X = master_data.drop('Diagnosis', axis=1)
y = master_data['Diagnosis']

le = LabelEncoder()
y_encoded = le.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

acc = model.score(X_test, y_test)
print(f"🎯 Accuracy: {acc*100:.2f}%")

artifacts = {'model': model, 'encoder': le}
with open('health_model.pkl', 'wb') as f:
    pickle.dump(artifacts, f)

print("💾 'health_model.pkl' Updated Successfully!")