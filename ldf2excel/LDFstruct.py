import decimal
import fnmatch
import itertools
import logging
import math
import struct
import typing
import warnings
from builtins import *

import attr


@attr.s(eq=False)
class LIN_attr(object):
    """
    Represents LIN attributes

    Signal has following attributes:

    * LIN protocol version
    * LIN language version
    * LIN speed
    * LIN channel name
    """
    LIN_protocol_ver = attr.ib(default=str)
    LIN_language_ver = attr.ib(default=str)
    LIN_speed = attr.ib(default=int)
    LIN_channel = attr.ib(default=str)

    def speed(self, LIN_speed):
        print("def : LDFstruct - LIN_attr - speed")
        self.LIN_speed = float(LIN_speed / 1000)
        return self.LIN_speed


@attr.s(eq=False)
class node_attr(object):
    """
    Represents  node attributes

    node has the following attributes:

    * node name
    * role
    * time base
    * jitter
    * configured NAD
    * init value
    * protocol version
    * supplied ID
    * function ID
    * variant ID
    * P2 min
    * ST min
    * N_As_timeout
    * N_Cr_timeout
    * response error
    * fault state signal
    """
    name = attr.ib(default=str)
    role = attr.ib(default=str)
    time_base = attr.ib(default=int)
    jitter = attr.ib(default=int)
    configured_NAD = attr.ib(default=int)
    init_NAD = attr.ib(default=int)
    protocol_ver = attr.ib(default=str)
    suppliedID = attr.ib(default=int)
    functionID = attr.ib(default=int)
    variantID = attr.ib(default=int)
    P2min = attr.ib(default=int)
    STmin = attr.ib(default=int)
    N_As = attr.ib(default=float)
    N_Cr = attr.ib(default=float)
    response_error = attr.ib(default=str)
    fault_state_signals = attr.ib(default=str)
    configurable_frames = attr.ib(default=dict)

    def role(self, role):
        print("def : LDFstruct - node_attr - role")
        if role =='Master':
            self.role = "master"
            return self.role
        else:
            self.role = "slave"
            return self.role

    def time_base(self, time_base):
        print("def : LDFstruct - node_attr - time_base")
        self.time_base = time_base * 1000
        return self.time_base

    def jitter(self, jitter):
        print("def : LDFstruct - node_attr - jitter")
        self.jitter = jitter * 1000
        return self.jitter

    def set_P2min(self, P2min):
        print("def : LDFstruct - node_attr - set_P2min")
        self.P2min = P2min * 1000
        return self.P2min

    def set_STmin(self, STmin):
        print("def : LDFstruct - node_attr - set_STmin")
        self.STmin = STmin * 1000
        return self.STmin

    def set_N_As(self, N_As):
        print("def : LDFstruct - node_attr - set_N_As")
        self.N_As = N_As * 1000
        return self.N_As

    def set_N_Cr(self, N_Cr):
        print("def : LDFstruct - node_attr - set_N_Cr")
        self.N_Cr = N_Cr * 1000
        return self.N_Cr

    def set_configurable_frames(self, configurable_frames):
        print("def : LDFstruct - node_attr - set_configurable_frames")
        cfarray = str()
        if type(configurable_frames) is dict:
            for key, val in configurable_frames.items():
                cfarray += key + ', ' + str(val) + ', '
            self.configurable_frames = cfarray[0:-2]
            return self.configurable_frames

        else:
            for cf in configurable_frames:
                cfarray += cf + ', '
            self.configurable_frames = cfarray[0:-2]
            return self.configurable_frames


@attr.s(eq=False)
class FS_attr(object):
    """
    Represents frame and signal attributes

    frame and signal have following attributes:

    * frame name
    * frame ID
    * frame size
    * signal name
    * startbit
    * width(length)
    * init value
    * publisher
    * subscriber
    * signal representation
    """
    frame_name = attr.ib(default=str)
    frameID = attr.ib(default=int)
    size = attr.ib(default=int)
    signal_name = attr.ib(default=str)
    startbit = attr.ib(default=int)
    width = attr.ib(default=int)
    init_value = attr.ib(default=int)
    publisher = attr.ib(default=str)
    subscriber = attr.ib(default=str)
    signal_representation = attr.ib(default=dict)

    def set_init_value(self, init_value):
        print("def : LDFstruct - FS_attr - set_init_value")
        if type(init_value) == list:
            initval = str()
            for val in init_value:
                initval += str(val) + ', '
            self.init_value = initval[0:-2]
        else:
            self.init_value = init_value


@attr.s(eq=False)
class OF_attr(object):
    """
    Represents other frames attributes

    other frames has following attributes:

    * frame type
    * event/sporadic name
    * table (etf)
    * frame id (etf)
    * frames
    """
    type = attr.ib(default=dict)
    name = attr.ib(default=str)
    table = attr.ib(default=str)
    frameID = attr.ib(default=int)
    frames = attr.ib(default=list)
    signal_representation = attr.ib(default=dict)


@attr.s(eq=False)
class table_attr(object):  # event triggered frame
    """
    Represents table attributes

    table has following attributes:

    * table name
    * slot
    * type
    * delay
    """
    name = attr.ib(default=str)
    slot = attr.ib(default=str)
    type = attr.ib(default=int)
    delay = attr.ib(default=int)
    node = attr.ib(default=str)
    frame = attr.ib(default=str)
    frame_index = attr.ib(default=str)

    def set_delay(self, delay):
        print("def : LDFstruct - table_attr - set_delay")
        self.delay = delay * 1000