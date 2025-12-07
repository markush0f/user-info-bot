# User Info Bot – Local Installation Guide

This project is an advanced chatbot capable of responding with **real information about the user**, combining web scraping via **HeadlessX**, GitHub repository analysis, vector-based semantic search, and a RAG (Retrieval-Augmented Generation) architecture using the OpenAI API.

Below is a complete guide to running the project **locally**, including Docker for the database, environment variables, and backend startup.

---

## 1. Requirements

* Python 3.11+
* Docker & Docker Compose
* Git
* An OpenAI API Key

---

## 2. Clone the Repository

```bash
git clone https://github.com/markush0f/user-info-bot.git
cd user-info-bot
```

---

## 3. Install and Configure HeadlessX

This project requires **HeadlessX** to enable advanced dynamic web scraping.

📌 **HeadlessX repository & documentation:**
[https://headlessx.saify.me/#api](https://headlessx.saify.me/#api)

Follow the instructions in their documentation to set up the service and generate your API keys.

---

## 4. Environment Variables

Create a `.env` file in the project root with the following structure:

```env
# OPENAI
OPENAI_API_KEY=

# DATABASE
USER_DB=
PASSWORD_DB=
DATABASE=
HOST=
PORT=
# REQUIRED if you use PSYCOPG2,
# SSL=require

# GITHUB
GITHUB_TOKEN=

# HEADLESSX
# Or use: node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
HEADLESSX_AUTH_TOKEN=
HEADLESSX_API=
```

---

## 5. Start the Database with Docker

Run PostgreSQL using Docker Compose:

```bash
docker compose up -d
```


---

## 6. Install Python Dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 7. Run the Backend

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

📌 **Important:**
All database tables are automatically created on startup using SQLModel — no migrations are required.

Your server will be available at:

```
http://localhost:8000
```

Interactive API docs:

```
http://localhost:8000/docs
```

---

## 8. Data Flow: How Information Is Collected, Processed, and Stored

This project follows a structured pipeline to extract, store, and embed user‑related information. Below is the complete flow of how data moves through the system:

### **1. Extract GitHub User Information**

The process begins by calling the GitHub extraction endpoint.
This step collects:

* User profile data
* Public repositories
* Metadata (stars, forks, last activity)

All raw GitHub data is saved locally inside the **`outputs/`** directory.
This ensures you always keep a local copy of the fetched information.

---

### **2. Save Projects Into the Database**

Once the GitHub data is downloaded, the next step is to persist the projects.

You can save:

* **All repositories at once** using a parameter such as `all=true`, or
* **Specific repositories** by providing only their names.

The `projects/save` endpoint processes each repository and stores it in the database.

---

### **3. Save Project Languages**

After saving the projects, the system must associate each repository with its detected languages.

The `projects/languages/save` endpoint:

* Reads language data extracted from GitHub
* Stores language–project relationships in the database

This enables the chatbot to understand the user's tech stack more accurately.

---

### **4. Save User Information**

User‑level metadata (profile details, description, followers, etc.) is saved through the `users/save` endpoint.

This creates a persistent user profile that can later be used by the chatbot to personalize responses.

---

### **5. Store Any Additional Entities**

The system also supports saving **custom entities** of any type:

* Websites scraped using HeadlessX
* Text documents
* Notes or user‑provided data
* Dynamic records from external APIs

These entities enrich the knowledge base used by the RAG pipeline.

---

### **6. Generate Embeddings (Final Step)**

After all data is stored, the final step is to create embeddings.

The embedding service:

1. Reads all stored entities, projects, languages, and user records
2. Converts them into vector embeddings
3. Stores them into the vector database for semantic search

This step is essential, as it allows the chatbot to:

* Retrieve relevant information
* Perform semantic reasoning
* Provide personalized, data‑driven responses

---

## 7. Data Flow Diagram

```
 ┌─────────────────────────┐        ┌──────────────────────────┐
 │ 1. GitHub Extraction    │        │   HeadlessX Scraping     │
 │  (Fetch user + repos)   │        │ (Dynamic website content)│
 └─────────────┬───────────┘        └──────────────┬───────────┘
               │                                     │
               ▼                                     ▼
       ┌─────────────────┐                    ┌─────────────────┐
       │  outputs/ folder│                    │  Additional     │
       │ (raw GitHub data)│                   │  Entities       │
       └─────────┬───────┘                    └────────┬────────┘
                 │                                      │
                 ▼                                      ▼
      ┌────────────────────┐                 ┌────────────────────┐
      │ 2. Save Projects   │                 │ Save Custom Entities│
      └─────────┬──────────┘                 └─────────┬───────────┘
                │                                        │
                ▼                                        ▼
        ┌───────────────────┐                  ┌───────────────────────┐
        │3. Save Languages  │                  │4. Save User Profile   │
        └──────────┬────────┘                  └───────────┬──────────┘
                   │                                         │
                   └───────────────┬─────────────────────────┘
                                   ▼
                      ┌─────────────────────────┐
                      │5. Generate Embeddings   │
                      │  (Vector Database)       │
                      └─────────────┬───────────┘
                                    ▼
                          ┌──────────────────────┐
                          │   RAG Query Engine    │
                          │ (Semantic Retrieval)  │
                          └─────────────┬────────┘
                                        ▼
                           ┌────────────────────────┐
                           │  LLM (OpenAI API)       │
                           │ Personalized Response   │
                           └────────────────────────┘
```

---

## 8. Workflow Diagram (Text-Based)

```
USER DATA INGESTION WORKFLOW
============================

1. GitHub Data Fetching
   → Repositories, metadata, activity
   → Stored in outputs/

2. Persist Repositories
   → Save all repos or selected ones
   → Create project records

3. Persist Language Statistics
   → Language ↔ Project associations

4. Persist User Profile
   → GitHub user info
   → Stored as user entity

5. Add Additional Entities
   → Scraped websites (HeadlessX)
   → Documents, notes, external records

6. Embedding Pipeline
   → Convert all stored entities to vectors
   → Insert into vector database

7. RAG Retrieval
   → Semantic search returns relevant context

8. LLM Generation
   → OpenAI model produces final grounded answer
```

---

## 9. API Reference Table

| Endpoint                           | Description                             | Input                               | Output                       |
| ---------------------------------- | --------------------------------------- | ----------------------------------- | ---------------------------- |
| **GET /github/extract/{username}** | Extract GitHub user + repos             | GitHub username                     | Saves raw data to `outputs/` |
| **POST /projects/save**            | Save projects into DB                   | `all=true` or list of project names | Project records              |
| **POST /projects/languages/save**  | Save language statistics                | Repo language metadata              | Language-project links       |
| **POST /users/save**               | Save user profile                       | GitHub user data                    | User record                  |
| **POST /entities/save**            | Save any custom entity                  | JSON                        | Generic entity record        |
| **POST /embeddings/generate**      | Generate embeddings for all stored data | None                                | Vector DB populated          |

---

## 10. Summary

With this guide, you can run the project locally with:

* PostgreSQL using Docker
* FastAPI backend fully configured
* Automatic table creation using SQLModel
* Complete environment variables for development or production
* HeadlessX integrated for dynamic web scraping

If you would like a section for VPS deployment, full Dockerization of the backend, or a diagram explaining the system architecture, I can add it.
