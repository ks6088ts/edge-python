import time

import numpy as np
import spidev


class Imu0:

    # MASK
    SPI_READ_MASK = 0x80
    DUMMY_BYTE = 0xFF

    # WHO_AM_I
    WHO_AM_I = 0x0F
    WHO_AM_I_VALUE = 0x6E

    # IMU registers (0x22-0x2D, 12 bytes)
    IMU_REGISTER = 0x22
    IMU_REGISTER_BYTES = 12
    IMU_NUM_INPUTS = 6

    # CTRL3_C SW reset
    CTRL3_C_SW_RESET = 0x01

    REGISTER_DICT_REG_IDX = 0
    REGISTER_DICT_VALUE_IDX = 1
    REGISTER_DICT = {
        # reg_name: reg, value
        "CTRL1_XL": [0x10, 0x84],
        "CTRL2_G": [0x11, 0x8C],
        "CTRL3_C": [0x12, 0x44],
        "CTRL4_C": [0x13, 0x02],
        "CTRL5_C": [0x14, 0x00],
        "CTRL6_C": [0x15, 0x05],
        "CTRL7_G": [0x16, 0x00],
        "CTRL8_XL": [0x17, 0x40],
        "CTRL9_XL": [0x18, 0xE0],
        "CTRL10_C": [0x19, 0x00],
    }

    def __init__(self, bus=0, device=0, max_speed_hz=1000000):
        self.bus = bus
        self.device = device
        self.max_speed_hz = max_speed_hz
        self.spi = spidev.SpiDev()

    def initialize(self):
        self.spi.open(self.bus, self.device)
        self.spi.max_speed_hz = self.max_speed_hz
        self._setup()
        self._dump_registers()

    def finalize(self):
        pass

    def get_states(self):
        resp = self._read_registers(self.IMU_REGISTER, self.IMU_REGISTER_BYTES)

        values = [0] * self.IMU_NUM_INPUTS
        for i, _ in enumerate(values):
            idx = i * 2
            values[i] = np.int16((resp[idx + 1] << 8) | resp[idx])
        return time.time(), [
            values[3],
            values[4],
            values[5],
            values[0],
            values[1],
            values[2],
        ]

    def _reset(self):
        return self.spi.xfer2(
            [
                self.REGISTER_DICT["CTRL3_C"][self.REGISTER_DICT_REG_IDX],
                self.CTRL3_C_SW_RESET,
            ]
        )

    def _get_who_am_i(self):
        return self._read_registers(self.WHO_AM_I, 1)

    def _get_current_register_dict(self):
        register_dict = {}
        for reg_name in self.REGISTER_DICT:
            current_value = self._read_registers(
                self.REGISTER_DICT[reg_name][self.REGISTER_DICT_REG_IDX], 1
            )
            register_dict[reg_name] = current_value
        return register_dict

    def _write_reg(self, reg, val):
        return self.spi.xfer2([reg, val])

    def _read_registers(self, reg, byte_count):
        data = [self.DUMMY_BYTE] * (byte_count + 1)
        data[0] = reg | self.SPI_READ_MASK
        assert 1 + byte_count == len(data)
        resp = self.spi.xfer2(data)
        assert 1 + byte_count == len(resp)
        if len(resp) == 2:
            return resp[1]
        return resp[1:]

    def _setup(self):

        self._reset()

        actual = self._get_who_am_i()
        assert (
            self.WHO_AM_I_VALUE == actual
        ), f"who_am_i check failed, \
            (expected, actual) = ({hex(self.WHO_AM_I_VALUE)}, {hex(actual)})"

        # Writing initial values into registers
        for value in self.REGISTER_DICT.values():
            self._write_reg(
                value[self.REGISTER_DICT_REG_IDX], value[self.REGISTER_DICT_VALUE_IDX]
            )

        # Verify current register values
        current_register_dict = self._get_current_register_dict()
        for key in self.REGISTER_DICT:
            assert (
                self.REGISTER_DICT[key][self.REGISTER_DICT_VALUE_IDX]
                == current_register_dict[key]
            )

    def _dump_registers(self):
        current_register_dict = self._get_current_register_dict()
        print("# device = imu0")
        print("# reg_name, reg_value, current")
        for reg_name in self.REGISTER_DICT:
            print(
                f"# {reg_name}, \
                {hex(self.REGISTER_DICT[reg_name][self.REGISTER_DICT_VALUE_IDX])}, \
                {hex(current_register_dict[reg_name])}"
            )
