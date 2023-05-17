import random
from fakeyou import FakeYou
import requests
from pydub import AudioSegment
import numpy as np
import librosa

fakeyou = FakeYou()

def get_track(text_path: str, beat_path: str, rap_start_ms: int):
    # rap_segment: AudioSegment = get_rap(text_path=text_path)
    rap_segment = AudioSegment.from_file("kanye_140.mp3")
    raw_filename = f"kanye_shine_raw_{random.randint(a=0, b=10000)}.mp3"
    rap_segment.export(raw_filename, format="mp3")

    y, sr = librosa.load(path=raw_filename)
    librosa.beat.tempo(y=y, sr=sr)

    beat_segment: AudioSegment = AudioSegment.from_file(beat_path)
    rap = beat_segment.overlay(rap_segment + 5, position=rap_start_ms)
    rap.export(f"kanye_shine_{random.randint(a=0, b=10000)}.mp3", format="mp3")
    
def get_rap(text_path: str):
    rap_segments = get_rap_segment(text_path=text_path)
    rap_segment: AudioSegment = AudioSegment.empty()
    for i in range(0, len(rap_segments)):
        rap_segment += rap_segments[i]        

    rap_filename = f"kanye_{random.randint(a=0, b=10000)}.mp3" 
    rap_segment.export(rap_filename, format="mp3")
    return rap_segment

def get_rap_segment(text_path: str):
    text_segments = split_text(text_path)  
    audio_segments = []
    for text_segment in text_segments:
        job_token = fakeyou.make_tts_job(text=text_segment, ttsModelToken="TM:1a7mjjxwq4js")
        job = fakeyou.tts_poll(job_token)
        response = requests.get(job.link)
        split = response.url.split("/")
        wav_filename = split[split.__len__() - 1]
        with open(wav_filename, "wb") as f:
            f.write(response.content)
        audio_segment = AudioSegment.from_file(wav_filename)
        audio_segments.append(audio_segment)
    return audio_segments

def split_text(path: str):
    text_split = []
    with open(path, "r") as f:
        text_split = f.readlines()  
    text_segments = []
    current_text = ""
    for line in text_split:
        if line == "\n":
            text_segments.append(current_text)
            current_text = ""
        else:
            current_text += line.replace("\n", "")
    text_segments.append(current_text)
    return text_segments

def generate_silent_segment(duration_ms):
    duration_ms = duration_ms
    audio_data = np.zeros(duration_ms, dtype=np.int16)
    audio_segment = AudioSegment(audio_data.tobytes(), frame_rate=44100, sample_width=2, channels=1)
    return audio_segment

def get_rap_duration(audio_segments):
    duration = 0
    for segment in audio_segments:
        duration += segment.__len__()
    return duration

get_track("text.txt", "shine.mp3", 50000)