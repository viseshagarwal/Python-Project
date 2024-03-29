import streamlit as st
import newspaper
import nltk


nltk.download('punkt')

def main():
    st.set_page_config(page_title="Top Articles Fetcher", page_icon=":newspaper:")
    st.title("Top Articles Fetcher")

    if 'article' not in st.session_state:
        st.session_state.article = ""
    
    website_url = st.text_input("Enter the URL of the news website:",value=st.session_state.article)
    
    if website_url:
        st.session_state.article = website_url

    if st.button("Fetch Top Articles"):
        if website_url:
            try:
                source = newspaper.build(website_url, memoize_articles=False)
                top_articles = source.articles[:10]
                if top_articles:
                    st.subheader("Top Articles")

                    for article in top_articles:
                        article.download()
                        article.parse()
                        article.nlp()
                        st.markdown(f"**Title:** {article.title}")
                        st.write(f"**Published Date:** {article.publish_date}")
                        st.write(f"**Keywords:** {', '.join(article.keywords)}")
                        st.write("**URL:**")
                        #st.text_area("URL", value=article.url, height=50)
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
