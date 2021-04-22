from threading import Thread

import paho.mqtt.client as mqtt
broker, port = "mqtt.item.ntnu.no", 1883
channel = "team13"

from stmpy import Machine, Driver
from os import system
import os
import pyaudio
import wave

        
class Player:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect(broker, port)
        self.client.subscribe(channel)
        self.filename = 'audio_files/output_audio/output.wav'

        try:
            thread = Thread(target=self.client.loop_forever)
            thread.start()
        except KeyboardInterrupt:
            print("Interrupted")
            self.client.disconnect()

    def on_message(self, client, userdata, msg):
        print("on_message(): topic: {}".format(msg.topic))

        f = open(self.filename, 'wb')
        f.write(msg.payload)
        f.close()
    
        
    def play(self):
        # Set chunk size of 1024 samples per data frame
        chunk = 1024  

        # Open the sound file 
        wf = wave.open(self.filename, 'rb')

        # Create an interface to PortAudio
        p = pyaudio.PyAudio()

        # Open a .Stream object to write the WAV file to
        # 'output = True' indicates that the sound will be played rather than recorded
        stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                        channels = wf.getnchannels(),
                        rate = wf.getframerate(),
                        output = True)

        # Read data in chunks
        data = wf.readframes(chunk)

        # Play the sound by writing the audio data to the stream
        while data != '':
            stream.write(data)
            data = wf.readframes(chunk)

        # Close and terminate the stream
        stream.close()
        p.terminate()

    def create_machine(self, name):
        t0 = {'source': 'initial', 'target': 'ready'}
        t1 = {'trigger': 'start', 'source': 'ready', 'target': 'playing'}
        t2 = {'trigger': 'done', 'source': 'playing', 'target': 'ready'}

        s_playing = {'name': 'playing', 'do': 'play()'}

        stm = Machine(name=name, transitions=[t0, t1, t2], states=[s_playing], obj=self)
        self.stm = stm
        return self.stm