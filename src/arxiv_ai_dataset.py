import os
import pandas as pd
import arxiv
from groq import Groq

# 1. Configuration & Client Setup
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def fetch_arxiv_papers(query):
    """Fetches the latest academic papers from ArXiv."""
    search = arxiv.Search(
        query=query,
        max_results=5,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    
    papers = []
    for result in search.results():
        papers.append({
            "title": result.title,
            "summary": result.summary,
            "url": result.pdf_url
        })
    return papers

def simplify_for_ai(text):
    """Uses LLM to simplify complex academic text for AI training."""
    prompt = f"Summarize this academic abstract in 3 simple bullet points for a high school student: {text}"
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        return completion.choices[0].message.content
    except Exception:
        return "Simplification failed."

if __name__ == "__main__":
    print("🔭 Fetching latest AI research from ArXiv...")
    research_list = fetch_arxiv_papers("Large Language Models")
    final_dataset = []

    for paper in research_list:
        print(f"Analyzing: {paper['title'][:40]}...")
        paper['ai_simplified_summary'] = simplify_for_ai(paper['summary'])
        final_dataset.append(paper)

    # Save as a structured academic dataset
    df = pd.DataFrame(final_dataset)
    df.to_csv('arxiv_ai_research_dataset.csv', index=False)
    print("\n✅ Success! 'arxiv_ai_research_dataset.csv' created.")
