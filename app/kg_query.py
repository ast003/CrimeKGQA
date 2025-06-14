import os
from neo4j import GraphDatabase
from pyvis.network import Network
import networkx as nx

class CrimeInvestigationChain:
    def __init__(self, neo4j_uri, neo4j_user, neo4j_password):
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

    def query(self, cypher_query, parameters=None):
        with self.driver.session() as session:
            result = session.run(cypher_query, parameters or {})
            return [record for record in result]

    def visualize_graph(self, cypher_query):
        """Return HTML for interactive graph visualization."""
        results = self.query(cypher_query)
        G = nx.Graph()

        # Robustly extract nodes and relationships from Neo4j result
        for record in results:
            for value in record.values():
                # Node
                if hasattr(value, 'id') and hasattr(value, 'labels'):
                    node_label = value.get('name', f"Node_{value.id}") if hasattr(value, 'get') else f"Node_{value.id}"
                    G.add_node(value.id, label=node_label)
                # Relationship
                elif hasattr(value, 'type') and hasattr(value, 'start_node') and hasattr(value, 'end_node'):
                    G.add_edge(value.start_node.id, value.end_node.id, label=value.type)

        if len(G.nodes) == 0:
            return "<p>No graph data to visualize.</p>"
        net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white")
        net.from_nx(G)
        return net.generate_html()

    def rag_answer(self, user_query):
        """Map question to Cypher, run, and summarize."""
        cypher_query = self.simple_cypher_template(user_query)
        if not cypher_query:
            return {"answer": "Sorry, I could not understand your question.", "graph_html": None, "cypher_query": None}

        results = [r.data() for r in self.query(cypher_query)]
        answer = f"Results for query: {user_query}\n\n{results}"
        graph_html = self.visualize_graph(cypher_query)
        return {"answer": answer, "graph_html": graph_html, "cypher_query": cypher_query}

    def simple_cypher_template(self, user_query):
        """Return Cypher that always includes nodes and relationships for visualization."""
        q = user_query.lower()
        if "people involved in multiple crimes" in q:
            # Returns people, crimes, and the PARTY_TO relationship
            return """
                MATCH (p:Person)-[r:PARTY_TO]->(c:Crime)
                WITH p, count(c) as num_crimes
                WHERE num_crimes > 1
                MATCH (p)-[r:PARTY_TO]->(c)
                RETURN p, r, c
                LIMIT 50
            """
        if "highest crime rates" in q or "areas" in q:
            # Returns locations, crimes, and OCCURRED_AT relationships
            return """
                MATCH (l:Location)<-[r:OCCURRED_AT]-(c:Crime)
                RETURN l, r, c
                ORDER BY l.name
                LIMIT 50
            """
        if "show all associates of" in q:
            name = q.split("show all associates of")[-1].strip().capitalize()
            return f"""
                MATCH (p:Person {{name: '{name}'}})-[r]-(a:Person)
                RETURN p, r, a
            """
        # Add more templates as needed
        return None

    def close(self):
        self.driver.close()

        
