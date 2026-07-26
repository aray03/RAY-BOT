from ddgs import DDGS

# Always use DDGS as a context manager to handle connection cleanup
with DDGS() as ddgs:
    results = ddgs.text("brian david gilbert zelda timeline site:youtube.com", max_results=5)
    for result in results:
        print(f"Title: {result['title']}")
        print(f"URL: {result['href']}\n")
