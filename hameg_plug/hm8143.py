import visa_plug
from openhtf import conf

__author__ = 'Jonas Steinkamp'
__email__ = 'jonas@steinka.mp'
__version__ = '0.1.0'


class HM8143(visa_plug.VisaPlug):
    @conf.save_and_restore(ident_code='HM8143')
    @conf.save_and_restore(timeout=500)
    def __init__(self):
        super(self.__class__, self).__init__()
        self.connection.read_termination = '\r'
        self._mixed_mode = None
        self._remote_mode = None
        self._output = None

        # enable mixed mode and Output off
        self.mixed_mode = True
        self.output = False

    def tearDown(self):
        # disable remote mode and turn output off
        self.remote_mode = False
        self.output = False

        super(self.__class__, self).tearDown()

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, on_off):
        if on_off:
            self._output = True
            self.connection.write("OP1")
        else:
            self._output = False
            self.connection.write("OP0")

    @property
    def remote_mode(self):
        return self._remote_mode

    @remote_mode.setter
    def remote_mode(self, on_off):
        if on_off:
            self._remote_mode = True
            self._mixed_mode = False
            self.connection.write("RM1")
        else:
            self._remote_mode = False
            self.connection.write("RM0")

    @property
    def mixed_mode(self):
        return self._mixed_mode

    @mixed_mode.setter
    def mixed_mode(self, on_off):
        if on_off:
            self._mixed_mode = True
            self._remote_mode = False
            self.connection.write("MX1")
        else:
            self._mixed_mode = False
            self._remote_mode = True
            self.connection.write("MX0")

    @property
    def voltage_1(self):
        return float(self.connection.query("RU1").replace("U1:", "").replace("V", ""))

    @voltage_1.setter
    def voltage_1(self, value):
        self.connection.write("SU1:{:2.2f}".format(value))

    @property
    def voltage_2(self):
        return float(self.connection.query("RU2").replace("U2:", "").replace("V", ""))

    @voltage_2.setter
    def voltage_2(self, value):
        self.connection.write("SU2:{:2.2f}".format(value))

    @property
    def voltage_1_measured(self):
        return float(self.connection.query("MU1").replace("U1:", "").replace("V", ""))

    @property
    def voltage_2_measured(self):
        return float(self.connection.query("MU2").replace("U2:", "").replace("V", ""))

    @property
    def current_1(self):
        return float(self.connection.query("RI1").replace("I1:", "").replace("A", ""))

    @current_1.setter
    def current_1(self, value):
        self.connection.write("SI1:{:1.3f}".format(value))

    @property
    def current_2(self):
        return float(self.connection.query("RI2").replace("I2:", "").replace("A", ""))

    @current_2.setter
    def current_2(self, value):
        self.connection.write("SI2:{:1.3f}".format(value))

    @property
    def current_1_measured(self):
        return float(self.connection.query("MI1").replace("I1:", "").replace("A", ""))

    @property
    def current_2_measured(self):
        return float(self.connection.query("MI2").replace("I2:", "").replace("A", ""))
