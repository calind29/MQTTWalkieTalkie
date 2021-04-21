import stmpy
from GUI_component import GUI
from record_logic import Recorder
from playback_logic import Player

stm_driver = stmpy.Driver()
stm_driver.start(keep_active=True)

gui_wt = GUI()
recorder = Recorder()
playback = Player()

driver = stmpy.Driver()
driver.add_machine(gui_wt.create_machine('gui_wt_stm'))
driver.add_machine(recorder.create_machine('recorder_stm'))
driver.add_machine(playback.create_machine('playback_stm'))
driver.start()

gui_wt.create_gui()
