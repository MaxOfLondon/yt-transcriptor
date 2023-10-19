# yt-transcriptor.py

## Description
`yt-transcriptor.py` retrieves YouTube user-supplied or automatic English subtitles with help of [YouTube Transcript/Subtitle API](https://github.com/jdepoix/youtube-transcript-api).
Transcript is then forged into sentences using [Deep Multilingual Punctuation Prediction](https://github.com/oliverguhr/deepmultilingualpunctuation) neural network and finally made available as a multi-line text or html formatted output that can be saved or used in a pipeline.

## Requirements
- 4.5G disk space
- git
- virtualenv
- python3.10+
- pip
- NVIDIA Graphics Card recommended for performance but not mandatory

## How to install
Ensure requirements are met then change directory where you want the project to be cloned into, i.e. `cd ~`

```sh
git clone https://github.com/MaxOfLondon/yt-transcriptor.git
cd yt-transcriptor
virtualenv -p 3.10 .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## How to use
```
$ python yt-transcriptor.py -h
usage: yt-transcriptor.py [-h] [--html] url

Extracts English transcript from YouTube video URL and makes it readable.

positional arguments:
  url         YouTube video URL

options:
  -h, --help  show this help message and exit
  --html      fomats output as html paragraphs
```

Example 1 - direct call:
```
$ python yt-transcriptor.py https://www.youtube.com/watch?v=8uEIBdjiX0I
[+] Fetching video transcript: 8uEIBdjiX0I
[+] Fetched in 0.77s
[+] Forming sentences
/home/max/Documents/dev/python/yt-transcriptor/.venv/lib/python3.10/site-packages/transformers/pipelines/token_classification.py:169: UserWarning: `grouped_entities` is deprecated and will be removed in version v5.0.0, defaulted to `aggregation_strategy="none"` instead.
  warnings.warn(
[+] Formed sentences in 30.12s
[Music].
Welcome to an exploration of a transformative Wellness practice: intermittent fasting.
...
```
The lines below `[+] Formed sentences in 30.12s` is the output of the program to stdout and it can be redirected to file instead, with, for example `python yt-transcriptor.py https://www.youtube.com/watch?v=8uEIBdjiX0I > transcript.txt`.

Example 2 - in a pipeline:
```
$ echo https://www.youtube.com/watch?v=8uEIBdjiX0I | python yt-transcriptor.py | awk '{print "Output: "$0}'
[+] Fetching video transcript: 8uEIBdjiX0I
[+] Fetched in 0.79s
[+] Forming sentences
/home/max/Documents/dev/python/yt-transcriptor/.venv/lib/python3.10/site-packages/transformers/pipelines/token_classification.py:169: UserWarning: `grouped_entities` is deprecated and will be removed in version v5.0.0, defaulted to `aggregation_strategy="none"` instead.
  warnings.warn(
[+] Formed sentences in 30.02s
Output: [Music].
Welcome to an exploration of a transformative Wellness practice: intermittent fasting.
...
```

To supress progress update redirect stderr to `/dev/null` or a log file, for example `python yt-transcriptor.py https://www.youtube.com/watch?v=ePXZguxYewI 2>/dev/null`
