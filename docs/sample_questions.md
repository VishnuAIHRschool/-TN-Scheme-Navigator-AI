# Sample Questions for Manual Evaluation

Use these to manually sanity-check retrieval quality and grounding after `ingest.py` and
`scrape_schemes.py` have been run. Expect every answer to name a real scheme from the CSV and
to say "not available" rather than guess when data is missing.

## English - Vector RAG leaning
- What schemes are available for farmers?
- What documents are required to apply for seed support?
- Is there any scheme for soil testing or soil health?

## English - Graph RAG leaning (relationships)
- Which schemes are sponsored by State?
- Which schemes are sponsored by Central government?
- Which schemes are for farmers and provide grants?
- Which schemes are connected to soil health?

## Tamil
- விவசாயிகளுக்கான திட்டங்கள் எவை?
- விவசாயிகளுக்கான மானிய திட்டங்கள் எவை?
- மாநில அரசு நிதியுதவி வழங்கும் திட்டங்கள் எவை?

## Vague / clarifying-question cases
These should make the assistant ask a follow-up question instead of guessing:
- I need help.
- What schemes are there?
- Tell me about subsidies.

## Out-of-scope / no-data cases
These should produce an explicit "not available in the retrieved scheme information" style
answer, not an invented one:
- What is the scheme for fishermen in Chennai?
- Is there a scheme for IT startups?
