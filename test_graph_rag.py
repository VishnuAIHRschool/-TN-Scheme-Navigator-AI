from graph_rag_engine import ask_graph_ai


def main():
    questions = [
        "Which schemes are sponsored by State?",
        "Which schemes are for farmers?",
        "Which schemes provide grants?",
        "Which schemes are related to seed support?",
    ]

    for question in questions:
        print("\nQuestion:")
        print(question)

        print("\nGraph RAG Answer:")
        answer = ask_graph_ai(question)
        print(answer)

        print("-" * 80)


if __name__ == "__main__":
    main()