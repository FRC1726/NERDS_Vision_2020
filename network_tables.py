from networktables import NetworkTables
import threading

import reflective_detective as rd
import display as display

class NTHandler:

    def __init__(self):
        self._connected = False
        _thread = threading.Thread(target=self.NTInit)
        _thread.start()
        _thread.join()

        self._preference = NetworkTables.getTable('Preference')
        self._smart_dashboard = NetworkTables.getTable('SmartDashboard')


    def addListener(self, key):
        if not self._preference.containsKey(key):
            self._preference.putNumber(key, 0)
            self._preference.setPersistent(key)
        return lambda table=self._preference, key=key : table.getValue(key, 0)


    def addValue(self, key, value):
        self._smart_dashboard.putNumber(key, value)

    def NTInit(self):
        while not NetworkTables.isConnected():
            NetworkTables.initialize(server='10.17.26.2')

        self._preference = NetworkTables.getTable('Preference')
        self._smart_dashboard = NetworkTables.getTable('SmartDashboard')

        self._connected = True
        print("There be networktables")
