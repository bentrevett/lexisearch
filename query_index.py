import argparse
import logging

import datasets
import sentence_transformers

import utils

logging.disable(logging.CRITICAL)

parser = argparse.ArgumentParser()
parser.add_argument("--query", type=str, required=True)
parser.add_argument("--k", type=int, default=10)
args = parser.parse_args()

model = sentence_transformers.SentenceTransformer(
    "sentence-transformers/multi-qa-mpnet-base-dot-v1", device="cuda"
)

dataset = datasets.load_dataset("json", data_files=["dataset.jsonl"], split="train")
dataset.load_faiss_index("embeddings", "index.faiss")

query_embedding = model.encode(args.query)
_, retrieved_examples = dataset.get_nearest_examples(
    "embeddings", query_embedding, k=10
)


for text, start, end, title, id in zip(
    retrieved_examples["text"],
    retrieved_examples["start_timestamp"],
    retrieved_examples["end_timestamp"],
    retrieved_examples["title"],
    retrieved_examples["id"],
):
    start = start.split(".")[0]
    end = end.split(".")[0]
    print(f"title: {title}")
    print(f"transcript: [{start}] {text}")
    print(f"link: https://youtu.be/{id}?t={utils.timestamp_to_seconds(start)}")
    print("*" * 88)
