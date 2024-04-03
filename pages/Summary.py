import streamlit as st
import newspaper
import os
from dotenv import load_dotenv
import google.generativeai as genai
import nltk
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer

# Set page configuration
st.set_page_config(
    page_title="Article Summary",
    page_icon=":newspaper:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Download NLTK data
nltk.download("punkt")
nltk.download("vader_lexicon")

# Load environment variables
load_dotenv()

# Configure generative AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(model_name="gemini-pro")

# Prompt for article summary
prompt = """You are a News article Summarizer, you have to summarize the news article text and content and provide a news summary.
Here is my news article text: 
"""


# Function to generate article summary using generative AI
def genai_summarize(text, prompt):
    try:
        summary = model.generate_content(prompt + text)
        summary_text = summary_text = (
            summary.text
            + '\n\n"'
            + "**Generated News Summary by using Gemini AI**"
            + '"'
        )
        return summary_text
    except Exception as e:
        raise ValueError(f"An error occurred while generating the summary: {str(e)}")


# Function to perform sentiment analysis using NLTK
def get_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(text)["compound"]

    if sentiment_score > 0:
        sentiment_label = "Positive 🙂"
    elif sentiment_score < 0:
        sentiment_label = "Negative 😞"
    else:
        sentiment_label = "Neutral 😐"

    return sentiment_score, sentiment_label


# Function to fetch article data
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

        sentiment_score, sentiment_label = get_sentiment(article.text)

        article_data = {
            "title": article.title,
            "text": article.text,
            "authors": article.authors,
            "published_date": str(article.publish_date),
            "top_image": article.top_image,
            "summary": summary,
            "keywords": article.keywords,
            "sentiment_score": sentiment_score,
            "sentiment_label": sentiment_label,
        }
        return article_data
    except Exception as e:
        st.error(f"An error occurred while fetching the article data: {str(e)}")
        return None


# Function to generate word cloud
def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(
        text
    )
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(plt)


# Main function to run the Streamlit app
def main():
    st.title("Article Summary")

    # Input URL of the article
    url = st.text_input("Enter the URL of the article:")

    # Fetch article when button clicked
    if st.button("Fetch Article"):
        with st.spinner("Fetching article..."):
            if url:
                article_data = fetch_article_data(url)
                if article_data:
                    # Display article details
                    st.header(article_data["title"])
                    st.image(
                        article_data["top_image"],
                        caption="Article Image",
                        use_column_width=True,
                    )
                    st.write(f"Published Date: {article_data['published_date']}")

                    # Display article text
                    st.subheader("News")
                    st.write(article_data["text"])

                    # Display keywords
                    if article_data["keywords"]:
                        st.subheader("Keywords")
                        st.write(", ".join(article_data["keywords"]))

                    # Display word cloud
                    if article_data["text"]:
                        st.subheader("Word Cloud")
                        generate_wordcloud(article_data["text"])

                    # Display article summary
                    if article_data["summary"]:
                        st.subheader("Summary")
                        st.write(article_data["summary"])
                    else:
                        st.warning("Failed to generate summary.")

                    # Display sentiment analysis
                    st.subheader("Sentiment Analysis")
                    st.write(f"Sentiment Score: {article_data['sentiment_score']:.2f}")
                    st.write(f"Overall sentiment: {article_data['sentiment_label']}")

                else:
                    st.warning("No article data available. Please check the URL.")
            else:
                st.warning("Please enter a valid URL.")


if __name__ == "__main__":
    main()
