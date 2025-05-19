import os
import json
import pandas as pd
from text_extraction import extract_text_from_pdf, extract_text_from_docx
from preprocessing import preprocess_text
from vectorization import vectorize_texts, calculate_similarity
from scoring import normalize_scores, assign_tier
from pros_cons import extract_pros_cons


def main():
    # Configuration
    resume_dir = 'resumes'  # Directory containing resume files
    job_desc_file = 'job_description.txt'  # Job description file
    output_file = 'candidate_rankings.json'  # Output JSON file

    # Load job description
    with open(job_desc_file, 'r') as f:
        job_desc = f.read()

    # Preprocess job description
    job_desc_processed = preprocess_text(job_desc)

    # Initialize list to store candidate data
    candidates = []

    # Process each resume file
    for filename in os.listdir(resume_dir):
        file_path = os.path.join(resume_dir, filename)
        if filename.endswith('.pdf'):
            resume_text = extract_text_from_pdf(file_path)
        elif filename.endswith('.docx'):
            resume_text = extract_text_from_docx(file_path)
        else:
            continue

        # Preprocess resume text
        resume_processed = preprocess_text(resume_text)

        # Extract candidate info (name, email) - placeholder for now
        candidate_info = {'name': filename, 'email': 'candidate@email.com'}

        # Vectorize texts and calculate similarity
        tfidf_matrix = vectorize_texts([job_desc_processed, resume_processed])
        similarity = calculate_similarity(tfidf_matrix)

        # Normalize score to 0-100
        score = normalize_scores(similarity)

        # Assign tier
        tier = assign_tier(score)

        # Extract pros and cons
        pros, cons = extract_pros_cons(resume_text, job_desc)

        # Append candidate data
        candidate_data = {
            'name': candidate_info['name'],
            'email': candidate_info['email'],
            'score': score,
            'tier': tier,
            'pros': pros,
            'cons': cons
        }
        candidates.append(candidate_data)

    # Sort candidates by score (descending)
    candidates.sort(key=lambda x: x['score'], reverse=True)

    # Write results to JSON file
    with open(output_file, 'w') as f:
        json.dump(candidates, f, indent=2)

    print(f'Results written to {output_file}')


if __name__ == '__main__':
    main() 