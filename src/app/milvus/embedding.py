from sentence_transformers import SentenceTransformer
from numpy.typing import NDArray


text_embedding_model = SentenceTransformer(r"I:\distiluse-base-multilingual-cased-v2")


def text_embedding(text: str) -> NDArray:
    return text_embedding_model.encode(text, convert_to_numpy=True)
