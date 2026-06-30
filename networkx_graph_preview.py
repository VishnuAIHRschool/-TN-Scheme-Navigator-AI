import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

CSV_PATH = "data/tn_scheme_details.csv"
OUTPUT_IMAGE = "data/knowledge_graph_preview.png"


def clean(value):
    if pd.isna(value):
        return ""
    return str(value).strip()


def add_edge_if_value(graph, source, target, relation):
    if source and target:
        graph.add_node(source, node_type="Scheme")
        graph.add_node(target, node_type=relation)
        graph.add_edge(source, target, relation=relation)


def main():
    if not os.path.exists(CSV_PATH):
        print("CSV file not found. Run python scrape_schemes.py first.")
        return

    df = pd.read_csv(CSV_PATH)

    graph = nx.Graph()

    for _, row in df.iterrows():
        scheme = clean(row.get("scheme_title"))
        department = clean(row.get("concerned_department"))
        beneficiary = clean(row.get("beneficiaries"))
        benefit_type = clean(row.get("types_of_benefits"))
        sponsor = clean(row.get("sponsored_by"))

        add_edge_if_value(graph, scheme, department, "Department")
        add_edge_if_value(graph, scheme, beneficiary, "Beneficiary")
        add_edge_if_value(graph, scheme, benefit_type, "BenefitType")
        add_edge_if_value(graph, scheme, sponsor, "Sponsor")

    print("NetworkX Knowledge Graph Summary")
    print("--------------------------------")
    print(f"Total nodes: {graph.number_of_nodes()}")
    print(f"Total edges: {graph.number_of_edges()}")
    print(f"Connected components: {nx.number_connected_components(graph)}")

    plt.figure(figsize=(18, 12))
    pos = nx.spring_layout(graph, seed=42, k=0.75)

    nx.draw_networkx_nodes(
        graph,
        pos,
        node_size=900,
        alpha=0.85
    )

    nx.draw_networkx_edges(
        graph,
        pos,
        alpha=0.35
    )

    nx.draw_networkx_labels(
        graph,
        pos,
        font_size=7
    )

    plt.title("TN Scheme Navigator AI - Knowledge Graph Preview")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(OUTPUT_IMAGE, dpi=200)
    plt.close()

    print(f"Graph preview saved to: {OUTPUT_IMAGE}")


if __name__ == "__main__":
    main()