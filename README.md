# lexisearch

Use semantic similarity models to query transcriptions from the [Lex Fridman Podcast](https://lexfridman.com/podcast/).

Transcriptions were obtained from [lexicap](https://karpathy.ai/lexicap/) using [Whisper](https://github.com/openai/whisper).

Inspired by: https://www.youtube.com/watch?v=vpU_6x3jowg

## HOWTO

Create the dataset used to build the index:

`create_dataset.py`

Build and save the index:

`create_index.py`

Afterwards, the index can be queried with, e.g.:

`query_index.py --query "What is the meaning of life?"`

This will get the top ten most semantically similar transcription windows, along with links to the podcast episode on YouTube at those timestamps.
