import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    prob_distribution = {}

    if corpus[page]:
        for link in corpus:
            prob_distribution[link] = (1 - damping_factor) / len(corpus)
        for link in corpus[page]:
            prob_distribution[link] += damping_factor / len(corpus[page])
    else:
        for link in corpus:
            prob_distribution[link] = 1 / len(corpus)

    return prob_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pageranks = {}
    for page in corpus:
        pageranks[page] = 0

    page = random.choice(list(corpus.keys()))

    for i in range(2, n):
        prob_distribution = transition_model(corpus, page, damping_factor) 
        pageranks[page] += 1
        page = random.choices(list(prob_distribution.keys()),
                              list(prob_distribution.values()), k=1)[0]

    for page in pageranks:
        pageranks[page] /= n
    return pageranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    pageranks = {}
    distribution = {}
    
    for page in corpus:
        pageranks[page] = 1/N

    converged = False
    while not converged:
        converged = True
        for page in pageranks:
            distribution[page] = pageranks[page]
        for PAGE in pageranks:
            iterativeSum = 0
            for page in corpus:
                for links in corpus[page]:
                    if (PAGE == links):
                        iterativeSum += pageranks[page] / len(corpus[page])

            pageranks[PAGE] = (1-damping_factor)/N + damping_factor*iterativeSum
            if (abs(distribution[PAGE] - pageranks[PAGE]) > 0.001):
                converged = False

    return pageranks


if __name__ == "__main__":
    main()
