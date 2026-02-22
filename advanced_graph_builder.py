"""
Advanced Multi-Document Knowledge Graph Builder
================================================
Builds comprehensive knowledge graphs across multiple standards with:
1. Structural relationships (within documents)
2. Cross-document references (citations)
3. Semantic similarity links (related content)
4. Definition relationships (terms and usage)
"""

import sys
import json
import hashlib
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from difflib import SequenceMatcher

# UTF-8 encoding for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


class AdvancedGraphBuilder:
    """Build comprehensive multi-document knowledge graph."""

    def __init__(self, verbose=True):
        self.verbose = verbose
        self.nodes = {}
        self.edges = []
        self.all_chunks = []  # All chunks from all documents
        self.documents = {}  # document_id -> chunks
        self.definitions = {}  # term -> node_id
        self.verification_log = []

    def log(self, message: str, level="INFO"):
        """Log message."""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        entry = f"[{timestamp}] [{level}] {message}"
        self.verification_log.append(entry)
        if self.verbose:
            print(entry)

    def calculate_hash(self, text: str) -> str:
        """Calculate SHA-256 hash."""
        return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]

    def generate_node_id(self, document_id: str, chunk_id: str, node_type: str) -> str:
        """Generate deterministic node ID."""
        doc = document_id.replace("/", "_").replace(" ", "_")
        chunk = str(chunk_id).replace(".", "_")
        return f"{doc}_{node_type}_{chunk}"

    def load_all_documents(self, chunks_base_dir: Path):
        """Load all standards from chunks directory."""
        self.log("="*80)
        self.log("PHASE 1: LOADING ALL DOCUMENTS")
        self.log("="*80)

        for doc_dir in sorted(chunks_base_dir.iterdir()):
            if not doc_dir.is_dir():
                continue

            document_id = doc_dir.name
            self.log(f"\n📁 Loading: {document_id}")

            doc_chunks = []
            json_files = sorted(doc_dir.glob("*.json"))

            for json_file in json_files:
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        chunk = json.load(f)
                        chunk['_source_file'] = str(json_file)
                        doc_chunks.append(chunk)
                        self.all_chunks.append(chunk)
                except Exception as e:
                    self.log(f"✗ Failed to load {json_file}: {e}", "ERROR")

            self.documents[document_id] = doc_chunks
            self.log(f"✓ Loaded {len(doc_chunks)} chunks from {document_id}")

        self.log(f"\n✅ LOADED {len(self.all_chunks)} total chunks from {len(self.documents)} documents")
        return len(self.all_chunks)

    def build_standard_nodes(self):
        """Create standard (root) nodes for each document."""
        self.log("\n" + "="*80)
        self.log("PHASE 2: CREATING STANDARD NODES")
        self.log("="*80 + "\n")

        for document_id in self.documents.keys():
            node_id = f"STANDARD_{document_id}"
            node = {
                "id": node_id,
                "type": "Standard",
                "document_id": document_id,
                "label": document_id.replace("_", " "),
                "created_at": datetime.now().isoformat()
            }
            self.nodes[node_id] = node
            self.log(f"✓ Created Standard: {node_id}")

    def build_clause_nodes(self):
        """Create clause nodes from all chunks."""
        self.log("\n" + "="*80)
        self.log(f"PHASE 3: CREATING CLAUSE NODES ({len(self.all_chunks)} chunks)")
        self.log("="*80 + "\n")

        for idx, chunk in enumerate(self.all_chunks, 1):
            chunk_id = chunk.get('chunk_id')
            document_id = chunk.get('document_id')
            title = chunk.get('title', 'Untitled')
            parent_id = chunk.get('parent_id')
            level = chunk.get('level', 1)

            # Extract full text
            content_parts = chunk.get('content', [])
            full_text = " ".join([c.get('text', '') for c in content_parts])
            text_hash = self.calculate_hash(full_text)

            # Generate node ID
            node_id = self.generate_node_id(document_id, chunk_id, "CLAUSE")

            # Create clause node
            node = {
                "id": node_id,
                "type": "Clause",
                "clause_id": chunk_id,
                "document_id": document_id,
                "title": title,
                "level": level,
                "parent_id": parent_id,
                "text": full_text[:500],
                "full_text": full_text,
                "text_hash": text_hash,
                "source_file": chunk.get('_source_file', ''),
                "chunk_index": idx
            }

            self.nodes[node_id] = node

            if idx % 50 == 0:
                self.log(f"✓ [{idx}/{len(self.all_chunks)}] Created {idx} clauses...")

        self.log(f"\n✅ Created {len(self.all_chunks)} CLAUSE nodes")

    def build_requirement_nodes(self):
        """Extract requirements and create requirement nodes."""
        self.log("\n" + "="*80)
        self.log("PHASE 4: EXTRACTING REQUIREMENT NODES")
        self.log("="*80 + "\n")

        req_count = 0

        for chunk in self.all_chunks:
            chunk_id = chunk.get('chunk_id')
            document_id = chunk.get('document_id')
            requirements = chunk.get('requirements', [])

            if not requirements:
                continue

            for req_idx, req in enumerate(requirements, 1):
                req_text = req.get('text', '')
                req_type = req.get('type', 'unknown')
                req_keyword = req.get('keyword', '')

                # Generate requirement ID
                req_id = self.generate_node_id(
                    document_id,
                    f"{chunk_id}_REQ{req_idx:02d}",
                    "REQ"
                )

                # Create requirement node
                node = {
                    "id": req_id,
                    "type": "Requirement",
                    "requirement_type": req_type,
                    "keyword": req_keyword,
                    "text": req_text,
                    "text_hash": self.calculate_hash(req_text),
                    "parent_clause": chunk_id,
                    "document_id": document_id,
                    "obligation_level": self._get_obligation_level(req_keyword)
                }

                self.nodes[req_id] = node
                req_count += 1

        self.log(f"✅ Created {req_count} REQUIREMENT nodes")

    def _get_obligation_level(self, keyword: str) -> str:
        """Map requirement keyword to obligation level."""
        mapping = {
            'shall': 'MANDATORY',
            'must': 'MANDATORY',
            'should': 'RECOMMENDED',
            'may': 'OPTIONAL',
            'can': 'OPTIONAL'
        }
        return mapping.get(keyword.lower(), 'UNKNOWN')

    def build_structural_edges(self):
        """Create edges for document structure."""
        self.log("\n" + "="*80)
        self.log("PHASE 5: CREATING STRUCTURAL EDGES")
        self.log("="*80 + "\n")

        edge_count = 0

        # Get all standard nodes
        standard_nodes = {n['document_id']: nid
                         for nid, n in self.nodes.items()
                         if n['type'] == 'Standard'}

        # Connect clauses to standards or parent clauses
        for node_id, node in self.nodes.items():
            if node['type'] != 'Clause':
                continue

            document_id = node['document_id']
            parent_clause_id = node.get('parent_id')

            if parent_clause_id:
                # Find parent clause node
                parent_node_id = self._find_clause_node_by_id(parent_clause_id, document_id)
                if parent_node_id:
                    edge = (parent_node_id, node_id, "HAS_SUBCLAUSE")
                    self.edges.append(edge)
                    edge_count += 1
            else:
                # Connect to standard root
                standard_id = standard_nodes.get(document_id)
                if standard_id:
                    edge = (standard_id, node_id, "HAS_CLAUSE")
                    self.edges.append(edge)
                    edge_count += 1

        # Connect requirements to clauses
        for node_id, node in self.nodes.items():
            if node['type'] != 'Requirement':
                continue

            parent_clause_id = node.get('parent_clause')
            document_id = node['document_id']
            parent_node_id = self._find_clause_node_by_id(parent_clause_id, document_id)

            if parent_node_id:
                edge = (parent_node_id, node_id, "CONTAINS_REQUIREMENT")
                self.edges.append(edge)
                edge_count += 1

        self.log(f"✅ Created {edge_count} structural edges")

    def _find_clause_node_by_id(self, clause_id: str, document_id: str) -> str:
        """Find clause node ID by chunk_id and document_id."""
        for node_id, node in self.nodes.items():
            if (node['type'] == 'Clause' and
                node.get('clause_id') == clause_id and
                node.get('document_id') == document_id):
                return node_id
        return None

    def detect_cross_references(self):
        """Detect and create cross-document reference links."""
        self.log("\n" + "="*80)
        self.log("PHASE 6: DETECTING CROSS-DOCUMENT REFERENCES")
        self.log("="*80 + "\n")

        # Common reference patterns
        patterns = [
            r'EN\s+\d+[-\d]*',  # EN 50174-2, EN 50173-1
            r'BS\s+EN\s+\d+[-\d]*',  # BS EN 50174-2
            r'IEC\s+\d+[-\d]*',  # IEC 60050-151
            r'ISO\s+\d+[-\d]*',  # ISO 9001
        ]

        ref_count = 0
        clause_nodes = [n for n in self.nodes.values() if n['type'] == 'Clause']

        for node in clause_nodes:
            full_text = node.get('full_text', '')

            # Extract all references
            refs = set()
            for pattern in patterns:
                matches = re.findall(pattern, full_text, re.IGNORECASE)
                refs.update([m.strip() for m in matches])

            # Find matching documents
            for ref in refs:
                # Normalize reference
                ref_normalized = ref.replace(" ", "_").replace(":", "").upper()

                # Find matching document
                for doc_id in self.documents.keys():
                    doc_normalized = doc_id.replace("_", "").upper()

                    if doc_normalized in ref_normalized or ref_normalized in doc_normalized:
                        # Create reference edge
                        standard_id = f"STANDARD_{doc_id}"
                        if standard_id in self.nodes:
                            edge = (node['id'], standard_id, "REFERENCES")
                            self.edges.append(edge)
                            ref_count += 1

        self.log(f"✅ Created {ref_count} CROSS-REFERENCE edges")

    def detect_semantic_similarities(self, similarity_threshold=0.4, max_links=100):
        """Detect semantically similar clauses across documents."""
        self.log("\n" + "="*80)
        self.log("PHASE 7: DETECTING SEMANTIC SIMILARITIES")
        self.log("="*80 + "\n")

        clause_nodes = [n for n in self.nodes.values() if n['type'] == 'Clause']
        sim_count = 0

        self.log(f"Analyzing {len(clause_nodes)} clauses for similarities...")

        for i, node1 in enumerate(clause_nodes):
            if sim_count >= max_links:
                break

            # Only compare across different documents
            for node2 in clause_nodes[i+1:]:
                if node1['document_id'] == node2['document_id']:
                    continue

                # Calculate similarity
                text1 = node1.get('full_text', '')
                text2 = node2.get('full_text', '')

                if not text1 or not text2:
                    continue

                similarity = self._calculate_similarity(text1, text2)

                if similarity >= similarity_threshold:
                    edge = (node1['id'], node2['id'], "SIMILAR_TO")
                    self.edges.append(edge)
                    sim_count += 1

                    if sim_count % 10 == 0:
                        self.log(f"  Found {sim_count} similar clause pairs...")

                    if sim_count >= max_links:
                        break

        self.log(f"✅ Created {sim_count} SIMILARITY edges")

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity using keyword overlap."""
        # Simplified similarity: use keyword overlap
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        # Filter common words
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at',
                       'to', 'for', 'of', 'with', 'by', 'from', 'is', 'are',
                       'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had'}

        words1 = words1 - common_words
        words2 = words2 - common_words

        if not words1 or not words2:
            return 0.0

        intersection = len(words1 & words2)
        union = len(words1 | words2)

        return intersection / union if union > 0 else 0.0

    def build_graph(self, chunks_base_dir: Path):
        """Main orchestration method."""
        self.log("\n" + "="*80)
        self.log("ADVANCED MULTI-DOCUMENT KNOWLEDGE GRAPH BUILDER")
        self.log("="*80 + "\n")

        # Step 1: Load all documents
        chunk_count = self.load_all_documents(chunks_base_dir)
        if chunk_count == 0:
            self.log("❌ No chunks loaded. Aborting.", "ERROR")
            return False

        # Step 2: Build standard nodes
        self.build_standard_nodes()

        # Step 3: Build clause nodes
        self.build_clause_nodes()

        # Step 4: Build requirement nodes
        self.build_requirement_nodes()

        # Step 5: Build structural edges
        self.build_structural_edges()

        # Step 6: Detect cross-references
        self.detect_cross_references()

        # Step 7: Detect semantic similarities
        self.detect_semantic_similarities(similarity_threshold=0.3, max_links=200)

        # Summary
        self.print_summary()

        return True

    def print_summary(self):
        """Print build summary."""
        self.log("\n" + "="*80)
        self.log("ADVANCED GRAPH BUILD SUMMARY")
        self.log("="*80)

        # Document statistics
        self.log("\nDOCUMENT STATISTICS:")
        for doc_id, chunks in sorted(self.documents.items()):
            self.log(f"  {doc_id:30s}: {len(chunks):4d} chunks")

        # Node statistics
        node_types = defaultdict(int)
        for node in self.nodes.values():
            node_types[node['type']] += 1

        self.log("\nNODE STATISTICS:")
        for ntype, count in sorted(node_types.items()):
            self.log(f"  {ntype:20s}: {count:4d} nodes")
        self.log(f"  {'TOTAL':20s}: {len(self.nodes):4d} nodes")

        # Edge statistics
        edge_types = defaultdict(int)
        for _, _, rel in self.edges:
            edge_types[rel] += 1

        self.log("\nEDGE STATISTICS:")
        for etype, count in sorted(edge_types.items()):
            self.log(f"  {etype:30s}: {count:4d} edges")
        self.log(f"  {'TOTAL':30s}: {len(self.edges):4d} edges")

        self.log("\n" + "="*80 + "\n")

    def export_to_json(self, output_path: Path):
        """Export graph to JSON format."""
        self.log(f"\n📝 Exporting graph to JSON: {output_path}")

        graph_data = {
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "node_count": len(self.nodes),
                "edge_count": len(self.edges),
                "document_count": len(self.documents),
                "chunk_count": len(self.all_chunks)
            },
            "documents": list(self.documents.keys()),
            "nodes": list(self.nodes.values()),
            "edges": [
                {"source": s, "target": t, "relationship": r}
                for s, t, r in self.edges
            ]
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, indent=2, ensure_ascii=False)

        self.log(f"✓ Exported to {output_path}")

    def export_verification_log(self, output_path: Path):
        """Export verification log."""
        self.log(f"\n📝 Exporting verification log: {output_path}")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(self.verification_log))

        self.log(f"✓ Exported verification log with {len(self.verification_log)} entries")


def main():
    """Run the advanced graph builder."""
    chunks_dir = Path("chunks")

    if not chunks_dir.exists():
        print(f"❌ Error: Directory not found: {chunks_dir}")
        return

    # Build graph
    builder = AdvancedGraphBuilder(verbose=True)
    success = builder.build_graph(chunks_dir)

    if success:
        # Export outputs
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        builder.export_to_json(output_dir / "advanced_graph.json")
        builder.export_verification_log(output_dir / "advanced_build_log.txt")

        print(f"\n✅ SUCCESS! Advanced graph built and exported")
        print(f"   - Documents: {len(builder.documents)}")
        print(f"   - Nodes: {len(builder.nodes)}")
        print(f"   - Edges: {len(builder.edges)}")
    else:
        print("\n❌ FAILED to build graph")


if __name__ == "__main__":
    main()
