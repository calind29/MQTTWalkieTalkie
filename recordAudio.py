from stmpy import Machine, Driver
from os import system
import os
import time

import pyaudio
import wave
import uuid

        
class Recorder:
    def __init__(self):
        self.recording = False
        self.chunk = 1024  # Record in chunks of 1024 samples
        self.sample_format = pyaudio.paInt16  # 16 bits per sample
        self.channels = 1
        self.fs = 44100  # Record at 44100 samples per second
        self.filename = str(uuid.uuid4()) + ".wav"
        self.p = pyaudio.PyAudio() 
        
    def record(self):
        stream = self.p.open(format=self.sample_format,
                channels=self.channels,
                rate=self.fs,
                frames_per_buffer=self.chunk,
                input=True)
        self.frames = []  # Initialize array to store frames
        # Store data in chunks for 3 seconds
        self.recording = True
        while self.recording:
            data = stream.read(self.chunk)
            self.frames.append(data)
        print("done recording")
        # Stop and close the stream 
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        self.p.terminate()
        
    def stop(self):
        print("stop")
        self.recording = False
    
    def process(self):
        print("processing")
        # Save the recorded data as a WAV file
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()

recorder = Recorder()
        
t0 = {'source': 'initial', 'target': 'ready'}
t1 = {'trigger': 'start', 'source': 'ready', 'target': 'recording'}
t2 = {'trigger': 'done', 'source': 'recording', 'target': 'processing'}
t3 = {'trigger': 'done', 'source': 'processing', 'target': 'ready'}

s_recording = {'name': 'recording', 'do': 'record()', "stop": "stop()"}
s_processing = {'name': 'processing', 'do': 'process()'}

stm = Machine(name='stm', transitions=[t0, t1, t2, t3], states=[s_recording, s_processing], obj=recorder)
recorder.stm = stm

driver = Driver()
driver.add_machine(stm)
driver.start()

def main():
    while True:
        print("driver started")
        driver.send('start', 'stm')
        print("sent start")
        choice = int(input("number: "))
        if choice == 1:
            driver.send('stop', 'stm')
            print("sent stop")

main()