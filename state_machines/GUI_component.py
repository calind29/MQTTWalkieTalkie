import stmpy
from appJar import gui
import time
import fileinput

class GUI:

    def print_to_receiving(self):
        print("transition: idle to receiving, trigger: msg_received")

    def print_to_sending(self): 
        print("transition: idle to sending, trigger: start in recorder_stm")

    def recording(self):
        self.print_to_sending()
        self.stm.driver.send('start', 'recorder_stm')

    def stop_recording(self):
        self.stm.driver.send('stop', 'recorder_stm')

    def play_msg_signal(self):
        self.stm.driver.send('start', 'playback_stm')

    def change_channel(self):

        newChannel = open("audio_files/channel.txt", "w")
        newChannel.write(self.app.getEntry("Channel"))

        self.stm.send('change_channel')
        self.stm.driver.send('change_channel_signal', 'playback_stm')
    
    def A(self):
        print("internal transition")

    def receive_emg_msg(self):
        print("'A emg msg was received!'")
        self.stm.driver.send('emg_msg', 'recorder_stm')
        self.app.setImage("show", "/img/rsos.png")
        self.app.setImageMap("show", self.click, self.coords)
        # self.stm.driver.send('emg_msg', 'playback_stm')

    def finish_emg_msg(self):
        print("'The emg msg is done playing!'")
        self.stm.driver.send('emg_msg', 'recorder_stm')
        self.app.setImage('show', "img/idle2.png")
        self.app.setImageMap("show", self.click, self.coords)
        # self.stm.driver.send('emg_msg', 'playback_stm')
    
    def print_back_to_idle(self):
        print("back to idle state")

    def print_to_receiving_emg_msg(self):
        print("going to receiving_emg_msg state")
        
    def print_to_sending_emg_msg(self):
        print("going to sending_emg_msg state")
    
    def print_start_machine(self):
        print("start machine")

    def print_do(self):
        print("this is a do")

    def print_timer(self):
        print("timer expired, going to idle state")

    def __init__(self):
        self.app = gui()
        self.a = ""
        self.channelEdit = False
        self.coords = {
            "Record": [76, 404, 188, 483],
            "SOS": [79, 496, 178, 533],
            "channel": [54, 155, 104, 191],
            "volume": [126, 170, 226, 292],
            "1": [83,565,138,594],
            "2": [158, 565, 224, 594],
            "3": [241, 565, 301, 594],
            "4": [83, 609, 138, 637],
            "5": [158, 609, 224, 637],
            "6": [241, 609, 301, 637],
            "7": [83, 652, 138, 684],
            "8": [158, 652, 224, 684],
            "9": [241, 652, 301, 684],
            "0": [158, 702, 224, 726],
            "+": [83, 702, 138, 726],
            "done": [241, 702, 301, 726]
        }
        self.app.addImage("show", "img/idle.png", 0, 0)
        self.app.setImageMap("show", self.click, self.coords)

        self.app.addLabel("l1", "<click on the device>")
        self.app.addLabel("channel", "" + str(50) + "")

    def click(self,area):
        self.app.setLabel("l1", area)
        if area == "SOS":
            self.stm.driver.send('emg_msg', 'recorder_stm')
            self.app.setImage("show", "img/ssos.png")
            self.app.setImageMap("show", self.click, self.coords)
            print("sending emergency message")
        if area == "Record":
            self.recording()
            #self.stm.driver.send('start', 'recorder_stm')
            self.app.setImage("show", "img/recording.png")
            self.app.setImageMap("show", self.click, self.coords)
            print("sending message")
        if area == "channel":
            # self.app.setImage("show", "/Users/cecilie/Desktop/ntnu/Frame 2.png")
            self.app.setImageMap("show", self.click, self.coords)
            print("channel changed")
        if area == None:
            self.app.setImage('show', "img/idle2.png")
            self.app.setImageMap("show", self.click, self.coords)
        """for k in ["0","1","2","3","4","5","6","7","8","9"]:
            if area == k:
                self.a = area
                self.app.setLabel("channelnow", "Channel: " + self.a)
                self.change_channel()
                break"""
        if area == "+":
            self.channelEdit = True
        k = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        if self.channelEdit:
            if area in k:
                self.a += area
            if area == "done":
                self.channelEdit = False
                self.app.setLabel("channelnow", "Current channel: " + self.a)
                self.change_channel()
                self.a = ""



    def create_gui(self):

        self.app.setFont(14)


        #self.app.startLabelFrame('Starting walkie talkie/ Home screen:')
        #self.app.addButton('Record message', self.recording)
        #self.app.addButton('Emergency', None)
        self.app.addButton('Play message', self.play_msg_signal)
        self.app.addLabelEntry("Channel", None)
        self.app.addButton('Change channel', self.change_channel)
        # self.app.stopLabelFrame()

        self.app.startLabelFrame('Releasing buttons:', 0,1)
        self.app.addButton('Release record', self.stop_recording)
        self.app.addButton('Release emergency', None)
        self.app.addButton('Emergency msg received', self.receive_emg_msg)
        self.app.addButton('Emergency msg finished', self.finish_emg_msg)
        self.app.stopLabelFrame()

        self.app.startLabelFrame('Display:',0,2)
        self.app.addLabel("channelnow", "Current channel: " + "1")
        #self.app.addLabel('Current Status: Listening', None)
        #self.app.addLabel('Current Volume: 15', None)
        self.app.stopLabelFrame()

        self.app.go()

    def create_machine(self, name): 
        # start
        t0 = {'source': 'initial',
            'target': 'idle',
            'effect': 'print_start_machine'}

        # idle to receiving by receiving message
        t1 = {
            'source': 'idle',
            'target': 'receiving',
            'trigger': 'msg_received',
            'effect': 'print_to_receiving'}

        # idle to sending by button
        t2 = {
            'source': 'idle',
            'trigger': 'record_button',
            'target': 'sending',
            'effect': 'print_to_sending; recording'}

        # idle to sending_emg_msg by button
        t3 = {
            'source': 'idle',
            # remember that this trigger represents a function which handles
            # the two buttons pressed simultanously
            'trigger': 'emg_mes_button',
            'target': 'sending_emg_msg',
            'effect': 'print_to_sending_emg_msg'}

        # idle to receiving_emg_msg by trigger by trigger emg_msg_received
        t4 = {
            'source': 'idle',
            'trigger': 'emg_mes_received',
            'target': 'receiving_emg_msg',
            'effect': 'print_to_receiving_emg_msg'}

        # receiving_emg_msg to idle by trigger done
        t5 = {
            'source': 'receiving_emg_msg',
            'trigger': 'done',
            'target': 'idle',
            'effect': 'print_back_to_idle'}

        # receiving to receiving_emg_msg by trigger emg_msg_received
        t6 = {
            'source': 'receiving',
            'trigger': 'emg_msg_received',
            'target': 'receiving_emg_msg',
            'effect': 'print_to_receiving_emg_msg'}

        # sending to receiving_emg_msg by trigger emg_msg_received
        t7 = {
            'source': 'sending',
            'trigger': 'emg_msg_received',
            'target': 'receiving_emg_msg',
            'effect': 'print_to_receiving_emg_msg'}

        # sending to idle by trigger done
        t8 = {
            'source': 'sending',
            'trigger': 'done',
            'target': 'idle',
            'effect': 'print_back_to_idle'}

        # receiving to idle by trigger done
        t9 = {
            'source': 'receiving',
            'trigger': 'done',
            'target': 'idle',
            'effect': 'print_back_to_idle'}

        # receiving to sending_emg_msg by trigger emg_mes_button
        t10 = {
            'source': 'receiving',
            'trigger': 'emg_mes_button',
            'target': 'sending_emg_msg',
            'effect': 'print_to_sending_emg_msg'}

        # sending_emg_msg to idle by trigger done
        t11 = {
            'source': 'sending_emg_msg',
            'trigger': 'done',
            'target': 'idle',
            'effect': 'print_back_to_idle'}

        # sending to idle by trigger timer
        t12 = {
            'source': 'sending',
            'trigger': 't',
            'target': 'idle',
            'effect': 'print_timer'}

        # sending_emg_msg to idle by trigger done or timer
        t13 = {
            'source': 'sending_emg_msg',
            'trigger': 't',
            'target': 'idle',
            'effect': 'print_timer'}

        # internal transition in idle
        t13 = {
            'source': 'idle',
            'trigger': 'change_channel',
            'target': 'idle',
            'effect': 'A'}

        idle = {'name': 'idle'
                }

        sending = {'name': 'sending',
                    'entry': 'start_timer("t", 3000)',
                    # do: publish()
                    # 'do': 'print_do',
                    'do': 'recording'}

        receiving = {'name': 'receiving',
                    # do: play()
                    'do': 'print_do'}

        receiving_emg_msg = {'name': 'receiving_emg_msg',
                            # do: play() - possible other function
                            'do': 'print_do'}

        sending_emg_msg = {'name': 'sending_emg_msg',
                            'entry': 'start_timer("t", 30000)',
                            #'do': 'publish()'
                            'do': 'print_do'}

        stm = stmpy.Machine(name=name, 
                transitions=[t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13], 
                states=[idle, sending, receiving, receiving_emg_msg, sending_emg_msg],
                obj=self) 
        self.stm = stm
        return self.stm