import streamlit as st
import newspaper
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load the environment variables
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

prompt = '''You are a News article Summarizer, you have to summarize the text and provide a news summary.
here is my news article text: 
'''

# Function to generate summary using GenAI
def genai_summarize(text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    summary = model.generate_content(prompt+text)
    return summary.text

# Function to fetch article data
def fetch_article_data(url):
    try:
        # Download and parse the article
        article = newspaper.Article(url=url, language='en')
        article.download()
        article.parse()

        # Extract relevant information
        article_data = {
            "title": article.title,
            "text": article.text,
            "published_date": str(article.publish_date),
            "top_image": article.top_image,
            "summary": genai_summarize(article.text, prompt)  # Generate summary using GenAI
        }
        return article_data
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Main Streamlit app
def main():
    st.set_page_config(page_title="Article Information Fetcher", page_icon=":newspaper:")

    st.title("Article Information Fetcher")

    # URL input
    url = st.text_input("Enter the URL of the article:")

    if st.button("Fetch Article"):
        if url:
            article_data = fetch_article_data(url)
            if article_data:
                # Display article information
                st.subheader(article_data['title'])
                st.image(article_data['top_image'], caption="Article Image", use_column_width=True)
                st.write(f"Published Date: {article_data['published_date']}")
                st.subheader("Text")
                st.write(article_data['text'])
                st.subheader("Summary")
                st.write(article_data['summary'])  # Display GenAI generated summary
            else:
                st.warning("No article data available. Please check the URL.")
        else:
            st.warning("Please enter a valid URL.")

if __name__ == "__main__":
    main()