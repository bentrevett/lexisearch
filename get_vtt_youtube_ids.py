import json
from pathlib import Path

import requests
import tqdm
from bs4 import BeautifulSoup

paths = sorted([p for p in Path("vtt").glob("*") if "large" in p.stem])

for path in tqdm.tqdm(paths):
    episode_number = path.stem.split("_")[1]
    page = requests.get(f"https://karpathy.ai/lexicap/{episode_number:0>4}-large.html")
    soup = BeautifulSoup(page.content, "html.parser")
    youtube_title = soup.find_all("h2")[0].text
    youtube_url = soup.find_all("a")[1]["href"]
    youtube_id = youtube_url.split("=")[-1]
    Path("data").mkdir(exist_ok=True)
    with path.open("r") as f:
        transcript = f.read()
    with Path(f"data/{youtube_id}.json").open("w") as f:
        json.dump(
            {
                "title": youtube_title,
                "id": youtube_id,
                "transcript": transcript,
            },
            f,
            indent=2,
        )
