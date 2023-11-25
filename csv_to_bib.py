import pandas as pd
import re
import os

def extract_year(citation):
    if pd.isnull(citation):
        return ""
    matches = re.findall(r'\((\d{4})\)', citation)
    return matches[0] if matches else ""

def generate_bibtex_key(author, title, citation):
    if pd.isnull(author) and pd.isnull(title):
        return "unknown"
    
    first_author_last_name = (author.split(",")[0].split()[-1].lower() if not pd.isnull(author) else "noauthor").strip()
    title_part = (''.join(title.split()[:2]).lower() if not pd.isnull(title) else "notitle").strip()
    year = extract_year(citation)
    year = f"_{year}" if year != "nodate" else ""  # Append an underscore only if there's a year
    
    return f"{first_author_last_name}{title_part}{year}"

def format_bibtex(entry):
    author_value = "" if pd.isna(entry['author']) else entry['author']
    return f"{entry['entry_type']}{{{entry['entry_key']},\n" \
           f"    title = {{{entry['title']}}},\n" \
           f"    author = {{{author_value}}},\n" \
           f"    url = {{{entry['url']}}},\n" \
           f"    keywords = {{{entry['keywords']}}},\n" \
           f"    date = {{{entry['date']}}},\n" \
           f"    urldate = {{{entry['urldate']}}}\n" \
           f"}}\n\n"

def create_bib():
    # Ask the user for the input file path
    csvfile = input("Please enter the input CSV file path: ")
    
    try:
        data = pd.read_csv(csvfile, encoding='utf-8')
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return
    
    df = data
    #Rename the columns from Notion
    df.rename(columns={
        'Structural Framework': 'Collections', 
        'Topics': 'Tags', 
        'Resource Type': 'Item Type', 
        'Title':'Name',
        'Resource Name': 'Name', 
        'Authors': 'Authors', 
        'Link': 'URL', 
        'Citation (APA)': 'In-Text Citation', 
        'Full Citation':'In-Text Citation' 
    }, inplace=True)

    df['Tags'] = "notion" + ", " + df['Tags']
    df['Collections'] = df['Collections'].str.split(', ').tolist()
    df['Name'] = df['Name'].str.replace('“', '"').str.replace('”', '"').str.replace('’','\'').str.replace('—','-')
    df['Authors'] = df['Authors'].str.replace('&','and').str.replace('�and�','and')
    df['Authors'] = df['Authors'].str.replace(', ', ' and ')

    # Mapping the Resource Type to BibTeX entry type
    resource_type_mapping = {
        "article": "@article",
        "podcast": "@audio",
        "website": "@online",
        "primer": "@book",
        "video": "@video",
        "report": "@report",
        "book": "@book"
    }

    # Extract unique topics
    unique_topics = set(topic for sublist in df['Collections'] for topic in sublist)

    # For each unique topic, filter rows that contain that topic and save as BibTeX
    for topic in unique_topics:
        filtered_df = df[df['Collections'].apply(lambda x: topic in x)]

        # Create the BibTeX entries
        bibtex_entries = []

        for _, row in filtered_df.iterrows():
            entry_type = resource_type_mapping.get(row['Item Type'], "@misc")
            entry_key = generate_bibtex_key(row['Authors'], row['Name'].replace(',',''), row['In-Text Citation'])
            entry = {
                "entry_type": entry_type,
                "entry_key": entry_key,
                "title": row['Name'],
                "author": row['Authors'],
                "url": row['URL'],
                "keywords": row['Tags'],
                "date": extract_year(row['In-Text Citation']),
                "urldate": "2023-09-06"  # Current date or use datetime module to get current date
            }
            bibtex_entries.append(entry)

        # Generate the complete BibTeX output
        bibtex_output = ''.join([format_bibtex(entry) for entry in bibtex_entries])
        # Make sure the Collections directory exists
        os.makedirs("Collections", exist_ok=True)
        with open(f"Collections/{topic}.bib", "w", encoding='utf-8') as file:
            file.write(bibtex_output)

# Call the function
create_bib()
