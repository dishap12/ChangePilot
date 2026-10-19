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
