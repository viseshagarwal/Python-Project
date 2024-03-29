import streamlit as st


def main(): 
    
    st.set_page_config(page_title="Home", page_icon=":newspaper:")
    st.sidebar.title("Navigation")
    st.title("Home")
    st.write("Welcome to the News Article Summarizer!")
    st.write("Use the sidebar to navigate to different pages.")
    st.write("You can use the following pages:")

    st.markdown("- **Top Articles Fetcher**: Fetch top articles from a news website.")
    st.markdown("- **Article Information Fetcher**: Fetch information about a specific article.")

    st.write("Happy Summarizing!")
    st.write("Made with ❤️ by [Visesh Agarwal](https://github.com/viseshagarwal)")

    
if __name__ == "__main__":
    main()