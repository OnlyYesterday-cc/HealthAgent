"""Offline BGE embeddings using local weights, CLS pooling and L2 normalization."""
from functools import lru_cache
from pathlib import Path

from app.core.config import get_settings

QUERY_PREFIX = "为这个句子生成表示以用于检索相关文章："


@lru_cache(maxsize=1)
def _load(model_path: str):
    import torch
    from transformers import AutoModel, AutoTokenizer

    path = Path(model_path)
    if not path.is_absolute():
        path = Path(__file__).resolve().parents[3] / path
    if not (path / "model.safetensors").is_file():
        raise RuntimeError(f"Local embedding weights missing: {path}")
    torch.set_num_threads(min(4, torch.get_num_threads()))
    tokenizer = AutoTokenizer.from_pretrained(path, local_files_only=True)
    model = AutoModel.from_pretrained(path, local_files_only=True, use_safetensors=True)
    model.eval()
    return tokenizer, model


def encode(texts: list[str], *, is_query: bool = False) -> list[list[float]]:
    import torch

    settings = get_settings()
    tokenizer, model = _load(settings.local_embedding_model_path)
    if model.config.hidden_size != settings.dashscope_embedding_dim:
        raise ValueError("Embedding dimension does not match local model; rebuild the index.")
    vectors = []
    for start in range(0, len(texts), 16):
        batch = texts[start:start + 16]
        if is_query:
            batch = [QUERY_PREFIX + text for text in batch]
        inputs = tokenizer(batch, padding=True, truncation=True, max_length=512, return_tensors="pt")
        with torch.inference_mode():
            output = model(**inputs).last_hidden_state[:, 0]
            output = torch.nn.functional.normalize(output, p=2, dim=1)
        vectors.extend(output.tolist())
    return vectors
