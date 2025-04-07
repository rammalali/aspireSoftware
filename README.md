# 📚 Mini Library Management System (FastAPI + AI)

This project is a lightweight **Library Management System** built with **FastAPI** and **PostgreSQL**, featuring AI-powered enhancements using **OpenAI GPT & Embedding models**.

## 🚀 Features

- ✅ **Book Management**  
  Add, edit, delete, and view book entries with metadata like title, author, year, genre, ISBN, and availability.

- 🔄 **Check-In / Check-Out**  
  Mark books as borrowed or returned.

- 🔍 **Search Books**  
  Filter books by title, author, genre, year, ISBN, or availability.

- 🧠 **AI-Generated Descriptions**  
  If no description is provided during book creation, the app auto-generates a relevant one using GPT-3.5.

- 🧬 **AI Embeddings Ready**  
  Book descriptions are embedded with `text-embedding-ada-002` and stored in PostgreSQL for future semantic search.

---

## 🛠 Tech Stack

- **Backend**: FastAPI (async)
- **Database**: PostgreSQL with SQLAlchemy (async)
- **AI**: OpenAI API (`gpt-3.5-turbo`, `text-embedding-ada-002`)
- **ORM**: SQLAlchemy with PostgreSQL `ARRAY` type for embeddings
- **Environment**: `.env` for managing API keys securely

---

## 🧑‍💻 Setup Instructions

1. **Clone the repo**  
   ```bash
   git clone https://github.com/rammalali/aspireSoftware.git
   cd aspireSoftware
3. **Testing*
   to test this project you can use postman or localhost:8000/docs 
