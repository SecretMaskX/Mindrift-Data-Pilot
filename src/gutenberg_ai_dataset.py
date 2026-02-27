import os, requests, pandas as pd
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def fetch_book_text(book_id):
    url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"
    response = requests.get(url)
    return response.text[5000:7000] # Kitabın ortasından bir kesit

def analyze_literary_style(text):
    prompt = f"Analyze the literary tone and sentiment of this text in 2 English sentences: {text}"
    completion = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
    return completion.choices[0].message.content

# Örnek: Sherlock Holmes (1661) ve Alice in Wonderland (11)
books = {"Sherlock_Holmes": "1661", "Alice_In_Wonderland": "11"}
data = []
for name, id in books.items():
    content = fetch_book_text(id)
    analysis = analyze_literary_style(content)
    data.append({"book": name, "analysis": analysis})

pd.DataFrame(data).to_csv('literary_analysis_dataset.csv', index=False)
print("✅ Gutenberg Dataset Ready!")
