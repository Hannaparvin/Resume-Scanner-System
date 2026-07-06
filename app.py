import streamlit as st
import pandas as pd

from parser import extract_text_from_pdf

from skills import (
    extract_experience,
    preprocess_text,
    extract_entities
)

from matcher import calculate_match_score


# PAGE CONFIG
st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="",
    layout="wide"
)


# CUSTOM CSS
st.markdown("""
<style>

.main {
    background-color: #0f172a;
    color: white;
}

h1 {
    color: white;
    font-size: 52px !important;
    font-weight: 800 !important;
}

h2, h3 {
    color: white;
}

.stButton>button {

    background: linear-gradient(
        90deg,
        #6366f1,
        #8b5cf6
    );

    color: white;

    border-radius: 12px;

    border: none;

    padding: 10px 25px;

    font-weight: bold;
}

.stTextInput>div>div>input {

    background-color: #1e293b;

    color: white;
}

.stTextArea textarea {

    background-color: #1e293b;

    color: white;
}

.stNumberInput input {

    background-color: #1e293b;

    color: white;
}

.card {

    background: #1e293b;

    padding: 25px;

    border-radius: 20px;

    margin-bottom: 20px;

    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
}

.skill-box {

    display: inline-block;

    padding: 8px 14px;

    margin: 5px;

    border-radius: 10px;

    color: white;

    font-size: 14px;
}

.matched-skill {

    background-color: #10b981;
}

.missing-skill {

    background-color: #ef4444;
}

</style>
""", unsafe_allow_html=True)


# HEADER
st.markdown("""
<h1>
    Resume Screening System
</h1>
""", unsafe_allow_html=True)


# SIDEBAR
st.sidebar.title(" Job Description")


job_title = st.sidebar.text_input(
    "Job Title"
)


required_skills_input = st.sidebar.text_area(
    "Required Skills (comma separated)",
    height=150
)


required_experience = st.sidebar.number_input(
    "Minimum Experience (Years)",
    min_value=0,
    max_value=20,
    value=1
)


uploaded_files = st.file_uploader(
    "Upload Resumes (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)


# MAIN LOGIC
if uploaded_files and required_skills_input:

    required_skills = [

        skill.strip().lower()

        for skill in required_skills_input.split(",")

        if skill.strip()
    ]

    all_results = []

    st.markdown("## 📊 Screening Results")


    for uploaded_file in uploaded_files:

        # EXTRACT TEXT
        text = extract_text_from_pdf(uploaded_file)

        if text.strip() == "":

            st.warning(
                f"Could not process {uploaded_file.name}"
            )

            continue


        # NLP PREPROCESSING
        clean_text = preprocess_text(text)


        # EXPERIENCE EXTRACTION
        candidate_experience = extract_experience(
            clean_text
        )


        # ENTITY EXTRACTION
        entities = extract_entities(clean_text)


        # MATCH SCORE
        result = calculate_match_score(

            clean_text,

            required_skills,

            candidate_experience,

            required_experience
        )


        candidate_data = {

            "Candidate Name": uploaded_file.name,

            "Experience": candidate_experience,

            "Matched Skills":
                result["matched_skills"],

            "Missing Skills":
                result["missing_skills"],

            "ATS Score": result["score"],

            "Entities": entities
        }

        all_results.append(candidate_data)


    # DATAFRAME
    results_df = pd.DataFrame(all_results)


    if not results_df.empty:

        # SORT BY SCORE
        results_df = results_df.sort_values(
            by="ATS Score",
            ascending=False
        )


        # METRICS
        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total Candidates",
                len(results_df)
            )

        with col2:

            st.metric(
                "Top ATS Score",
                f"{results_df['ATS Score'].max()}%"
            )

        with col3:

            st.metric(
                "Average Score",
                f"{round(results_df['ATS Score'].mean(), 2)}%"
            )


        st.markdown("---")


        # CANDIDATE CARDS
        for index, row in results_df.iterrows():

            st.markdown(
                f"""
                <div class="card">

                <h3>
                👤 {row['Candidate Name']}
                </h3>

                <p>
                <b>Experience:</b>
                {row['Experience']} years
                </p>

                <p>
                <b>ATS Score:</b>
                {row['ATS Score']}%
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )


            # PROGRESS BAR
            st.progress(
                int(row["ATS Score"])
            )


            # MATCHED SKILLS
            st.write("### ✅ Matched Skills")

            matched_html = ""

            for skill in row["Matched Skills"]:

                matched_html += f"""
                <span class="skill-box matched-skill">
                {skill}
                </span>
                """

            st.markdown(
                matched_html,
                unsafe_allow_html=True
            )


            # MISSING SKILLS
            st.write("### ❌ Missing Skills")

            missing_html = ""

            for skill in row["Missing Skills"]:

                missing_html += f"""
                <span class="skill-box missing-skill">
                {skill}
                </span>
                """

            st.markdown(
                missing_html,
                unsafe_allow_html=True
            )

            st.markdown("<br>", unsafe_allow_html=True)


else:

    st.info(
        "Upload resumes and enter job requirements."
    )