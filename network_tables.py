from networktables import NetworkTables
import threading

import reflective_detective as rd
import display as display

class NTHandler:

    def __init__(self, nt_instance = None):
        if nt_instance is None:
            self._connected = False
            _thread = threading.Thread(target=self.NTInit)
            _thread.start()
            _thread.join()
        else:
            self._nt_instance = nt_instance
            self._connected = True

        self._preference = NetworkTables.getTable('Preference')
        self._smart_dashboard = NetworkTables.getTable('SmartDashboard')


    def addListener(self, key, default_value):
        if not self._preference.containsKey(key):
            self._preference.putNumber(key, default_value)
            self._preference.setPersistent(key)
        return lambda table=self._preference, key=key, default=default_value : table.getValue(key, default_value)


    def addValue(self, key, value):
        self._smart_dashboard.putNumber(key, value)

    def NTInit(self):
        while not NetworkTables.isConnected():
            NetworkTables.initialize(server='10.17.26.2')

        self._preference = NetworkTables.getTable('Preference')
        self._smart_dashboard = NetworkTables.getTable('SmartDashboard')

        self._connected = True
        print("There be networktables")
