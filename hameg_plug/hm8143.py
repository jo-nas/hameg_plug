import visa_plug
from openhtf import conf

__author__ = 'Jonas Steinkamp'
__email__ = 'jonas@steinka.mp'
__version__ = '0.1.0'


def parse_current(data_string):
    current_string = data_string.replace("I1:", "")\
        .replace("I2:", "")\
        .replace("A", "")
    return float(current_string)


def parse_voltage(data_string):
    voltage_string = data_string.replace("U1:", "")\
        .replace("U2:", "")\
        .replace("V", "")
    return float(voltage_string)


class HM8143(visa_plug.VisaPlug):
    @conf.save_and_restore(visa_ident_code='HM8143')
    @conf.save_and_restore(visa_timeout=500)
    def __init__(self):
        super(self.__class__, self).__init__()
        self.connection.read_termination = '\r'
        self._mixed_mode = None
        self._remote_mode = None
        self._output = None

        # enable mixed mode and turn Output off
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
            self.write("OP1")
        else:
            self._output = False
            self.write("OP0")

    @property
    def remote_mode(self):
        return self._remote_mode

    @remote_mode.setter
    def remote_mode(self, on_off):
        if on_off:
            self._remote_mode = True
            self._mixed_mode = False
            self.write("RM1")
        else:
            self._remote_mode = False
            self._mixed_mode = True
            self.write("RM0")

    @property
    def mixed_mode(self):
        return self._mixed_mode

    @mixed_mode.setter
    def mixed_mode(self, on_off):
        if on_off:
            self._mixed_mode = True
            self._remote_mode = False
            self.write("MX1")
        else:
            self._mixed_mode = False
            self._remote_mode = True
            self.write("MX0")

    @property
    def voltage_1(self):
        return parse_voltage(self.query("RU1"))

    @voltage_1.setter
    def voltage_1(self, value):
        self.write("SU1:{:2.2f}".format(value))

    @property
    def voltage_2(self):
        return parse_voltage(self.query("RU2"))

    @voltage_2.setter
    def voltage_2(self, value):
        self.write("SU2:{:2.2f}".format(value))

    @property
    def voltage_1_measured(self):
        return parse_voltage(self.query("MU1"))

    @property
    def voltage_2_measured(self):
        return parse_voltage(self.query("MU2"))

    @property
    def current_1(self):
        return parse_current(self.query("RI1"))

    @current_1.setter
    def current_1(self, value):
        self.write("SI1:{:1.3f}".format(value))

    @property
    def current_2(self):
        return parse_current(self.query("RI2"))

    @current_2.setter
    def current_2(self, value):
        self.write("SI2:{:1.3f}".format(value))

    @property
    def current_1_measured(self):
        return parse_current(self.query("MI1"))

    @property
    def current_2_measured(self):
        return parse_current(self.query("MI2"))
