from hybrid_rag_engine import ask_hybrid_ai


def main():
    question = "Which schemes are sponsored by State?"

    answer, sources = ask_hybrid_ai(question)

    print("Question:")
    print(question)

    print("\nHybrid RAG Answer:")
    print(answer)

    print("\nSources:")
    for source in sources:
        print(source)


if __name__ == "__main__":
    main()