"""
Knowledge Graph Visualization Module
Handles visualization of LightRAG knowledge graphs using PyVis
"""

import logging
from typing import Optional, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class GraphVisualizer:
    """
    Handles knowledge graph visualization
    Creates interactive HTML visualizations using PyVis
    """
    
    def __init__(self, working_dir: str = "data/rag_workspace"):
        """
        Initialize graph visualizer
        
        Args:
            working_dir: Directory containing the knowledge graph files
        """
        self.working_dir = Path(working_dir)
    
    def generate_visualization(self) -> Optional[str]:
        """
        Generate interactive HTML visualization of the knowledge graph
        
        Returns:
            HTML string for interactive graph or None if no graph exists
        """
        try:
            import networkx as nx
            from pyvis.network import Network
            
            # Path to the graph file created by LightRAG
            graph_path = self.working_dir / "graph_chunk_entity_relation.graphml"
            
            if not graph_path.exists():
                logger.warning("No knowledge graph file found")
                return None
            
            # Load the graph using NetworkX
            G = nx.read_graphml(str(graph_path))
            
            # Check if graph is empty
            if len(G.nodes()) == 0:
                logger.warning("Knowledge graph is empty")
                return None
            
            logger.info(f"Loaded graph with {len(G.nodes())} nodes and {len(G.edges())} edges")
            
            # Create a PyVis network for interactive visualization
            net = Network(
                height="600px",
                width="100%",
                bgcolor="#ffffff",
                font_color="#000000",
                notebook=False,
                directed=False
            )
            
            # Configure physics for better layout
            net.set_options("""
            {
                "physics": {
                    "enabled": true,
                    "barnesHut": {
                        "gravitationalConstant": -8000,
                        "centralGravity": 0.3,
                        "springLength": 95,
                        "springConstant": 0.04,
                        "damping": 0.09,
                        "avoidOverlap": 0.1
                    },
                    "minVelocity": 0.75
                },
                "nodes": {
                    "font": {
                        "size": 14
                    }
                },
                "edges": {
                    "smooth": {
                        "type": "continuous"
                    }
                }
            }
            """)
            
            # Color scheme for different node types
            color_map = {
                'PERSON': '#FF6B6B',         # Red for people
                'ORGANIZATION': '#4ECDC4',   # Teal for organizations
                'TECHNOLOGY': '#45B7D1',     # Blue for tech
                'PROJECT': '#FFA07A',        # Light orange for projects
                'LOCATION': '#98D8C8',       # Green for locations
                'unknown': '#95A5A6'         # Gray for unknown
            }
            
            # Add nodes with colors based on type
            for node in G.nodes(data=True):
                node_id = node[0]
                node_data = node[1]
                
                # Determine node type and color
                node_type = node_data.get('entity_type', 'unknown')
                description = node_data.get('description', '').lower()
                
                # Try to infer type from description if not set
                if node_type == 'unknown':
                    if any(word in description for word in ['person', 'dr.', 'engineer', 'architect']):
                        node_type = 'PERSON'
                    elif any(word in description for word in ['company', 'organization', 'team']):
                        node_type = 'ORGANIZATION'
                    elif any(word in description for word in ['technology', 'framework', 'api', 'system']):
                        node_type = 'TECHNOLOGY'
                    elif any(word in description for word in ['project', 'initiative']):
                        node_type = 'PROJECT'
                
                color = color_map.get(node_type, '#95A5A6')
                
                # Add node with styling
                net.add_node(
                    node_id,
                    label=node_id,
                    title=f"Type: {node_type}\n{description[:200]}",
                    color=color,
                    size=25
                )
            
            # Add edges
            for edge in G.edges(data=True):
                source = edge[0]
                target = edge[1]
                edge_data = edge[2]
                
                # Get relationship description
                description = edge_data.get('description', 'related to')
                
                net.add_edge(
                    source,
                    target,
                    title=description,
                    label=description[:30] if len(description) > 30 else description
                )
            
            # Generate HTML
            html = net.generate_html()
            
            logger.info("Graph visualization generated successfully")
            return html
            
        except Exception as e:
            logger.error(f"Failed to generate graph visualization: {e}")
            return None
    
    def get_graph_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the knowledge graph
        
        Returns:
            Dictionary with graph statistics
        """
        try:
            import networkx as nx
            
            # Path to the graph file
            graph_path = self.working_dir / "graph_chunk_entity_relation.graphml"
            
            if not graph_path.exists():
                return {
                    "exists": False,
                    "nodes": 0,
                    "edges": 0,
                    "message": "No knowledge graph found. Please ingest documents first."
                }
            
            # Load and analyze the graph
            G = nx.read_graphml(str(graph_path))
            
            # Calculate statistics
            stats = {
                "exists": True,
                "nodes": len(G.nodes()),
                "edges": len(G.edges()),
                "density": nx.density(G) if len(G.nodes()) > 0 else 0,
                "connected_components": nx.number_connected_components(G.to_undirected()) if len(G.nodes()) > 0 else 0
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get graph stats: {e}")
            return {
                "exists": False,
                "error": str(e)
            }

