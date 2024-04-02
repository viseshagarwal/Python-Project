import streamlit as st
import newspaper
import nltk

nltk.download("punkt")


def main():

    st.set_page_config(
        page_title="Top Articles Fetcher",
        page_icon=":newspaper:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.title("Top Articles Fetcher")

    top_websites = {
        "News18": "https://www.News18.com/news",
        "NDTV": "https://ndtv.com/",
        "NDTV India": "https://www.ndtv.in/",
        "India TV": "https://www.indiatvnews.com/",
        "Deccan Herald": "https://www.deccanherald.com/",
        "BBC News": "https://www.bbc.com/news",
        "The Guardian": "https://www.theguardian.com/international",
        "New York Times": "https://www.nytimes.com/",
        "Washington Post": "https://www.washingtonpost.com/",
        "Wall Street Journal": "https://www.wsj.com/",
        "Times of India": "https://timesofindia.indiatimes.com/",
        "Indian Express": "https://indianexpress.com/",
        "The Hindu": "https://www.thehindu.com/",
        "Economic Times": "https://economictimes.indiatimes.com/",
        "Financial Express": "https://www.financialexpress.com/",
        "Live Mint": "https://www.livemint.com/",
        "Business Standard": "https://www.business-standard.com/",
        "Times Now": "https://www.timesnownews.com/",
        "Republic World": "https://www.republicworld.com/",
        "India Today": "https://www.indiatoday.in/",
        "Firstpost": "https://www.firstpost.com/",
        "Scroll.in": "https://scroll.in/",
    }

    # Option to select from predefined list or provide custom list
    selection_method = st.radio(
        "Select website(s) from:",
        options=["Top News Websites", "Custom News Website link"],
    )

    if selection_method == "Top News Websites":
        selected_website = st.selectbox(
            "Select a news website:", list(top_websites.keys())
        )
        website_url = top_websites.get(selected_website)
    else:
        custom_websites = st.text_area("Enter URLs of news websites (one per line):")
        website_url = [
            url.strip() for url in custom_websites.split("\n") if url.strip()
        ]

    if st.button("Fetch Top Articles"):
        with st.spinner("Fetching article..."):
            if website_url:
                try:
                    if isinstance(website_url, str):
                        website_url = [website_url]
                    for url in website_url:
                        source = newspaper.build(url, memoize_articles=False)
                        top_articles = source.articles[:10]
                        if top_articles:
                            st.subheader(f"Top Articles from {url}")

                            for article in top_articles:
                                article.download()
                                article.parse()
                                article.nlp()
                                st.markdown(f"**Title:** {article.title}")
                                st.write(f"**Published Date:** {article.publish_date}")
                                st.write(f"**Keywords:** {', '.join(article.keywords)}")
                                st.write("Copy the Artcile URL to view the summary")
                                st.write("**URL:**")
                                st.code(article.url)
                                url = article.url
                                st.session_state["url"] = url
                                # print(st.session_state)
                                st.markdown(
                                    '<a href="/Summary" target="_self"><button style="background-color: #4CAF50; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer;">Open Summary Page</button></a>',
                                    unsafe_allow_html=True,
                                )
                                # if st.button("Read Article", key=url):
                                #     st.session_state["url"] = url
                                #     st.markdown(f"**URL:** {url}")
                                #     print(st.session_state["url"])
                                #     st.write("---")
                                #     st.write("Click below to view the summary:")
                                #     # import streamlit as st

                                #     # st.markdown(
                                #     #     '<a href="http://localhost:8501/Summary" target="_blank"></a>',
                                #     #     unsafe_allow_html=True,
                                #     # )
                                #     # st.markdown('<a href="http://localhost:8501/Summary?url=' + url + '" target="_blank">Next page</a>', unsafe_allow_html=True)

                                st.write("---")
                        else:
                            st.warning(
                                f"No articles found on {url}. Please try another URL."
                            )

                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
            else:
                st.warning("Please select a news website.")


if __name__ == "__main__":
    main()
