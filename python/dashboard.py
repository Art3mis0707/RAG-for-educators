import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
import re

# Load data
file_path = "scores.xlsx"  # Update this if running locally

# Read Excel file
df = pd.read_excel(file_path, sheet_name=None, engine="openpyxl")
sheet_name = list(df.keys())[0]  # Automatically pick the first sheet
df = df[sheet_name]

# Ensure correct column names (trim spaces and check case sensitivity)
df.columns = df.columns.str.strip()

# Check if expected columns exist
expected_columns = ["Name", "USN", "Total-Test"]
test_cols = [col for col in df.columns if col.startswith("T")]  # Extract all test columns

for col in expected_columns:
    if col not in df.columns:
        raise KeyError(f"Missing expected column: {col}")

# Clean data: Replace empty strings/NaN with 0 in test columns
df[test_cols] = df[test_cols].replace(r'^\s*$', 0, regex=True).fillna(0).astype(float)
df['Total-Test'] = df['Total-Test'].replace(r'^\s*$', 0, regex=True).fillna(0).astype(float)

# Streamlit Styling
st.set_page_config(page_title="Student Score Dashboard", layout="wide", initial_sidebar_state="expanded")

# Background and title styling with updated sidebar widget styles
st.markdown(
    """
    <style>
    .stApp {
        background-color: #121212;
        font-family: 'Roboto', sans-serif;
    }
    h1 {
        color: #FFFFFF !important;
        font-size: 48px;
        font-weight: 700;
        text-align: center;
        margin-top: 20px;
    }
    .stButton>button {
        background-color: #F79C42;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #e6892f;
    }
    .sidebar .sidebar-content {
        background-color: #2F3A58;
        color: white;
        padding: 10px;
    }
    .stDataFrame table {
        font-family: 'Arial', sans-serif;
        font-size: 14px;
        color: #FFFFFF;
        border: none;
    }
    .stDataFrame table th {
        background-color: #4C72B0;
        color: white;
        padding: 10px;
    }
    /* Updated slider style with black background */
    .stSlider>div>div>div>div {
        background-color: #000000;
    }
    /* Updated selectbox style with black background and white text */
    .stSelectbox, .stSlider {
        background-color: #000000;
        border-radius: 6px;
        padding: 10px;
    }
    .stSelectbox select {
        color: #FFFFFF;
        font-weight: 600;
        background-color: #000000;
    }
    .card {
        background-color: #1E1E1E;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease-in-out;
    }
    .card:hover {
        transform: scale(1.03);
    }
    .stPlotlyChart {
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True
)

# Title
st.title("Student Score Dashboard")

# Sidebar filters with vibrant design
st.sidebar.header("Filter Options")

# Filter by score range first
score_range = st.sidebar.slider("Total Score Range", int(df["Total-Test"].min()), int(df["Total-Test"].max()), 
                                (int(df["Total-Test"].min()), int(df["Total-Test"].max())))

# Filter the dataframe based on score range
filtered_df = df[(df["Total-Test"] >= score_range[0]) & (df["Total-Test"] <= score_range[1])]

# Dynamically update the student list in the dropdown based on the filtered data
selected_student = st.sidebar.selectbox("Select Student", ["All"] + filtered_df["Name"].tolist(), index=0)

# Apply additional filter based on selected student (if not "All")
if selected_student != "All":
    filtered_df = filtered_df[filtered_df["Name"] == selected_student]

# Chatbot functionality
st.sidebar.header("Ask the Chatbot")
user_query = st.sidebar.text_input("Ask me something:", "")

def get_student_info(query):
    # Normalize both the query and the dataframe for case and whitespace issues
    query = query.strip().lower()

    # Pattern to match "student score of <USN>"
    score_match = re.search(r"student score of (\S+)", query)
    # Pattern to match "student name of <USN>"
    name_match = re.search(r"student name of (\S+)", query)

    # If the query is asking for the score
    if score_match:
        usn = score_match.group(1).strip().lower()  # Convert USN to lowercase
        student_data = df[df["USN"].str.strip().str.lower() == usn]
        
        if not student_data.empty:
            score = student_data["Total-Test"].values[0]
            return f"The score of student {usn.upper()} is {score}."
        else:
            return f"Student with USN {usn.upper()} not found."
    
    # If the query is asking for the name
    elif name_match:
        usn = name_match.group(1).strip().lower()  # Convert USN to lowercase
        student_data = df[df["USN"].str.strip().str.lower() == usn]
        
        if not student_data.empty:
            name = student_data["Name"].values[0]
            return f"The name of student with USN {usn.upper()} is {name}."
        else:
            return f"Student with USN {usn.upper()} not found."
    
    return "I didn't understand the question. Please ask again."

# Display chatbot response based on query
if user_query:
    response = get_student_info(user_query)
    st.sidebar.write(response)

# Display filtered table in a stylish card
with st.container():
    st.markdown('<h2 style="color: white; font-size: 36px; font-weight: 700;">Student Scores</h2>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.dataframe(filtered_df.style.set_properties(**{'text-align': 'center'}))
    st.markdown('</div>', unsafe_allow_html=True)

# Matplotlib Plot: Distribution of Total Test Scores
plt.figure(figsize=(10, 6))
sns.histplot(df['Total-Test'], bins=15, kde=True, color='skyblue')
plt.title('Distribution of Total Test Scores')
plt.xlabel('Total Test Score')
plt.ylabel('Number of Students')
st.pyplot(plt)

# Matplotlib Plot: Score Distribution per Test Section (Boxplot)
df_melted = df.melt(
    id_vars=['Name', 'USN'], 
    value_vars=test_cols, 
    var_name='Test Section', 
    value_name='Score'
)
plt.figure(figsize=(12, 6))
sns.boxplot(x='Test Section', y='Score', data=df_melted, palette='Set2')
plt.xticks(rotation=45, ha='right')
plt.title('Score Distribution Across Test Sections')
plt.xlabel('Test Section')
plt.ylabel('Score')
st.pyplot(plt)

# Plotly Chart: Total Test Scores Bar Chart (Interactive)
total_score_chart = px.bar(filtered_df, x="Name", y="Total-Test", title="Student Test Scores", labels={"Total-Test": "Score", "Name": "Student"})
total_score_chart.update_layout(
    title_font_size=24,
    title_font_family="Roboto, sans-serif",
    title_font_color="#4C72B0",
    xaxis_title_font_size=16,
    yaxis_title_font_size=16,
    xaxis_tickangle=-45,
    plot_bgcolor="#121212",  # Dark background for the plot
    paper_bgcolor="#121212",  # Dark background for the plot
    font=dict(color="#FFFFFF"),  # White text for contrast
    showlegend=False  # Hide the legend if it's not required
)
st.plotly_chart(total_score_chart, use_container_width=True)

# Plotly Chart: Average Score per Question (Interactive)
question_scores = df[test_cols].mean().reset_index()
question_scores.columns = ["Question", "Average Score"]
question_chart = px.bar(question_scores, x="Question", y="Average Score", title="Average Score per Question", labels={"Average Score": "Score", "Question": "Test Question"})
question_chart.update_layout(
    title_font_size=24,
    title_font_family="Roboto, sans-serif",
    title_font_color="#4C72B0",
    xaxis_title_font_size=16,
    yaxis_title_font_size=16,
    plot_bgcolor="#121212",  # Dark background for the plot
    paper_bgcolor="#121212",  # Dark background for the plot
    font=dict(color="#FFFFFF")  # White text for contrast
)
st.plotly_chart(question_chart, use_container_width=True)

# Additional Visualizations (Matplotlib Heatmaps)
# Correlation Heatmap Between Test Sections
plt.figure(figsize=(10, 8))
corr_matrix = df[test_cols].corr()
sns.heatmap(
    corr_matrix, 
    annot=True, 
    cmap='coolwarm', 
    vmin=-1, 
    vmax=1, 
    fmt=".2f", 
    linewidths=0.5
)
plt.title('Correlation Between Test Sections')
st.pyplot(plt)

# Top 20 Students Performance Heatmap
top_students = df.sort_values('Total-Test', ascending=False).head(20)
plt.figure(figsize=(15, 10))
sns.heatmap(
    top_students.set_index('Name')[test_cols], 
    annot=True, 
    cmap='YlGnBu', 
    fmt=".1f", 
    linewidths=0.5
)
plt.title('Test Section Scores for Top 20 Students')
plt.xlabel('Test Section')
plt.ylabel('Student Name')
st.pyplot(plt)
