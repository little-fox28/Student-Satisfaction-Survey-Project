import pandas as pd
import numpy as np
import random
import json
import sys
import io
from pathlib import Path

# Fix encoding for Vietnamese
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ============================================================================
# CONFIGURATION
# ============================================================================
PROJECT_ROOT = Path(__file__).parent.parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "data_generation_config.json"
OUTPUT_PATH = PROJECT_ROOT / "data" / "raw" / "survey_dummy_data.csv"

def load_config():
    """Load configuration from JSON file"""
    if not CONFIG_PATH.exists():
        print(f"❌ ERROR: Config file not found at {CONFIG_PATH}")
        print(f"   Đảm bảo file config/data_generation_config.json tồn tại")
        sys.exit(1)
    
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

# Load config
try:
    CONFIG = load_config()
    print("📋 Loading configuration from:", CONFIG_PATH)
    print("✓ Configuration loaded successfully\n")
except Exception as e:
    print(f"❌ Error loading configuration: {e}")
    sys.exit(1)

# Set seed
SEED = CONFIG['generation']['random_seed']
np.random.seed(SEED)
random.seed(SEED)

# Extract parameters
NUM_RECORDS = CONFIG['generation']['num_records']
GENDERS = CONFIG['demographics']['genders']
GENDER_DIST = [CONFIG['demographics']['gender_distribution'][g] for g in GENDERS]
SEMESTERS = CONFIG['demographics']['semesters']
MAJORS = CONFIG['demographics']['majors']
RESIDENCES = CONFIG['demographics']['residences']
RESIDENCE_DIST = [CONFIG['demographics']['residence_distribution'][r] for r in RESIDENCES]
WISHES = CONFIG['wishes']
SPAM_TEXTS = CONFIG['invalid_values']['spam_texts']
INVALID_MAJORS = CONFIG['invalid_values']['invalid_majors']

# Quality issue percentages
MISSING_PCT = CONFIG['data_quality_issues']['missing_values_percentage']
ILLOGICAL_PCT = CONFIG['data_quality_issues']['illogical_data_percentage']
STRAIGHTLINE_PCT = CONFIG['data_quality_issues']['straight_liners_percentage']
DUPLICATE_PCT = CONFIG['data_quality_issues']['duplicates_percentage']
SPAM_PCT = CONFIG['data_quality_issues']['spam_percentage']
OUTLIER_PCT = CONFIG['data_quality_issues']['extreme_outliers_percentage']
INVALID_MAJOR_PCT = CONFIG['data_quality_issues']['invalid_major_percentage']
INVALID_GPA_PCT = CONFIG['data_quality_issues']['invalid_gpa_percentage']
INVALID_SEMESTER_PCT = CONFIG['data_quality_issues']['invalid_semester_percentage']
QC_TRAP_FAIL_PCT = CONFIG['data_quality_issues']['qc_trap_failure_percentage']

# ============================================================================
# DATA GENERATION FUNCTIONS
# ============================================================================

def generate_demographics(n):
    """Generate demographic variables"""
    data = {
        'dem_gender': np.random.choice(GENDERS, n, p=GENDER_DIST),
        'dem_semester': np.random.choice(SEMESTERS, n),
        'dem_major': np.random.choice(MAJORS, n),
        'dem_residence': np.random.choice(RESIDENCES, n, p=RESIDENCE_DIST),
        'dem_gpa': np.random.normal(
            CONFIG['demographics']['gpa']['mean'],
            CONFIG['demographics']['gpa']['std_dev'],
            n
        ).clip(
            CONFIG['demographics']['gpa']['min'],
            CONFIG['demographics']['gpa']['max']
        ).round(2),
    }
    
    # Add invalid values
    invalid_major_idx = np.random.choice(n, size=int(n * INVALID_MAJOR_PCT), replace=False)
    for idx in invalid_major_idx:
        data['dem_major'][idx] = np.random.choice(INVALID_MAJORS)
    
    invalid_gpa_idx = np.random.choice(n, size=int(n * INVALID_GPA_PCT), replace=False)
    for idx in invalid_gpa_idx:
        data['dem_gpa'][idx] = np.random.choice(CONFIG['invalid_values']['invalid_gpa_values'])
    
    invalid_semester_idx = np.random.choice(n, size=int(n * INVALID_SEMESTER_PCT), replace=False)
    for idx in invalid_semester_idx:
        data['dem_semester'][idx] = np.random.choice(CONFIG['invalid_values']['invalid_semester_values'])
    
    return data


def generate_happiness(n, gpa):
    """Generate happiness variables"""
    base_happiness = np.random.normal(
        CONFIG['distributions']['happiness']['base_mean'],
        CONFIG['distributions']['happiness']['base_std_dev'],
        n
    )
    gpa_influence = (gpa - CONFIG['demographics']['gpa']['min']) / (CONFIG['demographics']['gpa']['max'] - CONFIG['demographics']['gpa']['min']) * 2
    
    hap_overall = (base_happiness + gpa_influence * 0.5).clip(1, 5).round(0).astype(float)
    hap_daily_joy = (hap_overall + np.random.normal(0, 0.5, n)).clip(1, 5).round(0).astype(float)
    hap_life_purpose = (hap_overall + np.random.normal(0, 0.5, n)).clip(1, 5).round(0).astype(float)
    hap_loyalty_choice = (hap_overall + np.random.normal(0, 0.5, n)).clip(1, 5).round(0).astype(float)
    
    data = {
        'hap_overall_satisfaction': hap_overall,
        'hap_daily_joy': hap_daily_joy,
        'hap_life_purpose': hap_life_purpose,
        'hap_loyalty_choice': hap_loyalty_choice,
    }
    
    # Add illogical data
    illogical_idx = np.random.choice(n, size=int(n * ILLOGICAL_PCT), replace=False)
    for idx in illogical_idx:
        if gpa[idx] > 3.5:
            data['hap_overall_satisfaction'][idx] = np.random.choice([1, 2])
            data['hap_daily_joy'][idx] = np.random.choice([1, 2])
    
    # Add missing values
    for col in data:
        missing_idx = np.random.choice(n, size=int(n * MISSING_PCT), replace=False)
        for idx in missing_idx:
            data[col][idx] = np.nan
    
    return data


def generate_academic(n, gpa):
    """Generate academic variables"""
    gpa_factor = (gpa - CONFIG['demographics']['gpa']['min']) / (CONFIG['demographics']['gpa']['max'] - CONFIG['demographics']['gpa']['min'])
    
    aca_program = (3 + gpa_factor * 1.5 + np.random.normal(0, 0.8, n)).clip(1, 5).round(0).astype(float)
    aca_teaching = (3.2 + np.random.normal(0, 1, n)).clip(1, 5).round(0).astype(float)
    aca_system = (3 + np.random.normal(0, 1, n)).clip(1, 5).round(0).astype(float)
    aca_deadline = (4 - gpa_factor * 1 + np.random.normal(0, 1, n)).clip(1, 5).round(0).astype(float)
    
    data = {
        'aca_program_suitability': aca_program,
        'aca_teaching_quality': aca_teaching,
        'aca_system_stability': aca_system,
        'aca_deadline_pressure': aca_deadline,
    }
    
    # Add missing values
    for col in data:
        missing_idx = np.random.choice(n, size=int(n * MISSING_PCT), replace=False)
        for idx in missing_idx:
            data[col][idx] = np.nan
    
    return data


def generate_environment(n):
    """Generate environment variables"""
    base_env = np.random.normal(
        CONFIG['distributions']['environment']['base_mean'],
        CONFIG['distributions']['environment']['base_std_dev'],
        n
    )
    
    data = {
        'env_facility_quality': (base_env + np.random.normal(0, 0.5, n)).clip(1, 5).round(0).astype(float),
        'env_service_satisfaction': (base_env + np.random.normal(0, 0.5, n)).clip(1, 5).round(0).astype(float),
        'env_dynamic_culture': (base_env + np.random.normal(0, 0.5, n)).clip(1, 5).round(0).astype(float),
    }
    
    # Add missing values
    for col in data:
        missing_idx = np.random.choice(n, size=int(n * MISSING_PCT), replace=False)
        for idx in missing_idx:
            data[col][idx] = np.nan
    
    return data


def generate_social(n, semester):
    """Generate social variables"""
    semester_factor = (semester - 5) / 4
    
    soc_peer = (3 + semester_factor * 1 + np.random.normal(0, 1, n)).clip(1, 5).round(0).astype(float)
    soc_community = (3 + np.random.normal(0, 1, n)).clip(1, 5).round(0).astype(float)
    soc_family = (3.5 - semester_factor * 0.5 + np.random.normal(0, 1, n)).clip(1, 5).round(0).astype(float)
    
    data = {
        'soc_peer_support': soc_peer,
        'soc_community_join': soc_community,
        'soc_family_support': soc_family,
    }
    
    # Add missing values
    for col in data:
        missing_idx = np.random.choice(n, size=int(n * MISSING_PCT), replace=False)
        for idx in missing_idx:
            data[col][idx] = np.nan
    
    return data


def generate_finance(n, residence, gpa):
    """Generate finance variables"""
    residence_factor = {
        "Trọ": 0,
        "Nhà": -0.3,
        "KTX": -0.5,
    }
    
    residence_scores = np.array([residence_factor[r] for r in residence])
    gpa_factor = (gpa - CONFIG['demographics']['gpa']['min']) / (CONFIG['demographics']['gpa']['max'] - CONFIG['demographics']['gpa']['min'])
    
    fin_tuition = (3.2 + np.random.normal(0, 1, n)).clip(1, 5).round(0).astype(float)
    fin_worry = (3.5 + residence_scores + np.random.normal(0, 1, n)).clip(1, 5).round(0).astype(float)
    fin_career = (3.2 + gpa_factor * 1.2 + np.random.normal(0, 0.8, n)).clip(1, 5).round(0).astype(float)
    
    data = {
        'fin_tuition_value': fin_tuition,
        'fin_living_cost_worry': fin_worry,
        'fin_career_confidence': fin_career,
    }
    
    # Add missing values
    for col in data:
        missing_idx = np.random.choice(n, size=int(n * MISSING_PCT), replace=False)
        for idx in missing_idx:
            data[col][idx] = np.nan
    
    return data


def generate_qc_data(n):
    """Generate QC trap data"""
    qc_trap = np.ones(n, dtype=int) * 2
    wrong_idx = np.random.choice(n, size=int(n * QC_TRAP_FAIL_PCT), replace=False)
    qc_trap[wrong_idx] = np.random.choice([1, 3, 4, 5], size=len(wrong_idx))
    return {'qc_trap_answer': qc_trap}


def generate_text(n):
    """Generate text data"""
    wishes = []
    for i in range(n):
        if np.random.rand() < SPAM_PCT:
            wishes.append(np.random.choice(SPAM_TEXTS))
        else:
            wishes.append(random.choice(WISHES))
    return {'text_student_wish': wishes}


def generate_dummy_data(n):
    """Main generation function"""
    print(f"🔄 Generating {n} records with data quality issues...\n")
    
    # Generate all data
    dem_data = generate_demographics(n)
    hap_data = generate_happiness(n, dem_data['dem_gpa'])
    aca_data = generate_academic(n, dem_data['dem_gpa'])
    env_data = generate_environment(n)
    soc_data = generate_social(n, dem_data['dem_semester'])
    fin_data = generate_finance(n, dem_data['dem_residence'], dem_data['dem_gpa'])
    qc_data = generate_qc_data(n)
    text_data = generate_text(n)
    
    # Combine
    all_data = {
        **dem_data, **hap_data, **aca_data, **env_data, 
        **soc_data, **fin_data, **qc_data, **text_data
    }
    
    # Create DataFrame
    column_order = [
        'dem_gender', 'dem_semester', 'dem_major', 'dem_residence', 'dem_gpa',
        'hap_overall_satisfaction', 'hap_daily_joy', 'hap_life_purpose', 'hap_loyalty_choice',
        'aca_program_suitability', 'aca_deadline_pressure', 'aca_teaching_quality', 'aca_system_stability',
        'env_facility_quality', 'env_service_satisfaction', 'env_dynamic_culture',
        'soc_peer_support', 'soc_community_join', 'soc_family_support',
        'fin_tuition_value', 'fin_living_cost_worry', 'fin_career_confidence',
        'qc_trap_answer', 'text_student_wish'
    ]
    
    df = pd.DataFrame(all_data)[column_order]
    
    # Add straight-liners
    print("  ✓ Adding Straight-Liners...")
    straightline_idx = np.random.choice(len(df), size=int(len(df) * STRAIGHTLINE_PCT), replace=False)
    straight_value = np.random.choice([1, 3, 5], size=len(straightline_idx))
    likert_cols = [col for col in df.columns if col.startswith(('hap_', 'aca_', 'env_', 'soc_', 'fin_'))]
    for i, idx in enumerate(straightline_idx):
        for col in likert_cols:
            df.loc[idx, col] = straight_value[i]
    
    # Add duplicates
    print("  ✓ Adding Duplicates...")
    dup_count = int(len(df) * DUPLICATE_PCT)
    if dup_count > 0:
        dup_idx = np.random.choice(len(df), size=dup_count, replace=False)
        duplicate_rows = df.iloc[dup_idx].copy()
        df = pd.concat([df, duplicate_rows], ignore_index=True)
    
    # Add extreme outliers
    print("  ✓ Adding Extreme Outliers...")
    outlier_idx = np.random.choice(len(df), size=int(len(df) * OUTLIER_PCT), replace=False)
    for idx in outlier_idx:
        for col in likert_cols:
            if np.random.rand() > 0.5:
                df.loc[idx, col] = np.random.choice(CONFIG['invalid_values']['invalid_gpa_values'])
    
    # Shuffle
    print("  ✓ Shuffling data...\n")
    df = df.sample(frac=1).reset_index(drop=True)
    
    return df


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("\n" + "="*80)
    print("🚀 DUMMY DATA GENERATOR - Team Shared Version")
    print("="*80)
    print(f"\nSeed: {SEED} (reproducible data)")
    print(f"Records: {NUM_RECORDS}")
    print(f"Config: {CONFIG_PATH}\n")
    
    try:
        # Generate data
        df = generate_dummy_data(NUM_RECORDS)
        
        # Ensure output directory exists
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        # Save
        df.to_csv(OUTPUT_PATH, index=False, encoding='utf-8')
        
        print("="*80)
        print("✅ SUCCESS - DATA GENERATED & SAVED")
        print("="*80)
        print(f"\nFile: {OUTPUT_PATH}")
        print(f"Records: {len(df)}")
        print(f"Columns: {len(df.columns)}")
        
        # Show quality issues
        print("\n" + "-"*80)
        print("📊 Data Quality Issues Summary")
        print("-"*80)
        
        missing = df.isnull().sum().sum()
        print(f"  • Missing Values: {missing}")
        
        trap_fail = df[df['qc_trap_answer'] != 2].shape[0]
        print(f"  • QC Trap Failures: {trap_fail} ({trap_fail/len(df)*100:.1f}%)")
        
        valid_majors = MAJORS
        invalid_major = df[~df['dem_major'].isin(valid_majors)].shape[0]
        print(f"  • Invalid Majors: {invalid_major}")
        
        spam = df[df['text_student_wish'].isin(SPAM_TEXTS)].shape[0]
        print(f"  • Spam Text: {spam}")
        
        dup = df.duplicated(subset=list(df.columns[:-1]), keep=False).sum()
        print(f"  • Potential Duplicates: {dup}")
        
        print("\n" + "="*80)
        print("✨ Data ready for team! Share with teammates for consistent testing")
        print("="*80 + "\n")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
