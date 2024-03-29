import streamlit as st
import newspaper
import os
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(model_name="gemini-1.0-pro")

prompt = '''You are a News article Summarizer, you have to summarize the text and provide a news summary.
here is my news article text: 
'''

def genai_summarize(text, prompt):
    try:
        summary = model.generate_content(prompt+text)
        return summary.text
    except Exception as e:
        st.error(f"An error occurred while generating the summary: {str(e)}")
        return None

def fetch_article_data(url):
    try:
        article = newspaper.Article(url=url, language='en')
        article.download()
        article.parse()
        article_data = {
            "title": article.title,
            "text": article.text,
            "published_date": str(article.publish_date),
            "top_image": article.top_image,
            "summary": genai_summarize(article.text, prompt)
        }
        return article_data
    except Exception as e:
        st.error(f"An error occurred while fetching the article data: {str(e)}")
        return None

def main():
    st.set_page_config(page_title="Article Information Fetcher", page_icon=":newspaper:")
    st.title("Article Information Fetcher")
    url = st.text_input("Enter the URL of the article:")

    if st.button("Fetch Article"):
        if url:
            article_data = fetch_article_data(url)
            if article_data:
                st.header(article_data['title'])
                st.image(article_data['top_image'], caption="Article Image", use_column_width=True)
                st.write(f"Published Date: {article_data['published_date']}")
                st.write(f"**Authors:** {article_data['authors'] if article_data['authors'] else 'Not available'}")
                st.subheader("Text")
                st.write(article_data['text'])
                if article_data['summary']:
                    st.subheader("Summary")
                    st.write(article_data['summary'])
                else:
                    st.warning("Failed to generate summary.")
            else:
                st.warning("No article data available. Please check the URL.")
        else:
            st.warning("Please enter a valid URL.")

if __name__ == "__main__":
    main()
