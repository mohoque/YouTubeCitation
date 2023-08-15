import streamlit as st
import requests
from bs4 import BeautifulSoup

def get_youtube_citation(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract video details
    video_title = soup.find("meta", {"property": "og:title"})["content"]
    channel_name = soup.find("link", {"itemprop": "name"})["content"]
    publication_date = soup.find("meta", {"itemprop": "datePublished"})["content"]
    
    # Extract year from publication date
    year = publication_date.split('-')[0]
    
    # Use channel name as author if available, otherwise use 'Anonymous'
    author_name = channel_name if channel_name else "Anonymous"
    
    # Create citation
    citation = f"{author_name}. ({year}). {video_title}. {channel_name}. Published on {publication_date}. YouTube. {url}"
    return citation

def get_youtube_citation_ris(citation, url, author_name, year, video_title, publication_date):
    # Create RIS content based on the provided citation details
    ris_content = f"""
TY  - VIDEO
AU  - {author_name}
PY  - {year}
TI  - {video_title}
UR  - {url}
DA  - {publication_date}
PB  - YouTube
KW  - YouTube Video
ER  - 
"""
    return ris_content.strip()

# Streamlit app interface
st.title("YouTube Citation Generator")

# Input URL
url = st.text_input("Enter YouTube Video URL:")

if url:
    try:
        citation = get_youtube_citation(url)
        st.write("Citation:", citation)

        # Extract details from the citation for RIS format
        author_name, year, video_title, publication_date = citation.split('.')[0], citation.split('.')[1].split('(')[1].split(')')[0], citation.split('.')[2].strip(), citation.split('Published on ')[1].split('.')[0]
        ris_content = get_youtube_citation_ris(citation, url, author_name, year, video_title, publication_date)

        # Option to download RIS format
        if st.button("Download RIS Format"):
            # Extract details from the citation for RIS format
            author_name, year, video_title, publication_date = citation.split('.')[0], citation.split('.')[1].split('(')[1].split(')')[0], citation.split('.')[2].strip(), citation.split('Published on ')[1].split('.')[0]
            ris_content = get_youtube_citation_ris(citation, url, author_name, year, video_title, publication_date)
    
            st.download_button("Download RIS File", ris_content, "citation.ris", "text/plain")

    except Exception as e:
        st.write("Error generating citation. Please ensure the URL is correct.")
