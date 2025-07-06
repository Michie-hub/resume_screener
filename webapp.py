from flask import Flask, render_template, request
import os
from scripts.utils import load_resumes, load_job_description
from scripts.preprocess import clean_text
from scripts.tfidf_matcher import rank_resumes
import pandas as pd
import fitz

app = Flask(__name__)
UPLOAD_FOLDER = "data/resumes/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    jd_text = ""

    JD_FOLDER = "data/job_descriptions/"
    RESUME_FOLDER = "data/resumes/"
    os.makedirs(JD_FOLDER, exist_ok=True)
    os.makedirs(RESUME_FOLDER, exist_ok=True)

    if request.method == "POST":
        # Handle job description input
        jd_file = request.files.get("jdfile")
        jd_select = request.form.get("jdselect")
        jd_textarea = request.form.get("jobdesc")

        if jd_file and jd_file.filename.endswith(".txt"):
            jd_path = os.path.join(JD_FOLDER, jd_file.filename)
            jd_file.save(jd_path)
            jd_text = load_job_description(jd_path)
        elif jd_select:
            jd_text = load_job_description(os.path.join(JD_FOLDER, jd_select))
        elif jd_textarea:
            jd_text = jd_textarea.strip()

        if not jd_text.strip():
            return render_template("index.html", results=[], error="❌ No job description provided.")

        # Handle resume uploads
        uploaded_files = request.files.getlist("resumes")
        for f in uploaded_files:
          if f.filename:  # skip empty uploads
             save_path = os.path.join(UPLOAD_FOLDER, f.filename)
             f.save(save_path)


        selected_existing_resumes = request.form.getlist("existing_resumes")

        resumes = []
        filenames = []

        # Load uploaded + selected resumes
        all_files = uploaded_files + selected_existing_resumes
        for file in os.listdir(RESUME_FOLDER):
            if file in [f.filename for f in uploaded_files] or file in selected_existing_resumes:
                full_path = os.path.join(RESUME_FOLDER, file)
                if file.endswith(".txt"):
                    with open(full_path, "r", encoding="utf-8") as f:
                        resumes.append(f.read())
                        filenames.append(file)
                elif file.endswith(".pdf"):
                    doc = fitz.open(full_path)
                    text = " ".join([page.get_text() for page in doc])
                    resumes.append(text)
                    filenames.append(file)

        cleaned_resumes = [clean_text(r) for r in resumes if r.strip()]
        cleaned_jd = clean_text(jd_text)

        if cleaned_resumes:
            ranked = rank_resumes(cleaned_resumes, cleaned_jd, filenames)[:5]
            results = ranked

    # Populate dropdowns
    jd_files = [f for f in os.listdir(JD_FOLDER) if f.endswith(".txt")]
    existing_resumes = [f for f in os.listdir(RESUME_FOLDER) if f.endswith((".txt", ".pdf"))]

    return render_template("index.html", results=results, jd_files=jd_files, existing_resumes=existing_resumes)



if __name__ == "__main__":
  app.run(debug=True)



