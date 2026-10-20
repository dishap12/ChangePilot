"""Transparent, local TF-IDF retrieval over requirement-sized chunks."""
from dataclasses import dataclass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Requirement


@dataclass(frozen=True)
class Hit:
    requirement: Requirement
    score: float


def search_requirements(query: str, requirements: list[Requirement], top_k: int = 4,
                        min_score: float = 0.06) -> list[Hit]:
    if not requirements or not query.strip():
        return []
    corpus = [r.text + " " + r.id for r in requirements]
    try:
        vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), sublinear_tf=True)
        matrix = vec.fit_transform(corpus + [query])
        similarities = cosine_similarity(matrix[-1], matrix[:-1])[0]
    except ValueError:  # Empty vocabulary
        return []
    ranked = sorted(enumerate(similarities), key=lambda item: (-item[1], requirements[item[0]].id))
    return [Hit(requirements[i], round(float(score), 3)) for i, score in ranked[:top_k] if score >= min_score]


def offline_response(hits: list[Hit]) -> str:
    if not hits:
        return "No sufficiently similar requirement found. Rephrase the question or inspect the source documents."
    return "\n\n".join(f"**[{h.requirement.id}]** {h.requirement.text}" for h in hits) + \
        "\n\n*These are retrieved excerpts, not an AI-generated conclusion. Review the linked requirements before deciding.*"


def semantic_search_requirements(query: str, requirements: list[Requirement],
                                 api_key: str, top_k: int = 4,
                                 model: str = "text-embedding-3-small") -> list[Hit]:
    """Optional hosted semantic embedding retrieval for explicit local opt-in.

    This mode sends the question and current requirement texts to the API.
    It is intentionally unavailable to the public, synthetic-only demo.
    No embedding indices or sensitive documents are persisted.
    """
    if not query.strip() or not requirements:
        return []
    if not api_key.strip():
        raise ValueError("An API key is required for semantic retrieval.")
    import numpy as np
    from openai import OpenAI
    texts = [query] + [r.text for r in requirements]
    response = OpenAI(api_key=api_key).embeddings.create(
        model=model, input=texts,
    )
    embeddings = np.asarray([row.embedding for row in sorted(response.data, key=lambda x: x.index)],
                            dtype=float)
    norms = np.linalg.norm(embeddings, axis=1)
    norms[norms == 0] = 1
    normalized = embeddings / norms[:, None]
    similarity = normalized[1:] @ normalized[0]
    ranked = sorted(enumerate(similarity), key=lambda t: (-float(t[1]), requirements[t[0]].id))
    return [Hit(requirements[i], round(float(score), 3)) for i, score in ranked[:top_k]]
