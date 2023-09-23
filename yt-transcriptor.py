from deepmultilingualpunctuation import PunctuationModel
from youtube_transcript_api import YouTubeTranscriptApi
from sys import stderr
import argparse
import re
import sys
import time

PATTERN_PUNCTUATION = re.compile(r'((?<=[\.\?!]\s)(\w+)|(^\w+))')
PATTERN_VIDEO_ID = re.compile(r'v=([\w]+)')
TERMINATORS = ['.', '!', '?']


def sentence_list(paragraph):
    end = True
    sentences = []
    while end > -1:
        end = find_sentence_end(paragraph)
        if end > -1:
            sentences.append(paragraph[end:].strip())
            paragraph = paragraph[:end]
    sentences.append(paragraph)
    sentences.reverse()
    return sentences


def find_sentence_end(paragraph):
    possible_endings = []
    sentence_terminators = TERMINATORS
    for sentence_terminator in sentence_terminators:
        t_indices = list(find_all(paragraph, sentence_terminator))
        possible_endings.extend(
            ([] if not len(t_indices)
                else [[i, len(sentence_terminator)] for i in t_indices]))
    if len(paragraph) in [pe[0] + pe[1] for pe in possible_endings]:
        max_end_start = max([pe[0] for pe in possible_endings])
        possible_endings = \
            [pe for pe in possible_endings
                if pe[0] != max_end_start]
    possible_endings = \
        [pe[0] + pe[1] for pe in possible_endings
            if sum(pe) > len(paragraph)
            or (sum(pe) < len(paragraph)
                and paragraph[sum(pe)] == ' ')]
    end = (-1 if not len(possible_endings) else max(possible_endings))
    return end


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)


def cap(match):
    return match.group().capitalize()


def fetch_transcript(video_id):
    print(f'[+] Fetching video transcript: {video_id}', file=stderr)
    try:
        start_time = time.time()
        ts = YouTubeTranscriptApi.get_transcript(video_id)
        text_list = [fragment.get('text') for fragment in ts]
        text = ' '.join(text_list)
        end_time = time.time()
        elapsed_time = end_time - start_time
    except Exception as e:
        print(
            f'[!] Failed to fetch transcript id {video_id} because of {e}',
            file=stderr)
        exit(1)
    print(f'[+] Fetched in {round(elapsed_time, 2)}s', file=stderr)
    return text


def form_sentences(text):
    print('[+] Forming sentences', file=stderr)
    try:
        start_time = time.time()
        model = PunctuationModel()
        punctuated = model.restore_punctuation(text)
        punctuated = PATTERN_PUNCTUATION.sub(cap, punctuated)
        end_time = time.time()
        elapsed_time = end_time - start_time
    except Exception as e:
        print(f'[!] Failed to form sentences because of {e}', file=stderr)
        exit(2)
    print(
        f'[+] Formed sentences in {round(elapsed_time, 2)}s',
        file=stderr)
    return punctuated


def html_paragraphs(lines):
    print('[+] Convering to html', file=stderr)
    start_time = time.time()
    html = '\n'.join(['<p>' + p.strip() + '</p>' for p in lines])
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'[+] Converted in {round(elapsed_time, 2)}s', file=stderr)
    return html


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extracts English transcript from YouTube video URL and \
            makes it readable.")
    parser.add_argument(
        'url',
        help="YouTube video URL",
        default=sys.stdin,
        nargs='?')
    parser.add_argument(
        '--html',
        action='store_true',
        default=False,
        help='fomats output as html paragraphs')
    return parser.parse_args()


def extract_video_id(url):
    result = PATTERN_VIDEO_ID.search(url)
    if result and result.group(1):
        return result.group(1)
    print(
        f'[!] Failed to extract video id from the link {url}',
        file=stderr)
    exit(3)


def input_url(url_object):
    if isinstance(url_object, str):
        return url_object
    else:
        return url_object.read().rstrip('\n')


def main():
    args = parse_args()
    args.url = input_url(args.url)
    video_id = extract_video_id(args.url)
    transcript = fetch_transcript(video_id)
    punctuated = form_sentences(transcript)
    line_list = sentence_list(punctuated)
    if args.html:
        html = (f'<p>{line}</p>\n' for line in line_list)
        for p in html:
            sys.stdout.write(p)
    else:
        para = (f'{line}\n' for line in line_list)
        for p in para:
            sys.stdout.write(p)


if __name__ == "__main__":
    main()
