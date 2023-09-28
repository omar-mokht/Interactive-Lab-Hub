import argparse
import queue
import sys
import sounddevice as sd
import json
import subprocess

from vosk import Model, KaldiRecognizer

q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text
    
def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        pass
        # print(status, file=sys.stderr)
    q.put(bytes(indata))

def process_sentence(sentence):
    return f'[Post Processed] {sentence}'

def speak_sentence(sentence):
    subprocess.check_output(f'./speech-scripts/googletts_arg.sh "{sentence}"', shell=True, stderr=subprocess.PIPE, universal_newlines=True)

    
device_info = sd.query_devices(None, "input")
# soundfile expects an int, sounddevice provides a float:
samplerate = int(device_info["default_samplerate"])
    
model = Model(lang="en-us")

with sd.RawInputStream(samplerate=samplerate, blocksize = 8000, device=1,
        dtype="int16", channels=1, callback=callback):
    print("#" * 80)
    print("Press Ctrl+C to stop the recording")
    print("#" * 80)

    rec = KaldiRecognizer(model, samplerate)
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            recognition = json.loads(rec.Result())["text"]
            print(recognition)
            # print(rec.Result())
            processed_sentence = process_sentence(recognition)
            print(processed_sentence)
            speak_sentence(processed_sentence)
        else:
            #print(rec.PartialResult())
            pass
