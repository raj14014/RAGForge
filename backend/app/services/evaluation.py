def precision_at_k(retrieved, relevant, k):
    if k <= 0:
        return 0.0

    retrieved_k = set(retrieved[:k])
    relevant_set = set(relevant)

    return len(retrieved_k & relevant_set) / k


def recall_at_k(retrieved, relevant, k):
    relevant_set = set(relevant)

    if not relevant_set:
        return 0.0

    retrieved_k = set(retrieved[:k])

    return len(retrieved_k & relevant_set) / len(relevant_set)


def hit_rate(retrieved, relevant, k):
    retrieved_k = set(retrieved[:k])
    relevant_set = set(relevant)

    return 1.0 if retrieved_k & relevant_set else 0.0


def mrr(retrieved, relevant):
    relevant_set = set(relevant)

    for index, item in enumerate(retrieved, 1):
        if item in relevant_set:
            return 1.0 / index

    return 0.0


def citation_accuracy(citations):
    if not citations:
        return 0.0

    cited = [
        citation
        for citation in citations
        if citation.get("verification") == "supported"
    ]

    return len(cited) / len(citations)


def unsupported_claim_rate(answer, citations):
    if not answer:
        return 0.0

    if not citations:
        return 1.0

    supported_ids = {
        int(citation["citation_id"].strip("[]"))
        for citation in citations
        if citation.get("verification") == "supported"
    }

    claims = answer.split(".")
    material_claims = [
        claim.strip()
        for claim in claims
        if claim.strip()
    ]

    if not material_claims:
        return 0.0

    unsupported = 0

    for claim in material_claims:
        citation_ids = [
            int(x)
            for x in __import__("re").findall(
                r"\[(\d+)\]",
                claim
            )
        ]

        if not citation_ids:
            unsupported += 1
            continue

        if not any(cid in supported_ids for cid in citation_ids):
            unsupported += 1

    return unsupported / len(material_claims)