# 🕵️‍♀️ CrimeKGQA: Crime Investigation Assistant

**CrimeKGQA** is an AI-powered question answering and visualization system for crime investigation, built on top of a Neo4j crime knowledge graph. It allows users to ask natural language questions about crimes, suspects, locations, and evidence — and provides both textual answers and interactive graph visualizations.

---

## 🚀 Features

* **📚 Knowledge Graph Backend:** Uses Neo4j to store and query a large-scale crime knowledge graph following the POLE model (Person, Object, Location, Event).
* **🔍 Natural Language Question Answering:** Maps user questions to Cypher queries using templates (can be extended to LLMs).
* **🌐 Interactive Visualization:** Displays graph-based answers with Pyvis and NetworkX.
* **💬 Modern UI:** Intuitive Streamlit chat interface.
* **🐳 Containerized Deployment:** Easily run all components via Docker Compose.

---

## 📦 Quickstart

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/ast003/CrimeKGQA-Crime-Investigation-Assistant.git
cd CrimeKGQA-Crime-Investigation-Assistant
```

### 2️⃣ Add Your Data

* Place your Neo4j database dump (for example, `pole.dump`) in the `data/` directory.
* ⚠️ **Important:** Do NOT commit the `data/` folder — it's ignored via `.gitignore`.

### 3️⃣ Build and Start the System

```bash
docker compose up --build
```

* **Neo4j Browser:** [http://localhost:7474](http://localhost:7474)
  (Username: `neo4j` | Password: `test`)

* **Streamlit App:** [http://localhost:8501](http://localhost:8501)

### 4️⃣ Load the POLE Dataset into Neo4j

Run the following commands:

```bash
docker exec -it crimekgqa-neo4j bin/neo4j-admin load --from=/data/pole.dump --database=graph.db --force
docker restart crimekgqa-neo4j
```

---

## 💡 How to Use

1. Open [http://localhost:8501](http://localhost:8501) in your browser.
2. Ask questions like:

   * *"Identify people involved in multiple crimes and find their connections."*
   * *"Which geographical areas have the highest crime rates?"*
   * *"Show all associates of Amy."*
3. View:

   * ✅ Generated Cypher query
   * ✅ Textual answer
   * ✅ Interactive graph visualization

---

## 📂 Project Structure

```
CrimeKGQA/
├── app/
│   ├── main.py
│   └── kg_query.py
├── data/
│   └── pole.dump  (not committed)
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## ⚙️ Technologies

* Python 3.10+
* Neo4j 3.5 / 4.x
* Pyvis, NetworkX
* Streamlit
* Docker & Docker Compose

---

## ⚙️ Customization

* **Add More Question Templates:**
  Edit the `simple_cypher_template()` function in `kg_query.py` to support more question types, or integrate an LLM for dynamic Cypher query generation.

* **Change Database Settings:**
  Update the environment variables in `docker-compose.yml` or add a `.env` file.

---

## ⚠️ Important Notes

* **Large Files:**
  GitHub does not allow files larger than 100 MB. Do NOT commit Neo4j dumps or system database files. Instead, use cloud storage (e.g., Google Drive) or [Git Large File Storage (LFS)](https://git-lfs.github.com) for sharing large datasets.

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 🙏 Acknowledgements

* Based on the [CrimeKGQA](https://arxiv.org/abs/2305.12292) research paper.
* Thanks to the Neo4j, Streamlit, and open-source Python communities for making this possible.

---

## 📬 Contact

For questions, suggestions, or collaboration:

* Open an [issue](https://github.com/ast003/CrimeKGQA-Crime-Investigation-Assistant/issues)
* Or email [asthasingh6038@gmail.com](mailto:asthasingh6038@gmail.com)

---

✨ **Happy investigating! 🕵️‍♂️✨**

