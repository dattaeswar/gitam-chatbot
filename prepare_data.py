import os

def prepare_chunks(file_path):
    if not os.path.exists(file_path):
        print("Error: gitam_data.md not found!")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # We split by '--- SOURCE', which is how your crawler separated pages
    pages = content.split("--- SOURCE")
    
    print(f"Original file size: {len(content) / 1024:.2f} KB")
    print(f"Found {len(pages)} individual sections.")

    # Save these as small chunks so we can upload them later
    with open("gitam_chunks.txt", "w", encoding="utf-8") as f:
        for i, page in enumerate(pages):
            if page.strip():
                # Clean up the text a bit
                clean_page = page.strip()
                f.write(f"CHUNK_{i}\n{clean_page}\nEND_CHUNK\n")
    
    print("Success! Created 'gitam_chunks.txt'. This is ready for Pinecone.")

prepare_chunks("gitam_data.md")