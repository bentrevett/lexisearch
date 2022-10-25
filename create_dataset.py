from pathlib import Path
import webvtt
import tqdm
import json

def timestamp_to_seconds(timestamp):
    h, m, s = timestamp.split(":")
    s = s.split(".")[0]
    seconds = int(h) * 60*60 + int(m) * 60 + int(s)
    return seconds 

def parse_vtt(path):
    return [
        {
            "text": caption.text.strip(),
            "start_timestamp": caption.start,
            "end_timestamp": caption.end,
            "start": timestamp_to_seconds(caption.start),
            "end": timestamp_to_seconds(caption.end),
        }
        for caption in webvtt.read(path)
    ]

window = 6
stride = 3

data_paths = list(Path("data").glob("*"))
dataset_path = Path("dataset.jsonl")

with dataset_path.open("w") as f:
    pass

for path in tqdm.tqdm(data_paths):
    captions = parse_vtt(path)
    for i in range(0, len(captions), stride):
        i_end = min(len(captions)-1, i+window)
        text = ' '.join([c["text"] for c in captions[i:i_end]])
        start_timestamp, start = captions[i]["start_timestamp"], captions[i]["start"]
        end_timestamp, end = captions[i_end]["start_timestamp"], captions[i_end]["start"]
        id = path.stem
        example = {
            "text": text,
            "start_timestamp": start_timestamp,
            "start": start,
            "end_timestamp": end_timestamp,
            "end": end,
            "id": id,
        }
        with dataset_path.open("a") as f:
            f.write(f"{json.dumps(example)}\n")