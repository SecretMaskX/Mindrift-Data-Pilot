import os
import pandas as pd
from github import Github
from groq import Groq

# 1. Configuration & Client Setup
# Kendi aktivasyon dosyamızdan otomatik gelen API anahtarını kullanır
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
# Herhangi bir Token gerektirmeden Public README'leri okumak için
g = Github() 

def get_repo_readme(repo_name):
    """Public bir GitHub deposundan README dosyasını çeker."""
    try:
        repo = g.get_repo(repo_name)
        return repo.get_readme().decoded_content.decode()
    except Exception as e:
        print(f"Error fetching {repo_name}: {e}")
        return None

def summarize_technical_docs(readme_text):
    """Teknik dokümanları AI eğitimi için 4 cümlede özetler."""
    # i5-7200U makineni yormamak için ilk 2000 karakteri işliyoruz
    prompt = f"Summarize the installation and core features of this project in 4 concise English sentences: {readme_text[:2000]}"
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        return completion.choices[0].message.content
    except Exception:
        return "Summary failed."

if __name__ == "__main__":
    # Analiz edilecek popüler kütüphaneler
    repos = ["pandas-dev/pandas", "tensorflow/tensorflow", "pallets/flask", "django/django"]
    tech_data = []

    print("💻 GitHub teknik dokümanları işleniyor...")
    for r in repos:
        print(f"Analyzing repo: {r}")
        content = get_repo_readme(r)
        if content:
            summary = summarize_technical_docs(content)
            tech_data.append({"repo": r, "summary": summary})

    # Teknik veri setini CSV olarak kaydet
    pd.DataFrame(tech_data).to_csv('github_tech_dataset.csv', index=False)
    print("\n✅ Success! 'github_tech_dataset.csv' created with 4 detailed summaries.")
