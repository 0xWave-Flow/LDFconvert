import os
import json
import sys
import ldfparser
import LDFstruct
import attr


def loadd(type, ldf):

    # load LIN attributes
    if type == 'LIN':
        LINarray = []
        LIN = LDFstruct.LIN_attr

        #print("def : load - loadd - ORGANIZE : {}".format(ldf['header']))
        LIN.LIN_protocol_ver = str(ldf['protocol_version'])
        LINarray.append(LIN.LIN_protocol_ver)

        LIN.LIN_language_ver = str(ldf['language_version'])
        LINarray.append(LIN.LIN_language_ver)

        LIN.speed(LIN, int(ldf['speed']))
        LINarray.append(LIN.LIN_speed)

        try:
            LIN.LIN_channel = ldf['channel_name']
            LINarray.append(LIN.LIN_channel)

        except:
            LINarray.append('/')

        print("def : load - loadd - ORGANIZE - LIN : {}".format(LINarray))
        return LINarray

    # load mater node attributes
    elif type == 'node master':

        #print("def : load - loadd - ORGANIZE - NODE MASTER : {}".format(ldf["nodes"]))
        #print("def : load - loadd - ORGANIZE - NODE MASTER : {}".format(ldf["nodes"]["slaves"]))

        nodearray = []
        ldf = ldf["nodes"]["master"]
        masternode = LDFstruct.node_attr

        masternode.name = ldf['name']
        nodearray.append(masternode.name)

        nodearray.append('master')

        masternode.time_base(masternode, ldf['timebase'])
        nodearray.append(masternode.time_base)

        masternode.jitter(masternode, ldf['jitter'])
        nodearray.append(masternode.jitter)

        for i in range(13):
            nodearray.append("/")

        print("def : load - loadd - ORGANIZE - NODE MASTER : {}".format(nodearray))
        return nodearray

    # load slave nodes attributes
    elif type == 'node slaves':
        slavearray = []
        slavenode = LDFstruct.node_attr

        slavenode.name = ldf["name"]
        slavearray.append(slavenode.name)

        slavearray.append("slave")
        slavearray.append("/")
        slavearray.append("/")

        slavenode.configured_NAD = ldf["configured_nad"]
        slavearray.append(slavenode.configured_NAD)

        if 'initial_nad' in ldf.keys():
            slavenode.init_NAD = ldf["initial_nad"]
            slavearray.append(slavenode.init_NAD)
        else:
            slavearray.append("/")

        slavenode.protocol_ver = str(ldf["lin_protocol"])
        slavearray.append(slavenode.protocol_ver)

        slavenode.suppliedID = ldf["product_id"]["supplier_id"]
        slavearray.append(slavenode.suppliedID)

        slavenode.functionID = ldf["product_id"]["function_id"]
        slavearray.append(slavenode.functionID)

        slavenode.variantID = ldf["product_id"]["variant"]
        slavearray.append(slavenode.variantID)

        if "P2_min" in ldf:
            slavenode.set_P2min(slavenode, ldf["P2_min"])
            slavearray.append(slavenode.P2min)
        else:
            slavearray.append(0)

        if "ST_min" in ldf:
            slavenode.set_STmin(slavenode, ldf["ST_min"])
            slavearray.append(slavenode.STmin)
        else:
            slavearray.append(0)

        try:
            slavenode.set_N_As(slavenode, ldf["N_As_timeout"])
            slavearray.append(slavenode.N_As)
        except:
            slavearray.append('/')


        try:
            slavenode.set_N_Cr(slavenode, ldf["N_Cr_timeout"])
            slavearray.append(slavenode.N_Cr)
        except:
            slavearray.append('/')

        slavenode.response_error = ldf["response_error"]
        slavearray.append(slavenode.response_error)

        if "fault_state_signals" in ldf.keys():
            slavenode.fault_state_signals = ldf['fault_state_signals']
            fss = str()
            for fs in slavenode.fault_state_signals:
                fss += fs + ', '

            slavearray.append(fss[0:-2])
        else:
            slavearray.append("/")

        slavenode.set_configurable_frames(slavenode, ldf['configurable_frames'])
        slavearray.append(slavenode.configurable_frames)

        print("def : load - loadd - ORGANIZE - SLAVE : {}".format(slavearray))
        return slavearray

    elif type == 'event_triggered_frames':
        etfarray = []
        etf = LDFstruct.OF_attr

        etf.type = type
        etfarray.append(etf.type)

        etf.name = ldf["name"]
        etfarray.append(etf.name)

        etf.table = ldf["collision_resolving_schedule_table"]
        etfarray.append(etf.table)

        etf.frameID = ldf["frame_id"]
        etfarray.append(etf.frameID)

        frames = str()
        etf.frames = ldf["frames"]
        for frame in ldf["frames"]:
            frames += frame + ", "
        etfarray.append(frames[0:-2])

        print("def : load - loadd - ORGANIZE - EVENT TRIGGER FRAME : {}".format(etfarray))
        return etfarray

    elif type == 'sporadic_frames':
        sfarray = []
        sf = LDFstruct.OF_attr

        sf.type = type
        sfarray.append(sf.type)

        sf.name = ldf['name']
        sfarray.append(sf.name)

        sfarray.append('/')
        sfarray.append('/')
        fr = str()
        for frame in ldf['frames']:
            fr += frame + ', '
        sfarray.append(fr[0:-2])

        print("def : load - loadd - ORGANIZE - SPORADIC FRAME : {}".format(sfarray))
        return sfarray
    else:
        print("error types")


def loadfs(type, ldff, ldf, signal):

    #print("def : load - loadfs - {} - {}".format(ldff,signal))

    if type == 'frame and signal':
        fsarray = []
        fs = LDFstruct.FS_attr
        fs.frame_name = ldff["name"]
        fsarray.append(fs.frame_name)

        fs.frameID = ldff["frame_id"]
        fsarray.append(fs.frameID)

        fs.size = ldff["length"]
        fsarray.append(fs.size)

        ldfs = ldf["signals"]
        for index in range(len(ldfs)):
            if signal["signal"] == ldfs[index]["name"]:
                fs.signal_name = ldfs[index]["name"]
                fsarray.append(fs.signal_name)

                fs.startbit = signal["offset"]
                fsarray.append(fs.startbit)

                fs.width = ldfs[index]["width"]
                fsarray.append(fs.width)

                fs.set_init_value(fs, ldfs[index]["init_value"])
                fsarray.append(fs.init_value)

                fs.publisher = ldff["publisher"]
                fsarray.append(fs.publisher)

                sub = str()
                fs.subscriber = ldfs[index]["subscribers"]
                for subs in ldfs[index]["subscribers"]:
                    sub += subs + ", "
                fsarray.append(sub[0:-2])


                if "signal_representations" in ldf:
                    for rep in ldf["signal_representations"]:
                        print("def : load - loadfs - SIGNAL REPRESENTATION : {}".format(rep))
                        if signal["signal"] in rep["signals"]:
                            for encode in ldf["signal_encoding_types"]:
                                if rep["encoding"] == encode["name"]:
                                    fs.signal_representation = str(encode)
                                    en = str()
                                    en += encode["name"] + ',\n'
                                    for value in encode["values"]:
                                        for val in value.values():
                                            en += str(val) + ', '
                                        en += '\n'
                                    fsarray.append(en[0:-3])
                                    return fsarray
                else:
                    fsarray.append('/')
                    return fsarray
        fsarray.append('/')

        return fsarray


def loadst(type, ldfst, ldfslot):

    #print("def : load - loadst")

    if type == "schedule_tables":
        starray = []
        st = LDFstruct.table_attr
        st.name = ldfst["name"]

        #print("def : load - loadst - {}".format(ldfslot["delay"]))

        starray.append(st.name)
        if ldfslot["command"]["type"].startswith('assign') or ldfslot["command"]["type"].startswith('master'):
            st.slot = "MasterReq"
            starray.append(st.slot)
        elif ldfslot["command"]["type"].startswith('slave'):
            st.slot = "SlaveResp"
            starray.append(st.slot)
        else:
            st.slot = ldfslot["command"]["frame"]
            starray.append(st.slot)

        st.type = ldfslot["command"]["type"]
        starray.append(st.type)

        st.set_delay(st, ldfslot["delay"])
        starray.append(st.delay)

        if ldfslot["command"]["type"].startswith('assign'):
            st.node = ldfslot["command"]["node"]
            starray.append(st.node)
        else:
            starray.append('/')

        if ldfslot["command"]["type"] == 'assign_frame_id':
            st.frame = ldfslot["command"]["frame"]
            starray.append(st.frame)
        else:
            starray.append('/')

        if ldfslot["command"]["type"] == 'assign_frame_id_range':
            st.frame_index = ldfslot["command"]["frame_index"]
            starray.append(st.frame_index)
        else:
            starray.append('/')

        print("def : load - loadst - SEND : {}".format(starray))

        return starray
