# -*- coding: utf-8 -*-
import visa
import openhtf.plugs as plugs
from openhtf.util import conf

__author__ = 'Jonas Steinkamp'
__email__ = 'jonas@steinka.mp'
__version__ = '0.1.0'

# TODO: Add Docstrings and Tests


conf.declare(
    'ident_code',
    description='identification code of the device. port or serial_number or device_name o vendor'
)

conf.declare(
    'timeout',
    default_value=60000,
    description='timeout for the device.'
)


class VisaDeviceException(Exception):
    """A basic Visa Device Exception"""


class MockConnection(object):
    def __init__(self):
        self.read_termination = None


class VisaPlug(plugs.BasePlug):
    @conf.inject_positional_args
    def __init__(self, ident_code, timeout):
        device = self.find_device(ident_code, timeout)[0]
        self.connection = MockConnection()

        self.vendor = device["vendor"]
        self.device_name = device["device_name"]
        self.serial_number = device["serial_number"]
        self.firmware_version = device["firmware_version"]
        self.called_function = ""

    def tearDown(self):
        self.called_function = "called teardown"

    def write(self, data):
        self.called_function = "called write: with -> {}".format(data)

    def query(self, data):
        self.called_function = "called query: with -> {}".format(data)
        if data == "RU1":
            return "U1:08.15V"

        if data == "RU2":
            return "U2:08.15V"

        if data == "MU1":
            return "U1:08.15V"

        if data == "MU2":
            return "U2:08.15V"

        if data == "RI1":
            return "I1: 8.15A"

        if data == "RI2":
            return "I2: 8.15A"

        if data == "MI1":
            return "I1: 8.15A"

        if data == "MI2":
            return "I2: 8.15A"

    def read(self):
        self.called_function = "called read"

    # ------------------------------------------------------------------------------------------------------------------
    # identification
    # ------------------------------------------------------------------------------------------------------------------
    def idn(self):
        return self.query('*IDN?')

    def get_identification(self):
        return self.idn()

    # ------------------------------------------------------------------------------------------------------------------
    # clear status command
    # ------------------------------------------------------------------------------------------------------------------
    def cls(self):
        self.write("*CLS")

    def clear_status_command(self):
        self.cls()

    # ------------------------------------------------------------------------------------------------------------------
    # reset command
    # ------------------------------------------------------------------------------------------------------------------
    def rst(self):
        self.write("*RST")

    def reset(self):
        self.rst()

    # ------------------------------------------------------------------------------------------------------------------
    # wait to continue
    # ------------------------------------------------------------------------------------------------------------------
    def wai(self):
        self.write("*WAI")

    def wait_to_continue(self):
        self.wai()

    # ------------------------------------------------------------------------------------------------------------------
    # event status register
    # ------------------------------------------------------------------------------------------------------------------
    def esr(self):
        return self.query("*ESR?")

    def get_event_status_register(self):
        return self.esr()

    # ------------------------------------------------------------------------------------------------------------------
    # self test
    # ------------------------------------------------------------------------------------------------------------------
    def tst(self):
        return self.query("*TST?")

    def self_test(self):
        return self.tst()

    # ------------------------------------------------------------------------------------------------------------------
    # status byte
    # ------------------------------------------------------------------------------------------------------------------
    def stb(self):
        return self.query("*STB?")

    def get_status_byte(self):
        return self.stb()

    # ------------------------------------------------------------------------------------------------------------------
    # event status
    # ------------------------------------------------------------------------------------------------------------------
    def ese(self, get=False):
        if get:
            return self.query("*ESE?")
        self.write("*ESE")

    def enable_event_status(self):
        self.ese()

    def is_event_status_enabled(self):
        return self.ese(True)

    # ------------------------------------------------------------------------------------------------------------------
    # operation complete command
    # ------------------------------------------------------------------------------------------------------------------
    def opc(self, get=False):
        if get:
            return self.query("*OPC?")
        self.write("*OPC")

    def set_operation_complete(self):
        self.opc()

    def get_operation_complete(self):
        return self.opc(True)

    # ------------------------------------------------------------------------------------------------------------------
    # service request command
    # ------------------------------------------------------------------------------------------------------------------
    def sre(self, get=False):
        if get:
            return self.query("*SRE?")
        self.write("*SRE")

    def get_service_request_enabled(self):
        return self.sre(True)

    def enable_service_request(self):
        self.sre()

    @staticmethod
    def find_device(ident_code="", timeout=None):
        return [{
                    'vendor': "HAMEG Instruments",
                    'device_name': "HM8143",
                    'serial_number': "",
                    'firmware_version': "2.45",
                    'port': ""
                }, ]
