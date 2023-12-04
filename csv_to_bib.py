import pandas as pd
import re
import os
import numpy as np

def flatten_list(nested):
  flat = []

  for l in nested:
    if isinstance(l, list):
        flat.extend(l)
    else:
        flat.append(l)
    
  return(flat)


def extract_year(citation):
    if pd.isnull(citation):
        return ""
    matches = re.findall(r'\((\d{4})\)', citation)
    return matches[0] if matches else ""

def format_title(row):
    if row['Resource Type'] != 'podcast':
        return row.Name
    else:
        if 'Podcast' in row.Authors:
            new_title = row.Authors.split(' Podcast')[0] + ': ' + row.Name

            if 'WhaZhaZi' in row.Authors:
                new_title = new_title + " with Thosh Collins (WhaZhaZi, Haudenosaunee and O'otham) and Chelsea Luger (Anishinaabe and Lakota)."

        elif 'podcast' in row.Authors: 
            new_subtitle = row.Name.split('Episode')[1]
            new_title = row.Authors.split(' podcast')[0] + new_subtitle
        elif 'Adriana Alejandre' in row.Authors:
            new_title = 'Latinx Therapy: ' + row.Name
        else:
            new_title = row.Name

        return new_title


def format_authors(row, orgs):

    authors =  row['Authors']

    if row['Resource Type'] != 'podcast':
        
        if authors not in orgs:
            authors = authors.replace(', LMFT', '')
            authors = authors.replace('&','and').replace('�and�','and')
            authors = authors.replace(', and ', ' and ')
            authors = authors.replace(', ', ' and ')

    else:
       authors = authors.replace(' podcast', '').replace(', LMFT', '')

       if 'All My Relations' in authors:
           authors = 'Wilbur, Matika and Keene, Adrienne'

    
    return authors 

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

    if entry['is_org']:
        bibtex_item = f"{entry['entry_type']}{{{entry['entry_key']},\n" \
           f"    title = { {{entry['title']}} },\n" \
           f"    author = { {{ {{author_value}} }} },\n" \
           f"    url = { {{entry['url']}} },\n" \
           f"    keywords = { {{entry['keywords']}} },\n" \
           f"    date = { {{entry['date']}} },\n" \
           f"    urldate = { {{entry['urldate']}} }\n" \
           f"}}\n\n"
        
    else:
        bibtex_item = f"{entry['entry_type']}{{{entry['entry_key']},\n" \
           f"    title = { {{entry['title']}} },\n" \
           f"    author = { {{author_value}} },\n" \
           f"    url = { {{entry['url']}} },\n" \
           f"    keywords = { {{entry['keywords']}} },\n" \
           f"    date = { {{entry['date']}} },\n" \
           f"    urldate = { {{entry['urldate']}} }\n" \
           f"}}\n\n"

    return bibtex_item

def create_bib(organizations):

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
    df['Name'] = df['Name'].apply(format_title, axis=1)
    
    df['Authors'] = df['Authors'].apply(format_authors, axis=1, args=(orgs))

    df['is_org'] = np.where(df['Authors'] in orgs, True, False)

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
                "urldate": "2023-09-06",  # Current date or use datetime module to get current date
                "is_org":  row['is_org']
            }
            bibtex_entries.append(entry)

        # Generate the complete BibTeX output
        bibtex_output = ''.join([format_bibtex(entry) for entry in bibtex_entries])
        # Make sure the Collections directory exists
        os.makedirs("Collections", exist_ok=True)
        with open(f"Collections/{topic}.bib", "w", encoding='utf-8') as file:
            file.write(bibtex_output)

# Call the function
# data/FHJCDatabaseShared.csv

# Authors with a name that does not fall into the First Name Last Name pattern.
# They don't have to be an organization but most of them are.
orgs = ['Sins Invalid', 'Anti-Eviction Mapping Project (AEMP)', 
        'We the Unhoused', 'National Partnership for Women and Families',
        'National Harm Reduction Coalition', 'The Drug Policy Alliance',
        'Addressing Racism Review Summary Report',
        'Reflections: A Journal of Community-Engaged Writing & Rhetoric']

create_bib(orgs)
