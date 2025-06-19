import os
import streamlit as st
from kg_query import CrimeInvestigationChain

# Configure Page
st.set_page_config(
    page_title="CrimeKGQA - Investigation Assistant",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background: #2e3b4e !important;
    }
    .stChatInput textarea {
        background-color: #1a1a1a !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize System
@st.cache_resource
def init_system():
    return CrimeInvestigationChain(
        neo4j_uri=os.getenv("NEO4J_URI", "bolt://neo4j:7687"),
        neo4j_user=os.getenv("NEO4J_USER", "neo4j"),
        neo4j_password=os.getenv("NEO4J_PASSWORD", "test")
    )

# Sidebar Controls
with st.sidebar:
    st.title("🔧 System Controls")
    st.markdown("**Connected Database:**")
    st.code(f"{os.getenv('NEO4J_URI', 'bolt://neo4j:7687')}")
    st.markdown("---")
    st.markdown("### Sample Queries")
    st.button("Show Multi-Crime Suspects", 
              help="Find suspects involved in multiple crimes")
    st.button("Analyze Crime Hotspots",
              help="Identify high-crime geographical areas")
    st.button("Visualize Crime Networks",
              help="Show network of suspects and relationships")

# Main Interface
st.title("🕵️ CrimeKGQA - Intelligent Investigation Assistant")
st.markdown("""
**Welcome to the Crime Investigation Assistant**  
Ask natural language questions about criminal networks, patterns, and relationships.
""")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"]["answer"])
        if msg["content"]["graph_html"]:
            st.components.v1.html(msg["content"]["graph_html"], height=600)

# Processing Pipeline
if prompt := st.chat_input("Enter investigation question..."):
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": {"answer": prompt, "graph_html": "", "cypher": ""}
    })
    
    # Generate response
    with st.spinner("🔍 Analyzing criminal patterns..."):
        response = init_system().rag_answer(prompt)
        
        # Add assistant response
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
        
        # Rerender
        st.rerun()

