from hybrid_rag_engine import ask_hybrid_ai


def main():
    questions = [
        ("Which schemes are sponsored by State?", "English"),
        ("மாநில அரசு நிதியுதவி வழங்கும் திட்டங்கள் எவை?", "Tamil"),
        ("Which schemes are for farmers and provide grants?", "Bilingual"),
    ]

    for question, language in questions:
        print("\nQuestion:")
        print(question)

        print("\nLanguage:")
        print(language)

        answer, sources, route = ask_hybrid_ai(question, language)

        print("\nRoute Used:")
        print(route)

        print("\nAnswer:")
        print(answer)

        print("\nSources:")
        for source in sources:
            print(source)

        print("-" * 100)


if __name__ == "__main__":
    main()