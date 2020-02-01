import networktables
import _thread

import reflective_detective as rd
import display as display

class NTHandler:

    def __init__(self, NTInit):
        self._connected = False
        _thread.start_new_thread( NTInit, (self))

    def get_hsv_range(self):
        

    def get_filter_range(self):

    def NTInit(self):
        while not networktables.isconnected():
            networktables.initialize(server='10.17.26.2')

        self._preference = networktables.getTable('Preference')
        self._smart_dashboard = networktables.getTable('SmartDashboard')

        self._connected = True
        
        