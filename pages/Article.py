import streamlit as st
import newspaper

# Main Streamlit app
def main():
    st.set_page_config(page_title="Top Articles Fetcher", page_icon=":newspaper:")

    st.title("Top Articles Fetcher")

    # URL input
    website_url = st.text_input("Enter the URL of the news website:")

    if st.button("Fetch Top Articles"):
        if website_url:
            try:
                # Initialize the newspaper source
                source = newspaper.build(website_url, memoize_articles=False)

                # Fetch top articles
                top_articles = source.articles[:10]  # Fetch top 5 articles

                if top_articles:
                    st.subheader("Top Articles")

                    for article in top_articles:
                        article.download()
                        article.parse()
                        print(article)
                        # Display article title and publish date
                        st.markdown(f"**Title:** {article.title}")
                        st.write(f"**Published Date:** {article.publish_date}")
                        st.code(article.url)
                        st.write('---')

                else:
                    st.warning("No articles found on this website. Please try another URL.")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a valid URL.")

if __name__ == "__main__":
    main()
