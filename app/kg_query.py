import os
from neo4j import GraphDatabase
from pyvis.network import Network
import networkx as nx
from vertexai.generative_models import GenerativeModel
import vertexai

class CrimeInvestigationChain:
    def __init__(self, neo4j_uri, neo4j_user, neo4j_password):
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        # Authenticate Vertex AI
        project = os.getenv("VERTEX_PROJECT")
        location = os.getenv("VERTEX_LOCATION", "us-central1")
        vertexai.init(project=project, location=location)
        self.llm = GenerativeModel("gemini-2.5-flash")  # Latest recommended model

    def get_schema(self):
        """Extract schema information compatible with Neo4j 3.5"""
        schema = {"nodes": set(), "relationships": set()}
        with self.driver.session() as session:
            # Get node labels
            result = session.run("CALL db.labels()")
            schema["nodes"] = {record["label"] for record in result}
            # Get relationship types
            result = session.run("CALL db.relationshipTypes()")
            schema["relationships"] = {record["relationshipType"] for record in result}
        return "Nodes: " + ", ".join(schema["nodes"]) + "\nRelationships: " + ", ".join(schema["relationships"])

    def _strip_code_blocks(self, text):
        """Remove Markdown code block markers (with or without language) from text."""
        lines = text.strip().splitlines()
        # Remove first line if it's a code block marker (e.g., ``````cypher)
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]
        # Remove last line if it's a code block marker
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        return "\n".join(lines).strip()

    def generate_cypher(self, question):
        """Use Gemini to generate Cypher query from natural language"""
        schema = self.get_schema()
        prompt = f"""
You are a Crime Investigation Cypher Expert. Generate Cypher queries for Neo4j 3.5.
Follow these rules:
1. Use ONLY the following schema: {schema}
2. Never use database names (default is 'graph.db')
3. Use only nodes and relationships from the POLE model
4. Return ONLY valid Cypher with no explanations

Question: {question}
"""
        response = self.llm.generate_content(prompt)
        cypher = self._strip_code_blocks(response.text)
        return cypher

    def execute_query(self, cypher):
        """Execute Cypher and return raw results"""
        with self.driver.session() as session:
            return session.run(cypher).data()

    def visualize_graph(self, cypher):
        """Create interactive visualization from Cypher results"""
        try:
            results = self.execute_query(cypher)
            G = nx.Graph()
            for record in results:
                for key, value in record.items():
                    if isinstance(value, dict):
                        # Handle nodes
                        if "labels" in value:
                            labels = list(value["labels"])
                            props = {k: v for k, v in value.items() if k != "labels"}
                            node_id = value.get("id", key)
                            G.add_node(node_id, label=props.get("name", key), group=labels[0] if labels else "Node")
                        # Handle relationships
                        elif "type" in value:
                            G.add_edge(value.get("start"), value.get("end"), label=value.get("type"))
            net = Network(height="600px", width="100%")
            net.from_nx(G)
            return net.generate_html()
        except Exception as e:
            return f"<p style='color: red'>Visualization Error: {str(e)}</p>"

    def rag_answer(self, question):
        """Full RAG pipeline with error handling"""
        try:
            # Step 1: Generate Cypher
            cypher = self.generate_cypher(question)
            # Step 2: Execute Query
            results = self.execute_query(cypher)
            # Step 3: Generate Natural Language Answer
            answer = f"## Investigation Results\n\n{results}\n\n**Cypher Query:**\n``````"
            # Step 4: Create Visualization
            viz_html = self.visualize_graph(cypher)
            return {
                "answer": answer,
                "graph_html": viz_html,
                "cypher": cypher
            }
        except Exception as e:
            return {
                "answer": f"🔴 Investigation Error: {str(e)}",
                "graph_html": "",
                "cypher": ""
            }
