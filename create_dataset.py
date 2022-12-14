import argparse
import io
import json
from pathlib import Path

import tqdm
import webvtt

import utils

parser = argparse.ArgumentParser()
parser.add_argument("--window", type=int, default=6)
parser.add_argument("--stride", type=int, default=3)
args = parser.parse_args()


def parse_vtt(vtt_str):
    return [
        {
            "text": caption.text.strip(),
            "start_timestamp": caption.start,
            "end_timestamp": caption.end,
            "start": utils.timestamp_to_seconds(caption.start),
            "end": utils.timestamp_to_seconds(caption.end),
        }
        for caption in webvtt.read_buffer(io.StringIO(vtt_str))
    ]


data_paths = list(Path("data").glob("*"))
dataset_path = Path("dataset.jsonl")

with dataset_path.open("w") as f:
    pass

for path in tqdm.tqdm(data_paths):
    with path.open("r") as f:
        contents = json.load(f)
    vtt_str = contents["transcript"]
    title = contents["title"]
    id = contents["id"]
    captions = parse_vtt(vtt_str)
    for i in range(0, len(captions), args.stride):
        i_end = min(len(captions) - 1, i + args.window)
        text = " ".join([c["text"] for c in captions[i:i_end]])
        start_timestamp, start = captions[i]["start_timestamp"], captions[i]["start"]
        end_timestamp, end = (
            captions[i_end]["start_timestamp"],
            captions[i_end]["start"],
        )
        id = path.stem
        example = {
            "text": text,
            "start_timestamp": start_timestamp,
            "start": start,
            "end_timestamp": end_timestamp,
            "end": end,
            "id": id,
            "title": title,
        }
        with dataset_path.open("a") as f:
            f.write(f"{json.dumps(example)}\n")
