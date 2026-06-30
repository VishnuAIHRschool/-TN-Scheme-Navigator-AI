def get_language_instruction(language: str) -> str:
    """
    Returns language instruction for final AI response.
    """

    if language == "Tamil":
        return """
        Respond fully in Tamil.
        Use simple, clear Tamil that a normal citizen can understand.
        Keep government scheme names in English if exact translation may confuse the user.
        Explain eligibility, benefit, how to apply, and source clearly.
        """

    if language == "Bilingual":
        return """
        Respond in both English and Tamil.
        First give a short English answer.
        Then provide the Tamil explanation below it.
        Keep the Tamil simple and citizen-friendly.
        """

    return """
    Respond in clear professional English.
    Keep the answer simple, structured, and citizen-friendly.
    """


def get_ui_text(language: str):
    """
    UI text dictionary for Streamlit labels.
    """

    if language == "Tamil":
        return {
            "page_title": "அறிவு வரைபட RAG உதவியாளர்",
            "intro": "இந்த பக்கம் ChromaDB Vector RAG மற்றும் Neo4j Knowledge Graph RAG இரண்டையும் பயன்படுத்துகிறது.",
            "question_label": "உங்கள் கேள்வியை கேளுங்கள்",
            "placeholder": "உதாரணம்: மாநில அரசு நிதியுதவி வழங்கும் திட்டங்கள் எவை?",
            "button": "Hybrid Graph RAG மூலம் கேளுங்கள்",
            "answer_heading": "AI பதில்",
            "sources_heading": "அதிகாரப்பூர்வ ஆதாரங்கள்",
        }

    if language == "Bilingual":
        return {
            "page_title": "Knowledge Graph RAG Assistant / அறிவு வரைபட உதவியாளர்",
            "intro": "This page uses both Vector RAG and Neo4j Graph RAG. / இந்த பக்கம் இரண்டு RAG முறைகளையும் பயன்படுத்துகிறது.",
            "question_label": "Ask your question / உங்கள் கேள்வியை கேளுங்கள்",
            "placeholder": "Example: Which schemes are sponsored by State? / மாநில அரசு நிதியுதவி வழங்கும் திட்டங்கள் எவை?",
            "button": "Ask Hybrid Graph RAG",
            "answer_heading": "Hybrid AI Answer / AI பதில்",
            "sources_heading": "Official Sources / அதிகாரப்பூர்வ ஆதாரங்கள்",
        }

    return {
        "page_title": "Knowledge Graph RAG Assistant",
        "intro": "This page uses both ChromaDB Vector RAG and Neo4j Knowledge Graph RAG.",
        "question_label": "Ask your Knowledge Graph question",
        "placeholder": "Example: Which schemes are sponsored by State?",
        "button": "Ask Hybrid Graph RAG",
        "answer_heading": "Hybrid AI Answer",
        "sources_heading": "Official References",
    }