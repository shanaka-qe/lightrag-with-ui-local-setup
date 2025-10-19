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
        
        # Define entity type patterns for better detection
        self.entity_patterns = {
            'PERSON': {
                'titles': ['dr.', 'prof.', 'mr.', 'ms.', 'mrs.', 'ceo', 'cto', 'director', 'manager'],
                'roles': ['engineer', 'architect', 'developer', 'analyst', 'consultant', 'specialist', 'lead', 'head', 'chief', 'president'],
                'name_patterns': [r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', r'\bDr\. [A-Z][a-z]+\b', r'\bProf\. [A-Z][a-z]+\b']
            },
            'ORGANIZATION': {
                'keywords': ['company', 'organization', 'team', 'department', 'division', 'corporation', 'inc', 'llc', 'ltd', 'group', 'association', 'institute', 'foundation', 'agency', 'bureau', 'lab', 'research'],
                'known_orgs': ['mit', 'google', 'ibm', 'microsoft', 'amazon', 'stanford', 'aws', 'azure', 'cloud', 'platform', 'network', 'ai', 'quantum']
            },
            'TECHNOLOGY': {
                'keywords': ['react', 'tensorflow', 'python', 'javascript', 'java', 'docker', 'kubernetes', 'postgresql', 'redis', 'mongodb', 'next.js', 'fastapi', 'django', 'pytorch', 'scikit', 'oauth', 'jwt', 'ssl', 'tls', 'qiskit', 'cirq', 'pennylane', 'q#', 'qutip', 'openqasm'],
                'categories': ['framework', 'library', 'tool', 'software', 'application', 'database', 'server', 'cloud', 'infrastructure', 'system', 'api']
            },
            'LOCATION': {
                'keywords': ['san francisco', 'cambridge', 'london', 'singapore', 'austin', 'boulder', 'mountain view', 'zurich', 'tokyo', 'princeton', 'geneva', 'california', 'massachusetts', 'texas', 'colorado', 'switzerland', 'japan', 'new jersey', 'virginia', 'united kingdom'],
                'location_types': ['location', 'city', 'country', 'state', 'region', 'area', 'office', 'building', 'facility', 'headquarters', 'center', 'campus']
            },
            'PROJECT': {
                'keywords': ['phoenix', 'project', 'initiative', 'program', 'campaign', 'strategy', 'plan', 'proposal', 'implementation', 'development', 'transformation', 'digital', 'research', 'laboratory', 'quantum']
            },
            'CONCEPT': {
                'keywords': ['quantum', 'computing', 'ai', 'machine learning', 'algorithm', 'encryption', 'security', 'optimization', 'personalization', 'concept', 'idea', 'principle', 'methodology', 'approach', 'theory', 'model', 'framework', 'paradigm', 'philosophy', 'artificial intelligence', 'neural network', 'deep learning']
            }
        }
    
    def _detect_entity_type(self, node_id: str, combined_text: str, original_type: str) -> str:
        """
        Robust entity type detection using pattern matching
        
        Args:
            node_id: The node identifier
            combined_text: Combined node ID and description text
            original_type: Original entity type from LightRAG
            
        Returns:
            Detected entity type
        """
        import re
        
        # If we already have a good type from LightRAG, use it
        if original_type in ['person', 'organization', 'technology', 'location', 'project', 'concept']:
            return original_type.upper()
        
        # Order matters - check most specific patterns first
        
        # Location detection (very specific patterns)
        if self._is_location(combined_text):
            return 'LOCATION'
        
        # Project detection (specific keywords)
        if self._is_project(combined_text):
            return 'PROJECT'
        
        # Technology detection (specific tech terms)
        if self._is_technology(combined_text):
            return 'TECHNOLOGY'
        
        # Organization detection (specific org terms)
        if self._is_organization(combined_text):
            return 'ORGANIZATION'
        
        # Concept detection (abstract terms)
        if self._is_concept(combined_text):
            return 'CONCEPT'
        
        # Person detection (names and titles - check last to avoid false positives)
        if self._is_person(node_id, combined_text):
            return 'PERSON'
        
        return 'unknown'
    
    def _is_person(self, node_id: str, text: str) -> bool:
        """Check if entity is a person"""
        # Check for titles and roles
        person_indicators = self.entity_patterns['PERSON']['titles'] + self.entity_patterns['PERSON']['roles']
        if any(indicator in text for indicator in person_indicators):
            return True
        
        # Check for name patterns (First Last format)
        import re
        name_pattern = r'\b[A-Z][a-z]+ [A-Z][a-z]+\b'
        if re.search(name_pattern, node_id):
            return True
        
        return False
    
    def _is_organization(self, text: str) -> bool:
        """Check if entity is an organization"""
        org_keywords = self.entity_patterns['ORGANIZATION']['keywords'] + self.entity_patterns['ORGANIZATION']['known_orgs']
        return any(keyword in text for keyword in org_keywords)
    
    def _is_technology(self, text: str) -> bool:
        """Check if entity is a technology"""
        tech_keywords = self.entity_patterns['TECHNOLOGY']['keywords'] + self.entity_patterns['TECHNOLOGY']['categories']
        return any(keyword in text for keyword in tech_keywords)
    
    def _is_location(self, text: str) -> bool:
        """Check if entity is a location"""
        location_keywords = self.entity_patterns['LOCATION']['keywords'] + self.entity_patterns['LOCATION']['location_types']
        return any(keyword in text for keyword in location_keywords)
    
    def _is_project(self, text: str) -> bool:
        """Check if entity is a project"""
        return any(keyword in text for keyword in self.entity_patterns['PROJECT']['keywords'])
    
    def _is_concept(self, text: str) -> bool:
        """Check if entity is a concept"""
        return any(keyword in text for keyword in self.entity_patterns['CONCEPT']['keywords'])
    
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
            
            # Enhanced physics and styling configuration
            net.set_options("""
            {
                "physics": {
                    "enabled": true,
                    "barnesHut": {
                        "gravitationalConstant": -12000,
                        "centralGravity": 0.4,
                        "springLength": 120,
                        "springConstant": 0.05,
                        "damping": 0.12,
                        "avoidOverlap": 0.2
                    },
                    "minVelocity": 0.5,
                    "maxVelocity": 50,
                    "timestep": 0.35
                },
                "nodes": {
                    "font": {
                        "size": 14,
                        "face": "Arial",
                        "bold": true,
                        "color": "#2C3E50"
                    },
                    "borderWidth": 2,
                    "borderWidthSelected": 4,
                    "shadow": {
                        "enabled": true,
                        "color": "rgba(0,0,0,0.3)",
                        "size": 5,
                        "x": 2,
                        "y": 2
                    }
                },
                "edges": {
                    "smooth": {
                        "type": "continuous",
                        "forceDirection": "none",
                        "roundness": 0.2
                    },
                    "font": {
                        "size": 12,
                        "face": "Arial",
                        "color": "#2C3E50"
                    },
                    "shadow": {
                        "enabled": true,
                        "color": "rgba(0,0,0,0.2)",
                        "size": 3,
                        "x": 1,
                        "y": 1
                    }
                },
                "interaction": {
                    "hover": true,
                    "hoverConnectedEdges": true,
                    "selectConnectedEdges": true,
                    "tooltipDelay": 200
                },
                "layout": {
                    "improvedLayout": true,
                    "hierarchical": {
                        "enabled": false
                    }
                }
            }
            """)
            
            # Enhanced color scheme for different node types
            color_map = {
                'PERSON': '#FF4757',         # Vibrant red for people
                'ORGANIZATION': '#2ED573',    # Bright green for organizations
                'TECHNOLOGY': '#3742FA',     # Royal blue for tech
                'PROJECT': '#FF6348',        # Orange-red for projects
                'LOCATION': '#2F3542',       # Dark blue-gray for locations
                'CONCEPT': '#FFA502',        # Golden yellow for concepts
                'EVENT': '#9C88FF',         # Purple for events
                'PRODUCT': '#FF6B9D',        # Pink for products
                'SERVICE': '#70A1FF',       # Light blue for services
                'unknown': '#A4B0BE'        # Light gray for unknown
            }
            
            # Add nodes with colors based on type
            for node in G.nodes(data=True):
                node_id = node[0]
                node_data = node[1]
                
                # Enhanced entity type detection based on node content
                node_type = node_data.get('entity_type', 'unknown')
                description = node_data.get('description', '')
                node_id_lower = node_id.lower()
                description_lower = description.lower()
                
                # Combine node ID and description for better detection
                combined_text = f"{node_id_lower} {description_lower}"
                
                # Use robust entity type detection
                detected_type = self._detect_entity_type(node_id, combined_text, node_type)
                node_type = detected_type
                
                color = color_map.get(node_type, '#95A5A6')
                
                # Debug logging for entity detection
                logger.debug(f"Node: {node_id} | Type: {node_type} | Color: {color}")
                
                # Enhanced node styling with dynamic sizing and colors
                # Calculate node size based on connections (degree centrality)
                node_degree = G.degree(node_id)
                base_size = 20
                size_multiplier = min(3.0, 1.0 + (node_degree * 0.3))  # Cap at 3x size
                node_size = int(base_size * size_multiplier)
                
                # Simplified but effective node styling
                net.add_node(
                    node_id,
                    label=node_id,
                    title=f"<b>Type:</b> {node_type}<br><b>Connections:</b> {node_degree}<br><b>Description:</b> {description[:150]}...",
                    color=color,  # Use simple color assignment
                    size=node_size,
                    font={
                        'color': '#FFFFFF' if node_type in ['PERSON', 'ORGANIZATION', 'TECHNOLOGY'] else '#2C3E50',
                        'size': max(12, min(18, node_size // 2)),
                        'face': 'Arial',
                        'bold': True
                    },
                    borderWidth=2,
                    borderWidthSelected=4
                )
            
            # Add colorful edges with relationship types
            relationship_colors = {
                'works_at': '#E74C3C',      # Red for employment
                'located_in': '#3498DB',    # Blue for location
                'part_of': '#2ECC71',       # Green for membership
                'related_to': '#9B59B6',    # Purple for general relations
                'manages': '#F39C12',       # Orange for management
                'collaborates': '#1ABC9C',   # Teal for collaboration
                'depends_on': '#E67E22',    # Dark orange for dependencies
                'creates': '#8E44AD',       # Dark purple for creation
                'uses': '#16A085',          # Dark teal for usage
                'implements': '#D35400'     # Brown for implementation
            }
            
            for edge in G.edges(data=True):
                source = edge[0]
                target = edge[1]
                edge_data = edge[2]
                
                # Get relationship description and type
                description = edge_data.get('description', 'related to')
                relationship_type = edge_data.get('relationship_type', 'related_to')
                
                # Determine edge color based on relationship type
                edge_color = relationship_colors.get(relationship_type, '#95A5A6')
                
                # Calculate edge width based on relationship strength (if available)
                edge_width = edge_data.get('weight', 1.0)
                edge_width = max(1, min(5, int(edge_width * 2)))  # Scale to 1-5
                
                net.add_edge(
                    source,
                    target,
                    title=f"<b>Relationship:</b> {relationship_type}<br><b>Description:</b> {description}",
                    label=description[:25] if len(description) > 25 else description,
                    color={
                        'color': edge_color,
                        'highlight': '#FF6B6B',  # Pink highlight
                        'hover': '#4ECDC4'       # Teal hover
                    },
                    width=edge_width,
                    dashes=False,
                    arrows={
                        'to': {
                            'enabled': True,
                            'scaleFactor': 1.2,
                            'type': 'arrow'
                        }
                    }
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

