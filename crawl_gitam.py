import os
from dotenv import load_dotenv
from firecrawl import Firecrawl

# Load secrets from .env file
load_dotenv()
FIRE_KEY = os.getenv("fc-abb44575ebe84391a1748f552e67cfa8")

# Initialize with the secret key
app = Firecrawl(api_key=FIRE_KEY)

print("Starting to crawl GITAM... please wait.")

# Run the crawl (v1 flat style)
crawl_result = app.crawl(
    url='https://www.gitam.edu',
    limit=5,
    scrape_options={'formats': ['markdown']}
)

# Save results to knowledge base
with open("gitam_data.md", "w", encoding="utf-8") as f:
    if isinstance(crawl_result, (list, tuple)):
        for doc in crawl_result:
            source = getattr(doc, 'metadata', {}).get('sourceURL', 'Unknown')
            content = getattr(doc, 'markdown', '')
            f.write(f"--- SOURCE: {source} ---\n{content}\n\n")

print("SUCCESS! 'gitam_data.md' is ready.")