import streamlit as st
import pandas as pd
import tempfile
import os
import json
from text_extraction import extract_text_from_pdf, extract_text_from_docx
from preprocessing import preprocess_text
from vectorization import vectorize_texts, calculate_similarity
from scoring import normalize_scores, assign_tier
from pros_cons import extract_pros_cons

st.set_page_config(page_title="AI Resume Ranker", layout="wide")
st.title("AI Resume Ranker")
st.write("Upload resumes and a job description. Get ranked candidates with AI-powered analysis!")

# --- Upload job description ---
st.header("1. Upload Job Description")
jd_file = st.file_uploader("Upload Job Description (TXT, DOCX, or paste below)", type=["txt", "docx"], key="jd")
jd_text = ""
if jd_file:
    if jd_file.name.endswith(".txt"):
        jd_text = jd_file.read().decode("utf-8")
    elif jd_file.name.endswith(".docx"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(jd_file.read())
            tmp_path = tmp.name
        jd_text = extract_text_from_docx(tmp_path)
        os.unlink(tmp_path)
else:
    jd_text = st.text_area("Or paste job description here:")

# --- Upload resumes ---
st.header("2. Upload Resumes (PDF, DOCX, or TXT)")
resume_files = st.file_uploader("Upload one or more resumes", type=["pdf", "docx", "txt"], accept_multiple_files=True)

# --- Process and Rank ---
if st.button("Run AI Ranking") and jd_text and resume_files:
    st.info("Processing resumes...")
    candidates = []
    jd_processed = preprocess_text(jd_text)
    for file in resume_files:
        # Extract text
        if file.name.endswith(".pdf"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(file.read())
                tmp_path = tmp.name
            resume_text = extract_text_from_pdf(tmp_path)
            os.unlink(tmp_path)
        elif file.name.endswith(".docx"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                tmp.write(file.read())
                tmp_path = tmp.name
            resume_text = extract_text_from_docx(tmp_path)
            os.unlink(tmp_path)
        elif file.name.endswith(".txt"):
            resume_text = file.read().decode("utf-8")
        else:
            continue
        resume_processed = preprocess_text(resume_text)
        # Extract candidate info (simple extraction)
        lines = resume_text.splitlines()
        name = lines[0].strip() if lines else file.name
        email = next((l for l in lines if "@" in l), "unknown@email.com")
        # Vectorize and score
        tfidf_matrix = vectorize_texts([jd_processed, resume_processed])
        similarity = calculate_similarity(tfidf_matrix)
        score = normalize_scores(similarity)
        tier = assign_tier(score)
        pros, cons = extract_pros_cons(resume_text, jd_text)
        candidates.append({
            "name": name,
            "email": email,
            "score": score,
            "tier": tier,
            "pros": pros,
            "cons": cons
        })
    # Sort and display
    candidates.sort(key=lambda x: x["score"], reverse=True)
    df = pd.DataFrame(candidates)
    st.header("3. Results")
    st.dataframe(df[["name", "email", "score", "tier"]], use_container_width=True)
    for c in candidates:
        with st.expander(f"{c['name']} ({c['tier']}, Score: {c['score']})"):
            st.markdown(f"**Email:** {c['email']}")
            st.markdown(f"**Pros:**\n- " + "\n- ".join(c['pros']))
            st.markdown(f"**Cons:**\n- " + "\n- ".join(c['cons']))

    # --- Download options ---
    st.header("4. Download Results")
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("Download as JSON", data=json.dumps(candidates, indent=2), file_name="candidate_rankings.json", mime="application/json")
    with col2:
        csv = df.to_csv(index=False)
        st.download_button("Download as CSV", data=csv, file_name="candidate_rankings.csv", mime="text/csv")
else:
    st.warning("Please upload a job description and at least one resume.") 