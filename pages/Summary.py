import streamlit as st
import newspaper
import os
from dotenv import load_dotenv
import google.generativeai as genai
import nltk
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from textblob import TextBlob

st.set_page_config(
    page_title="Article Summary",
    page_icon=":newspaper:",
    layout="wide",
    initial_sidebar_state="expanded",
)

nltk.download("punkt")

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(model_name="gemini-pro")

prompt = """You are a News article Summarizer, you have to summarize the news article text and content and provide a news summary.
here is my news article text: 
"""


def genai_summarize(text, prompt):
    try:
        summary = model.generate_content(prompt + text)
        return summary.text
    except Exception as e:
        raise ValueError(f"An error occurred while generating the summary: {str(e)}")


def fetch_article_data(url):
    try:
        article = newspaper.Article(url=url, language="en")
        article.download()
        article.parse()
        article.nlp()

        try:
            summary = genai_summarize(article.text, prompt)
        except Exception as genai_exception:
            summary = article.summary if article.summary else "No summary available"

        article_data = {
            "title": article.title,
            "text": article.text,
            "authors": article.authors,
            "published_date": str(article.publish_date),
            "top_image": article.top_image,
            "summary": summary,
            "keywords": article.keywords,
            "sentiment": TextBlob(
                article.text
            ).sentiment.polarity,  
        }
        return article_data
    except Exception as e:
        st.error(f"An error occurred while fetching the article data: {str(e)}")
        return None


def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(
        text
    )
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(plt)


def main():
    st.title("Article Summary")

    url = st.text_input("Enter the URL of the article:")

    if st.button("Fetch Article"):
        with st.spinner("Fetching article..."):  
            if url:
                article_data = fetch_article_data(url)
                if article_data:
                    st.header(article_data["title"])
                    st.image(
                        article_data["top_image"],
                        caption="Article Image",
                        use_column_width=True,
                    )
                    st.write(f"Published Date: {article_data['published_date']}")
                    st.subheader("News")
                    st.write(article_data["text"])

                    if article_data["keywords"]:
                        st.subheader("Keywords")
                        st.write(", ".join(article_data["keywords"]))

                    if article_data["text"]:
                        st.subheader("Word Cloud")
                        generate_wordcloud(article_data["text"])

                    if article_data["summary"]:
                        st.subheader("Summary")
                        st.write(article_data["summary"])
                    else:
                        st.warning("Failed to generate summary.")

                    st.subheader("Sentiment Analysis")
                    sentiment_score = article_data["sentiment"]
                    if sentiment_score > 0:
                        st.write("Overall sentiment: Positive")
                    elif sentiment_score < 0:
                        st.write("Overall sentiment: Negative")
                    else:
                        st.write("Overall sentiment: Neutral")

                else:
                    st.warning("No article data available. Please check the URL.")
            else:
                st.warning("Please enter a valid URL.")


if __name__ == "__main__":
    main()
