import argparse

import datasets
import sentence_transformers

parser = argparse.ArgumentParser()
parser.add_argument("--query", type=str, required=True)
args = parser.parse_args()

model = sentence_transformers.SentenceTransformer(
    "sentence-transformers/multi-qa-mpnet-base-dot-v1", device="cuda"
)

dataset = datasets.load_dataset("json", data_files=["dataset.jsonl"], split="train")
dataset.load_faiss_index("embeddings", "index.faiss")

query_embedding = model.encode(args.query)
scores, retrieved_examples = dataset.get_nearest_examples(
    "embeddings", query_embedding, k=10
)

for score, example in zip(scores, retrieved_examples["text"]):
    print(score)
    print(example)
    print("*" * 100)
