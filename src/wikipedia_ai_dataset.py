import os
import pandas as pd
import wikipediaapi
from groq import Groq

# 1. Configuration & Client Setup
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
wiki = wikipediaapi.Wikipedia('MindriftDataProject/1.0 (contact: omer@example.com)', 'en')

def get_wiki_summary(topic):
    """Fetches a concise summary from Wikipedia."""
    page = wiki.page(topic)
    if page.exists():
        return page.summary[:1500] # Limiting for efficiency
    return None

def generate_qa_pairs(context):
    """Uses LLM to create structured Q&A pairs for AI training."""
    prompt = f"Based on the following text, create 3 professional Question-Answer pairs for AI training. Format: Q: [Question] A: [Answer]\n\nText: {context}"
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile", # High-performance model
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # Target topics for a global dataset
    topics = ["Artificial Intelligence", "Quantum Computing", "Sustainable Energy", "SpaceX", "Deep Learning"]
    dataset = []

    print("🚀 Starting Global AI Dataset Generation...")
    for topic in topics:
        print(f"Processing: {topic}")
        summary = get_wiki_summary(topic)
        if summary:
            qa_data = generate_qa_pairs(summary)
            dataset.append({"topic": topic, "content": summary[:200] + "...", "ai_qa_pairs": qa_data})

    # Save as a structured CSV for LLM training
    df = pd.DataFrame(dataset)
    df.to_csv('global_knowledge_qa_dataset.csv', index=False)
    print("\n✅ Success! 'global_knowledge_qa_dataset.csv' created.")
