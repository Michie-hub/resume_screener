from scripts.preprocess import clean_text
from scripts.tfidf_matcher import rank_resumes
from scripts.utils import load_resumes, load_job_description
import pandas as pd

resumes, filenames = load_resumes("data/resumes/")
print(f"✅ Loaded resumes: {filenames}")
print(f"✅ Resume count: {len(resumes)}")

job_description = load_job_description("data/job_descriptions/jd.txt")
print(f"✅ Loaded Job Description: {job_description[:100]}...")  # Preview first 100 characters

#preprocess
cleaned_resumes = [clean_text(r) for r in resumes]
cleaned_jd = clean_text(job_description)
cleaned_resumes = []
valid_filenames = []

for resume, fname in zip(resumes, filenames):
    cleaned = clean_text(resume)
    if cleaned.strip():  # only keep if not empty
        cleaned_resumes.append(cleaned)
        valid_filenames.append(fname)

if len(cleaned_resumes) == 0:
    print("❌ All resumes were empty after cleaning. Exiting.")
    exit()


#check that we have resumes before ranking
if not cleaned_resumes:
  print("No resumes found. Please add .txt files to data/resumes/")
else:
    print(f"🧠 Resumes ready for ranking: {len(cleaned_resumes)}")
    print(f"📄 First resume preview: {cleaned_resumes[0][:100]}")


    #rank
    ranked = rank_resumes(cleaned_resumes, cleaned_jd)
    top_n = 5  # You can change this as needed
    ranked = ranked[:top_n]


    #export with filenames


    result_df = pd.DataFrame({ 
        "Filename" : valid_filenames,
        "SimilarityScore": [score for _, score in ranked]
    })
    #save to csv
    result_df.to_csv("output/ranked_resumes.csv", index=False)

    print("Ranked results saved to output/ranked_resumes.csv")
