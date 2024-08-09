
# Newspaper Summarizer

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen.svg)

Welcome to the **Newspaper Summarizer** project! This repository contains a Python-based web application built with Streamlit that fetches articles from various news websites, summarizes them, and performs further analysis. The project leverages web scraping, natural language processing (NLP), and data analysis techniques to provide concise summaries and insights.

## Features

- **Web Scraping:** Automatically fetches articles from selected news websites.
- **Text Summarization:** Uses NLP techniques to generate concise summaries of the articles.
- **Data Analysis:** Provides additional analysis on the articles, such as sentiment analysis, keyword extraction, and more.
- **User Interface:** Simple and intuitive Streamlit interface for users to interact with the summarizer and view results.
- **Customizable:** Easily extendable to include more news sources or additional types of analysis.

## Installation

To get started with the project, follow the steps below:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/viseshagarwal/Python-Project.git
   cd Python-Project
   ```

2. **Create and Activate a Virtual Environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the Required Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables:**

   Create a `.env` file in the root directory and add your GEMINI API key.

   ```env
   # .env file example
   GEMINI_API_KEY=your_gemini_api_key
   ```

   You can obtain a GEMINI API key by signing up at the [Google AI Studio](https://aistudio.google.com/app/apikey).

5. **Run the Application:**

   ```bash
   streamlit run app.py
   ```

   The application will be available at `http://localhost:8501/`.

## Usage

- Visit the home page to see a list of the latest articles from selected news websites.
- Click on an article to view the summary and additional analysis.
- Use the search feature to find articles on specific topics or keywords.

## Project Structure

```plaintext
.
├── Home.py              # Main Streamlit application
├── requirements.txt    # List of Python dependencies
├── pages/         # Core summarization and analysis logic
│   ├── __init__.py
│   ├── Article.py     # Web scraping logic
│   ├── Summary.py   # Text summarization logic
└── README.md           # Project README file
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Streamlit](https://streamlit.io/) for the web application framework.
- [Newspaper3k](https://github.com/codelucas/newspaper) for article extraction.
- [NLTK](https://www.nltk.org/) and [spaCy](https://spacy.io/) for natural language processing.

## Contact

For any questions or feedback, feel free to reach out at [viseshagarwal@gmail.com](mailto:viseshagarwal@gmail.com).
```
