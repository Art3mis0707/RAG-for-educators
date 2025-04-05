#!/usr/bin/env python
# send_emails.py

import pandas as pd
import numpy as np
import smtplib
from email.mime.text import MIMEText

#########################################
# STEP 1: Read and Clean Data from Excel
#########################################

# Read the Excel file.
import os
base_dir = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(base_dir, 'scores.xlsx')
df = pd.read_excel(excel_path)

print("=== Original Data ===")
print(df.head(10))

# Convert key columns to string and strip extra whitespace.
for col in ['Name', 'USN', 'Email']:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

# (Optional) Replace blank cells in key columns with a placeholder if needed.
# For numeric columns like the test scores, we replace empty strings with 0.
df = df.replace(r'^\s*$', 0, regex=True)
df = df.replace(np.nan, 0)

# Create a separate DataFrame for emails (unique rows)
df_emails = df[['Name', 'USN', 'Email']].drop_duplicates()
print("\n=== Email DataFrame (after cleaning) ===")
print(df_emails.head(10))

#########################################
# STEP 2: Process the Test Scores Data
#########################################

# List of columns with test scores. Make sure these match your Excel sheet.
test_cols = ['T1a', 'T1b', 'T2', 'T3a', 'T3b', 'T4a', 'T4b', 'T5a', 'T5b', 'Total-Test']
assessment_cols = test_cols[:-1]  # Exclude 'Total-Test' for assessment

# Convert all test columns to numeric (if they aren’t already)
for col in assessment_cols + ['Total-Test']:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# Define a mapping for topics for each assessment column.
topic_mapping = {
    'T1a': 'Regular Expression',
    'T1b': 'Epsilon NFA',
    'T2': 'Epsilon NFA and DFA equivalence',
    'T3a': 'Regular Expressions',
    'T3b': 'DFA Minimization',
    'T4a': 'Combining DFAs',
    'T4b': 'Decision Algorithms',
    'T5a': 'Pumping Lemma',
    'T5b': 'Epsilon DFA construction'
}

# Melt the DataFrame so that each row corresponds to one student's score on one question.
df_melted = df.melt(
    id_vars=['Name', 'USN', 'Email'],
    value_vars=assessment_cols,
    var_name='Question',
    value_name='Score'
)

# Map the topic names (optional: you can print to verify)
df_melted['Topic'] = df_melted['Question'].map(topic_mapping)

# Define maximum marks per question.
max_marks_dict = {
    'T1a': 6,
    'T1b': 4,
    'T2': 10,
    'T3a': 4,
    'T3b': 6,
    'T4a': 6,
    'T4b': 4,
    'T5a': 6,
    'T5b': 4
}
df_melted['MaxMarks'] = df_melted['Question'].map(max_marks_dict)

# Categorize performance based on score/max_marks.
def categorize_performance(row):
    score = row['Score']
    max_score = row['MaxMarks']
    if max_score == 0:
        return '0-25%'
    fraction = score / max_score
    if fraction < 0.25:
        return '0-25%'
    elif fraction < 0.50:
        return '25-50%'
    elif fraction < 0.75:
        return '50-75%'
    else:
        return '75-100%'

df_melted['Performance'] = df_melted.apply(categorize_performance, axis=1)

# Fill missing values if any (should already be numeric).
df_melted['Score'] = df_melted['Score'].fillna(0)
df_melted['MaxMarks'] = df_melted['MaxMarks'].fillna(1)

print("\n=== Melted DataFrame with Performance ===")
print(df_melted.head(10))

#########################################
# STEP 3: Map Study Materials and Create a Pivot Table
#########################################

# Define a dictionary of study materials based on performance.
materials_dict = {
    'T1a': {
        '0-25%':   "https://drive.google.com/file/d/1JmykSea-aeI1acrtXN4Zuw86BNccachg/view?usp=drive_link",
        '25-50%':  "https://drive.google.com/file/d/1Hpqz52LTxUIS5_oQi0j4OOYeeVM7w9Tt/view?usp=drive_link",
        '50-75%':  "https://drive.google.com/file/d/1vJNn4RYOcoA0G2YwnouIxVV89NSXdG9Y/view?usp=drive_link",
        '75-100%': "https://drive.google.com/file/d/1tu4jljojm4nH2BKYDg_ePST8rJ7Qjn8P/view?usp=drive_link"
    },
    'T1b': {
        '0-25%':   "https://drive.google.com/file/d/1PB6AfcStIP1EVCfOoZcpiUCJugrmZHQD/view?usp=drive_link",
        '25-50%':  "https://drive.google.com/file/d/19ZxklXB-MltUtA-Y6F52vTRD1rfp1_eB/view?usp=drive_link",
        '50-75%':  "https://drive.google.com/file/d/1WYq-stjp5dU3Z1rNigI-BBj0yKrZ2gXj/view?usp=drive_link",
        '75-100%': "https://drive.google.com/file/d/1tu4jljojm4nH2BKYDg_ePST8rJ7Qjn8P/view?usp=drive_link"
    },
    'T2': {
        '0-25%':   "https://drive.google.com/file/d/1tu4jljojm4nH2BKYDg_ePST8rJ7Qjn8P/view?usp=drive_link",
        '25-50%':  "https://drive.google.com/file/d/19ZxklXB-MltUtA-Y6F52vTRD1rfp1_eB/view?usp=drive_link",
        '50-75%':  "https://drive.google.com/file/d/1Hpqz52LTxUIS5_oQi0j4OOYeeVM7w9Tt/view?usp=drive_link",
        '75-100%': "https://drive.google.com/file/d/1Hpqz52LTxUIS5_oQi0j4OOYeeVM7w9Tt/view?usp=drive_link"
    },
    'T3a': {
        '0-25%':   "https://drive.google.com/file/d/1PB6AfcStIP1EVCfOoZcpiUCJugrmZHQD/view?usp=drive_link",
        '25-50%':  "https://drive.google.com/file/d/1Hpqz52LTxUIS5_oQi0j4OOYeeVM7w9Tt/view?usp=drive_link",
        '50-75%':  "https://drive.google.com/file/d/1PB6AfcStIP1EVCfOoZcpiUCJugrmZHQD/view?usp=drive_link",
        '75-100%': "https://drive.google.com/file/d/1Hpqz52LTxUIS5_oQi0j4OOYeeVM7w9Tt/view?usp=drive_link"
    },
    'T3b': {
        '0-25%':   "https://drive.google.com/file/d/19ZxklXB-MltUtA-Y6F52vTRD1rfp1_eB/view?usp=drive_link",
        '25-50%':  "https://drive.google.com/file/d/19ZxklXB-MltUtA-Y6F52vTRD1rfp1_eB/view?usp=drive_link",
        '50-75%':  "https://drive.google.com/file/d/1tu4jljojm4nH2BKYDg_ePST8rJ7Qjn8P/view?usp=drive_link",
        '75-100%': "https://drive.google.com/file/d/1tu4jljojm4nH2BKYDg_ePST8rJ7Qjn8P/view?usp=drive_link"
    },
    'T4a': {
        '0-25%':   "https://drive.google.com/file/d/1PB6AfcStIP1EVCfOoZcpiUCJugrmZHQD/view?usp=drive_link",
        '25-50%':  "https://drive.google.com/file/d/19ZxklXB-MltUtA-Y6F52vTRD1rfp1_eB/view?usp=drive_link",
        '50-75%':  "https://drive.google.com/file/d/1WYq-stjp5dU3Z1rNigI-BBj0yKrZ2gXj/view?usp=drive_link",
        '75-100%': "https://drive.google.com/file/d/1tu4jljojm4nH2BKYDg_ePST8rJ7Qjn8P/view?usp=drive_link"
    },
    'T4b': {
        '0-25%':   "https://drive.google.com/file/d/1tu4jljojm4nH2BKYDg_ePST8rJ7Qjn8P/view?usp=drive_link",
        '25-50%':  "https://drive.google.com/file/d/19ZxklXB-MltUtA-Y6F52vTRD1rfp1_eB/view?usp=drive_link",
        '50-75%':  "https://drive.google.com/file/d/1Hpqz52LTxUIS5_oQi0j4OOYeeVM7w9Tt/view?usp=drive_link",
        '75-100%': "https://drive.google.com/file/d/1Hpqz52LTxUIS5_oQi0j4OOYeeVM7w9Tt/view?usp=drive_link"
    },
    'T5a': {
        '0-25%':   "https://drive.google.com/file/d/1PB6AfcStIP1EVCfOoZcpiUCJugrmZHQD/view?usp=drive_link",
        '25-50%':  "https://drive.google.com/file/d/19ZxklXB-MltUtA-Y6F52vTRD1rfp1_eB/view?usp=drive_link",
        '50-75%':  "https://drive.google.com/file/d/1WYq-stjp5dU3Z1rNigI-BBj0yKrZ2gXj/view?usp=drive_link",
        '75-100%': "https://drive.google.com/file/d/1tu4jljojm4nH2BKYDg_ePST8rJ7Qjn8P/view?usp=drive_link"
    },
    'T5b': {
        '0-25%':   "https://drive.google.com/file/d/1tu4jljojm4nH2BKYDg_ePST8rJ7Qjn8P/view?usp=drive_link",
        '25-50%':  "https://drive.google.com/file/d/19ZxklXB-MltUtA-Y6F52vTRD1rfp1_eB/view?usp=drive_link",
        '50-75%':  "https://drive.google.com/file/d/1Hpqz52LTxUIS5_oQi0j4OOYeeVM7w9Tt/view?usp=drive_link",
        '75-100%': "https://drive.google.com/file/d/1Hpqz52LTxUIS5_oQi0j4OOYeeVM7w9Tt/view?usp=drive_link"
    }
}

def get_material(row):
    q = row['Question']
    perf = row['Performance']
    return materials_dict[q][perf]

df_melted['Material'] = df_melted.apply(get_material, axis=1)

# Create a pivot table: each student (by Name and USN) will have one row with study materials for each question.
df_student_material = df_melted.pivot_table(
    index=['Name', 'USN'],
    columns='Question',
    values='Material',
    aggfunc='first'
)

# Remove the column-level name and fill missing values.
df_student_material.columns.name = None
df_student_material = df_student_material.fillna('')

print("\n=== Pivoted DataFrame (Student-wise Materials) ===")
print(df_student_material.head(10))

#########################################
# STEP 4: Create Reports (Excel and HTML)
#########################################

# Write pivoted data to Excel and HTML for review.
df_student_material.to_excel("student_materials.xlsx", engine='openpyxl')
print("Excel report generated: student_materials.xlsx")

html_report = df_student_material.to_html()
with open("student_materials_report.html", "w") as f:
    f.write(html_report)
print("HTML report generated: student_materials_report.html")

#########################################
# STEP 5: Prepare Email Content
#########################################

# Reset index so that Name and USN become columns.
df_student_material = df_student_material.reset_index()

# Debug print: Check the data after resetting the index.
print("\n=== Pivoted DataFrame after resetting index ===")
print(df_student_material.head(10))

# Merge the email addresses from df_emails.
df_student_material = df_student_material.merge(df_emails, on=['Name', 'USN'], how='left')

# Debug print: Check that the merge includes the correct Email.
print("\n=== Final DataFrame with Emails ===")
print(df_student_material[['Name', 'USN', 'Email']].head(10))

def generate_email_content(row):
    """
    Generate personalized email content for a student.
    Expects the row to have 'Name', 'Email', and study material columns.
    """
    student_name = row['Name']
    email = row['Email']
    if pd.isna(email) or email == "0" or not email:
        print(f"Skipping student {student_name} due to missing email.")
        return None, None

    # Drop non-material columns to isolate study material columns.
    materials = row.drop(labels=['Name', 'USN', 'Email']).dropna()

    email_body = f"Subject: Study Materials for Your Test Performance 📚\n\n"
    email_body += f"Dear {student_name},\n\n"
    email_body += "Based on your test performance, here are study materials to help you improve:\n\n"

    for topic, material in materials.items():
        if material:  # Skip empty entries.
            email_body += f"- {topic}: {material}\n"

    email_body += "\nPlease review these materials to strengthen your understanding.\n\n"
    email_body += "Best regards,\n[Teacher Name]\n[Institution Name]\n"

    return email, email_body

# For testing, iterate until a row with a valid email is found.
sample_email, sample_body = None, None
for idx in df_student_material.index:
    sample_email, sample_body = generate_email_content(df_student_material.loc[idx])
    if sample_email is not None:
        break

print("\n=== Sample Email Content ===")
print(sample_body)

# Optionally, write the sample email content to a file.
with open("sample_email.txt", "w") as file:
    file.write(sample_body)

#########################################
# STEP 6: Send Email Using SMTP (Testing)
#########################################

# Configure your SMTP credentials.
EMAIL_SENDER = "maildummy049@gmail.com"
EMAIL_PASSWORD = ""  # Replace with your app-specific password if using Gmail.
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_email(to_email, email_body):
    """Send an email using SMTP."""
    msg = MIMEText(email_body)
    msg["Subject"] = "Study Materials for Your Test Performance 📚"
    msg["From"] = EMAIL_SENDER
    msg["To"] = to_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, to_email, msg.as_string())
        print(f"✅ Email sent successfully to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")

# For testing: send an email to a specific student. Adjust the index as needed.
# (For example, we try row index 61 if available.)
# For testing: iterate until a row with a valid email is found.
# Use row with index 61 for generating and sending the email.
if len(df_student_material) > 61:
    sample_email, sample_body = generate_email_content(df_student_material.iloc[61])
    print("\n=== Email Content for idx 61 ===")
    print(sample_body)
    if sample_email and sample_body:
        print("\nSending email using the data from idx 61...")
        send_email(sample_email, sample_body)
    else:
        print("Error: Email generation failed for idx 61.")
else:
    print("Not enough rows in DataFrame to access idx 61.")



