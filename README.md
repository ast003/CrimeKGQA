Absolutely! Here’s your **complete `README.md`** — ready to copy-paste **as raw Markdown code**, without any extra explanation — exactly how you’d save it in a file:

````markdown
# 🕵️‍♂️ CrimeKGQA: Crime Investigation Assistant

CrimeKGQA is an AI-powered question answering and visualization system for crime investigation, built on a Neo4j crime knowledge graph. It allows investigators and researchers to ask natural language questions about crimes, suspects, locations, and evidence — and get both text answers and interactive graph visualizations.

---

## 🚀 Features

✅ **Knowledge Graph Backend** — Neo4j stores and queries a large-scale crime knowledge graph using the POLE model (Person, Object, Location, Event).  
✅ **Natural Language Q&A** — Maps user questions to Cypher queries using templates (and can be extended to LLMs).  
✅ **Interactive Visualization** — Visualizes answers as an interactive graph using Pyvis and NetworkX.  
✅ **Modern UI** — Built with Streamlit for a smooth chat-like interface.  
✅ **Containerized Deployment** — Runs with Docker Compose for easy setup and reproducibility.

---

## 🏁 Quickstart

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/ast003/CrimeKGQA-Crime-Investigation-Assistant.git
cd CrimeKGQA-Crime-Investigation-Assistant
````

### 2️⃣ Add Your Data

* Place your Neo4j database dump (e.g., `pole.dump`) in the `data/` directory.
* ⚠️ **Important:** Do **NOT** commit the `data/` folder — it's listed in `.gitignore`.

### 3️⃣ Build & Run the System

```bash
docker compose up --build
```

* **Neo4j Browser:** [http://localhost:7474](http://localhost:7474)
  *(Username: `neo4j` | Password: `test`)*
* **Streamlit App:** [http://localhost:8501](http://localhost:8501)

### 4️⃣ Load the POLE Dataset into Neo4j

Run this in your terminal:

```bash
docker exec -it crimekgqa-neo4j bin/neo4j-admin load --from=/data/pole.dump --database=graph.db --force
docker restart crimekgqa-neo4j
```

---

## 💡 Usage

* Open [http://localhost:8501](http://localhost:8501).
* Ask questions such as:

  * *"Identify people involved in multiple crimes and find their connections."*
  * *"Which areas have the highest crime rates?"*
  * *"Show all associates of Amy."*
* The app shows:

  * ✅ The generated Cypher query
  * ✅ A text answer
  * ✅ An interactive knowledge graph visualization

---

## 📁 Project Structure

```plaintext
CrimeKGQA/
├── app/
│   ├── main.py
│   └── kg_query.py
├── data/
│   └── pole.dump  (Not committed)
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## 🛠️ Technologies

* Python 3.10+
* Neo4j (3.5 or 4.x)
* Pyvis, NetworkX
* Streamlit
* Docker & Docker Compose

---

## ⚙️ Customization

* **Add More Questions:**
  Edit the `simple_cypher_template()` function in `kg_query.py` to define new question patterns, or connect an LLM for dynamic Cypher generation.

* **Configure Database:**
  Update environment variables in `docker-compose.yml` or `.env`.

---

## ⚠️ Notes

* **Large Data:**
  GitHub does **not** accept files larger than 100 MB — do not commit large dumps or Neo4j system files.
  For sharing big datasets, use cloud storage (e.g., Google Drive) or [Git Large File Storage (LFS)](https://git-lfs.github.com).

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 🙏 Acknowledgements

* Inspired by the [CrimeKGQA](https://arxiv.org/abs/2305.12292) research paper.
* Special thanks to Neo4j, Streamlit, and the open-source Python community.

---

## 📬 Contact

💌 For questions, feature requests, or collaboration:

* Open an [issue](https://github.com/ast003/CrimeKGQA-Crime-Investigation-Assistant/issues)
* Or email: [asthasingh6038@gmail.com](mailto:asthasingh6038@gmail.com)

---

✨ *Happy investigating! Stay curious, stay safe.* 🔍✨

````

---

✅ **How to use:**  
1. Copy all the lines above **as is**  
2. Save to a file named `README.md`  
3. Add & commit it to your repo:  
   ```bash
   git add README.md
   git commit -m "Add complete README.md"
   git push
````

If you want, I can also generate a polished version with badges, a table of contents, or example screenshots — just ask! 🚀✨

