from pathlib import Path
import requests
from bs4 import BeautifulSoup
import tqdm

paths = sorted([p for p in Path("vtt").glob("*") if "large" in p.stem])

for path in tqdm.tqdm(paths):
    episode_number = path.stem.split("_")[1]
    page = requests.get(f"https://karpathy.ai/lexicap/{episode_number:0>4}-large.html")
    soup = BeautifulSoup(page.content, "html.parser")
    youtube_link = soup.find_all("a")[1]["href"]
    youtube_id = youtube_link.split("=")[-1]
    Path("data").mkdir(exist_ok=True)
    with path.open("r") as f:
        transcription = f.read()
    with Path(f"data/{youtube_id}.vtt").open("w") as f:
        f.write(transcription)