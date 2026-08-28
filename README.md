# AI Smart Recipe Chatbot

An AI-powered culinary assistant that combines **LLMs, Retrieval-Augmented Generation (RAG), recipe APIs, and YouTube transcript analysis** to provide intelligent and context-aware cooking assistance.

## Features

- AI-powered conversational recipe assistant
- **RAG-based document question answering**
- Recipe search using **Spoonacular API**
- **YouTube transcript analysis** for cooking videos
- Context-aware responses using **Google Gemini**
- Interactive web interface built with **Streamlit**

## Architecture

```text
User
 ↓
Streamlit Interface
 ↓
Query Processing
 ↓
 ┌──────────────┬─────────────────┐
 │              │                 │
 RAG       Spoonacular API   YouTube Transcript
 │              │                 │
 └──────────────┴─────────────────┘
                ↓
         Context Construction
                ↓
           Gemini LLM
                ↓
          AI Response
```

## Tech Stack

* **Language:** Python
* **Frontend:** Streamlit
* **AI/LLM:** Google Gemini
* **AI Technique:** Retrieval-Augmented Generation (RAG)
* **Recipe Data:** Spoonacular API
* **Content Processing:** YouTube Transcripts

## How It Works

1. User enters a cooking or recipe-related query.
2. The application identifies the required information source.
3. Relevant information is retrieved from documents, Spoonacular, or YouTube transcripts.
4. Retrieved information is combined with the user's query.
5. Gemini generates a context-aware response.
6. The response is displayed through the Streamlit interface.

## Example Queries

```text
"What can I cook with potatoes and tomatoes?"

"Give me a vegetarian alternative to this recipe."

"What ingredients are used in this cooking video?"

"Explain this recipe step by step."
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/sreenidhe08/AI-Smart-Recipe-Chatbot.git
cd AI-Smart-Recipe-Chatbot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
SPOONACULAR_API_KEY=your_spoonacular_api_key
```

> Never commit API keys or `.env` files to GitHub.

### 4. Run the application

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

## Future Improvements

* Image-based ingredient recognition
* Personalized dietary recommendations
* Nutrition analysis
* Voice-based interaction
* Weekly meal planning
* Improved vector-based RAG retrieval

## Learning Outcomes

This project demonstrates practical experience with:

* **Generative AI and LLMs**
* **Retrieval-Augmented Generation**
* **Prompt Engineering**
* **API Integration**
* **Natural Language Processing**
* **Streamlit Application Development**
* **AI Application Architecture**

## License

This project is intended for educational and development purposes.

```
```
