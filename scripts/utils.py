import os
import fitz

def load_resumes(folder_path):
  resumes = []
  filenames = []

  for file in os.listdir(folder_path):
    full_path = os.path.join(folder_path, file)
    if file.endswith(".txt"):
      with open(full_path, "r", encoding="utf-8") as f:
                resumes.append(f.read())
                filenames.append(file)
    elif file.endswith(".pdf"):
      doc = fitz.open(full_path) 
      text = " ".join([page.get_text() for page in doc])  
      resumes.append(text)
      filenames.append(file)

  return resumes, filenames
    
def load_job_description(filepath):
  with open(filepath, "r", encoding="utf-8") as f:
    return f.read()
      
    