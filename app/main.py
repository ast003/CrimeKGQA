import os
import streamlit as st
from kg_query import CrimeInvestigationChain

st.set_page_config(page_title="CrimeKGQA", page_icon="🔍", layout="wide")
st.title("🔍 CrimeKGQA: Crime Investigation Assistant")

with st.sidebar:
    st.header("System Info")
    st.markdown("**Neo4j URI:** " + os.getenv("NEO4J_URI", "bolt://neo4j:7687"))
    st.markdown("**User:** " + os.getenv("NEO4J_USER", "neo4j"))
    st.markdown("**Sample queries:**")
    st.markdown("- Identify people involved in multiple crimes and find their connections")
    st.markdown("- Which geographical areas have the highest crime rates?")
    st.markdown("- Show all associates of Amy")

@st.cache_resource
def init_chain():
    return CrimeInvestigationChain(
        neo4j_uri=os.getenv("NEO4J_URI", "bolt://neo4j:7687"),
        neo4j_user=os.getenv("NEO4J_USER", "neo4j"),
        neo4j_password=os.getenv("NEO4J_PASSWORD", "test")
    )

chain = init_chain()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.markdown(message["content"])
        else:
            st.markdown(message["content"]["answer"])
            if message["content"].get("graph_html"):
                st.components.v1.html(message["content"]["graph_html"], height=600)
            if message["content"].get("cypher_query"):
                with st.expander("Generated Cypher Query"):
                    st.code(message["content"]["cypher_query"], language="cypher")

if prompt := st.chat_input("Ask a crime investigation question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            response = chain.rag_answer(prompt)
            st.markdown(response["answer"])
            if response.get("graph_html"):
                st.components.v1.html(response["graph_html"], height=600)
            if response.get("cypher_query"):
                with st.expander("Generated Cypher Query"):
                    st.code(response["cypher_query"], language="cypher")
            st.session_state.messages.append({"role": "assistant", "content": response})

st.markdown("---")
st.markdown("**CrimeKGQA** - Powered by Neo4j, Python, and Streamlit.")
