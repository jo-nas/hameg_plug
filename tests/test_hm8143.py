import sys
import pytest
import mock_visa_plug
sys.modules['visa_plug'] = mock_visa_plug

import hameg_plug


def test_it_can_create_a_hm8143_plug():
    assert isinstance(hameg_plug.HM8143(), hameg_plug.HM8143)


@pytest.fixture
def hm8143():
    return hameg_plug.HM8143()


# Init Tests
#
def test_it_has_fill_out_all_device_information(hm8143):
    assert hm8143.firmware_version == "2.45"
    assert hm8143.device_name == "HM8143"
    assert hm8143.serial_number == ""
    assert hm8143.vendor == "HAMEG Instruments"


def test_it_has_activated_mixed_mode_on_init(hm8143):
    assert hm8143.mixed_mode is True


def test_it_has_cached_mixed_mode_and_remote_mode_on_init(hm8143):
    assert hm8143._mixed_mode is True
    assert hm8143._remote_mode is False


def test_it_has_disabled_the_output_on_init(hm8143):
    assert hm8143.output is False


# Teardown tests
#
def test_it_disabled_remote_mode_on_teardown(hm8143):
    hm8143.remote_mode = True
    hm8143.tearDown()
    assert hm8143.remote_mode is False


def test_it_disabled_the_output_on_teardown(hm8143):
    hm8143.output = True
    hm8143.tearDown()
    assert hm8143.output is False


def test_it_teardown_its_parent(hm8143):
    hm8143.tearDown()
    assert hm8143.called_function == "called teardown"


# Output tests
#
def test_it_can_activate_the_output(hm8143):
    hm8143.output = True
    assert hm8143.output is True
    assert hm8143.called_function == "called write: with -> OP1"


def test_it_can_deactivate_the_output(hm8143):
    hm8143.output = False
    assert hm8143.output is False
    assert hm8143.called_function == "called write: with -> OP0"


# Remote Mode tests
#
def test_it_can_activate_the_remote_mode(hm8143):
    hm8143.remote_mode = True
    assert hm8143.remote_mode is True
    assert hm8143.called_function == "called write: with -> RM1"


def test_it_deactivate_mixed_mode_on_activating_remote_mode(hm8143):
    hm8143.mixed_mode = True
    hm8143.remote_mode = True
    assert hm8143.mixed_mode is False


def test_it_can_deactivate_the_remote_mode(hm8143):
    hm8143.remote_mode = False
    assert hm8143.remote_mode is False
    assert hm8143.called_function == "called write: with -> RM0"


def test_it_activate_mixed_mode_on_deactivating_remote_mode(hm8143):
    hm8143.mixed_mode = False
    hm8143.remote_mode = False
    assert hm8143.mixed_mode is True


# Remote Mode tests
#
def test_it_can_activate_the_mixed_mode(hm8143):
    hm8143.mixed_mode = True
    assert hm8143.mixed_mode is True
    assert hm8143.called_function == "called write: with -> MX1"


def test_it_deactivate_remote_mode_on_activating_mixed_mode(hm8143):
    hm8143.remote_mode = True
    hm8143.mixed_mode = True
    assert hm8143.remote_mode is False


def test_it_can_deactivate_the_mixed_mode(hm8143):
    hm8143.mixed_mode = False
    assert hm8143.mixed_mode is False
    assert hm8143.called_function == "called write: with -> MX0"


def test_it_activate_remote_mode_on_deactivating_mixed_mode(hm8143):
    hm8143.remote_mode = False
    hm8143.mixed_mode = False
    assert hm8143.remote_mode is True


# Voltage
#
def test_it_sets_voltage_1(hm8143):
    hm8143.voltage_1 = 8.15
    assert hm8143.called_function == "called write: with -> SU1:8.15"


def test_it_reads_voltage_1(hm8143):
    assert hm8143.voltage_1 == 8.15
    assert hm8143.called_function == "called query: with -> RU1"


def test_it_sets_voltage_2(hm8143):
    hm8143.voltage_2 = 8.15
    assert hm8143.called_function == "called write: with -> SU2:8.15"


def test_it_reads_voltage_2(hm8143):
    assert hm8143.voltage_2 == 8.15
    assert hm8143.called_function == "called query: with -> RU2"


def test_it_measures_voltage_1(hm8143):
    assert hm8143.voltage_1_measured == 8.15
    assert hm8143.called_function == "called query: with -> MU1"


def test_it_measures_voltage_2(hm8143):
    assert hm8143.voltage_2_measured == 8.15
    assert hm8143.called_function == "called query: with -> MU2"


# Current
#
def test_it_sets_current_1(hm8143):
    hm8143.current_1 = 8.15
    assert hm8143.called_function == "called write: with -> SI1:8.150"


def test_it_reads_current_1(hm8143):
    assert hm8143.current_1 == 8.15
    assert hm8143.called_function == "called query: with -> RI1"


def test_it_sets_current_2(hm8143):
    hm8143.current_2 = 8.15
    assert hm8143.called_function == "called write: with -> SI2:8.150"


def test_it_reads_current_2(hm8143):
    assert hm8143.current_2 == 8.15
    assert hm8143.called_function == "called query: with -> RI2"


def test_it_measures_current_1(hm8143):
    assert hm8143.current_1_measured == 8.15
    assert hm8143.called_function == "called query: with -> MI1"


def test_it_measures_current_2(hm8143):
    assert hm8143.current_2_measured == 8.15
    assert hm8143.called_function == "called query: with -> MI2"


# test helper functions
#
def test_it_parse_current_string_to_float():
    number = hameg_plug.hm8143.parse_current("I1:08.15A")
    assert isinstance(number, float)
    assert number == 8.15

    number = hameg_plug.hm8143.parse_current("I2:08.15A")
    assert isinstance(number, float)
    assert number == 8.15


def test_it_parse_voltage_string_to_float():
    number = hameg_plug.hm8143.parse_voltage("U1:08.15V")
    assert isinstance(number, float)
    assert number == 8.15

    number = hameg_plug.hm8143.parse_voltage("U2:08.15V")
    assert isinstance(number, float)
    assert number == 8.15