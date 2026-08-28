# AI Smart Recipe Chatbot

An AI-powered culinary assistant that combines **Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), external recipe APIs, and YouTube transcript analysis** to provide intelligent, context-aware cooking and recipe assistance.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [How It Works](#how-it-works)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [Application Modules](#application-modules)
- [RAG Pipeline](#rag-pipeline)
- [YouTube Transcript Analysis](#youtube-transcript-analysis)
- [Recipe API Integration](#recipe-api-integration)
- [LLM Integration](#llm-integration)
- [Example Workflow](#example-workflow)
- [Use Cases](#use-cases)
- [Testing](#testing)
- [Error Handling](#error-handling)
- [Security Considerations](#security-considerations)
- [Performance Considerations](#performance-considerations)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Learning Outcomes](#learning-outcomes)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Overview

The **AI Smart Recipe Chatbot** is an interactive AI application designed to make recipe discovery and cooking assistance more intelligent and conversational.

Instead of relying only on predefined recipes, the application combines multiple information sources:

1. **LLM-based conversational AI**
2. **Retrieval-Augmented Generation (RAG)**
3. **Recipe APIs**
4. **YouTube cooking-video transcripts**
5. **User queries and contextual information**

This allows users to ask natural-language questions such as:

> What can I cook with chicken and potatoes?

> Give me a vegetarian alternative to this recipe.

> Explain the cooking steps in this video.

> What ingredients are required for this recipe?

The system processes the query, retrieves relevant information when required, and uses an LLM to generate a useful response.

---

# Key Features

## 1. AI-Powered Recipe Assistance

Users can interact with the chatbot using natural language.

The assistant can help with:

- Recipe discovery
- Ingredient suggestions
- Cooking instructions
- Recipe explanations
- Ingredient substitutions
- Cooking-related questions
- Personalized recipe recommendations

---

## 2. Retrieval-Augmented Generation

The application uses **RAG** to improve responses by providing relevant external context to the language model.

Instead of asking the LLM to answer purely from its internal knowledge, the system:

```text
User Query
     ↓
Retrieve Relevant Information
     ↓
Build Context
     ↓
Send Context + Query to LLM
     ↓
Generate Response
