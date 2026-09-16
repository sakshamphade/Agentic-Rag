from ddgs import DDGS

with DDGS() as ddgs:

    results = list(
        ddgs.text(
            "Who is Elon Musk",
            max_results=5
        )
    )

print(results)