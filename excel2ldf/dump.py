import os
import json
import sys
import ldfparser
import attr
import xlsxwriter
import xlrd


def dumpp(infile, outfile):

    print("def : dump - dumpp")

    # load excel
    wb = xlrd.open_workbook(infile)
    f = open(outfile, "w")

    # header (optional)
    f.write('/**********************************************************/\n')
    f.write('/* This is the example convert Excel format to LDF format */\n')
    f.write('/**********************************************************/\n')
    f.write('\n')

    # LIN global definition (Required)
    f.write('LIN_description_file;\n')
    sheet = 'LIN Attributes'
    table = wb.sheet_by_name(sheet)

    lin_attr = ['LIN_protocol_version',
                'LIN_language_version',
                'LIN_speed',
                'Channel_name']

    for idx in range(len(lin_attr)):
        if lin_attr[idx] != 'LIN_speed' and str(table.row_values(1)[idx]) != '/':
            tmp = lin_attr[idx] + ' = "' + str(table.row_values(1)[idx]) + '";\n'
            print(tmp)
            f.write(lin_attr[idx] + ' = "' + str(table.row_values(1)[idx]) + '";\n')
        elif lin_attr[idx] == 'LIN_speed':
            tmp = lin_attr[idx] + ' = ' + str(table.row_values(1)[idx]) + ' kbps;\n'
            print(tmp)
            f.write(lin_attr[idx] + ' = ' + str(table.row_values(1)[idx]) + ' kbps;\n')
    f.write('\n')

    # Node Attribute (Required)
    sheet = 'Node Attributes'
    table = wb.sheet_by_name(sheet)
    f.write('Nodes {\n\t')
    slavelist = []

    # read and write master and slaves
    for row in range(1, table.nrows):
        node_data = table.row_values(row)

        if node_data[1] == 'master':
            print("def : dump - dumpp - MASTER : {}".format(node_data))
            f.write(
                "Master: " + str(node_data[0]) + ', ' + str(int(node_data[2])) + " ms, " + str(node_data[3]) + "ms;")
        else:
            slavelist.append(node_data[0])

    f.write("\n\tSlaves: ")
    for slave in slavelist:
        print("def : dump - dumpp - SLAVE : {}".format(slave))
        if slave != slavelist[-1]:
            f.write(slave + ", ")
        else:
            f.write(slave + ";\n}\n")
    f.write('\n')
    # Node composition (optional)

    # Signals (Required)
    sheet = 'Frame and Signal Attributes'
    table = wb.sheet_by_name(sheet)
    f.write('Signals {\n')

    # read and write signals
    for row in range(1, table.nrows):
        signal_data = table.row_values(row)
        print("def : dump - dumpp - SIGNAL : {}".format(signal_data))
        if type(signal_data[6]) == str:
            f.write('\t' + str(signal_data[3]) + ": " + str(int(signal_data[5])) + ', {' + signal_data[6] +
                    '}, ' + str(signal_data[7]) + ', ' + str(signal_data[8]) + ';\n')
        else:
            f.write('\t' + str(signal_data[3]) + ": " + str(int(signal_data[5])) + ', ' + str(int(signal_data[6])) +
                    ', ' + str(signal_data[7]) + ', ' + str(signal_data[8]) + ';\n')

    f.write('}\n\n')
    # diagnostic signal (optional)

    # Frames (Required)
    sheet = 'Frame and Signal Attributes'
    table = wb.sheet_by_name(sheet)
    f.write('Frames {\n')

    # read and write frames
    framelist = []
    for row in range(1, table.nrows):
        frame_data = table.row_values(row)
        print("def : dump - dumpp - FRAME : {}".format(frame_data))
        # first frame in excel
        if frame_data[0] not in framelist and row == 1:
            f.write('\t' + str(frame_data[0]) + ": " + str(int(frame_data[1])) + ', ' + str(
                frame_data[7]) + ', ' +
                    str(int(frame_data[2])) + ' {\n\t\t' + str(frame_data[3]) + ', ' + str(int(frame_data[4])) + ';\n')

        # detect new frame and signal
        elif frame_data[0] not in framelist:
            f.write('\t}\n\t' + str(frame_data[0]) + ": " + str(int(frame_data[1])) + ', ' + str(
                frame_data[7]) + ', ' +
                    str(int(frame_data[2])) + ' {\n\t\t' + str(frame_data[3]) + ', ' + str(int(frame_data[4])) + ';\n')

        # frames with multiple signals
        else:
            f.write('\t\t' + str(frame_data[3]) + ', ' + str(int(frame_data[4])) + ';\n')
        framelist.append(frame_data[0])
    f.write('\t}\n}\n\n')


    sheet = 'Diagnostic_Frames'
    table = wb.sheet_by_name(sheet)

    Diag = []
    for row in range(1, table.nrows):
        diag_data = table.row_values(row)

        FrameExist = False
        for each in Diag:
            if each['FrameName'] == diag_data[0]:
                FrameExist = True
                break

        if FrameExist == True:

            SignalTemp = {}
            SignalTemp['SignalName'] = diag_data[2]
            SignalTemp['StartBit'] = diag_data[3]
            SignalTemp['Length'] = diag_data[4]
            SignalTemp['InitValue'] = diag_data[5]

            for each in Diag:
                if each["FrameName"] == diag_data[0]:
                    each["Signals"].append(SignalTemp)
                    break

        else:
            # print("DIAG : {}".format(diag_data))
            # Diag["FrameName"] = diag_data[0]
            # Diag["FrameID"] = diag_data[1]
            SignalTemp = {}
            DiagTemp = {}
            SignalTemp['SignalName'] = diag_data[2]
            SignalTemp['StartBit'] = diag_data[3]
            SignalTemp['Length'] = diag_data[4]
            SignalTemp['InitValue'] = diag_data[5]
            DiagTemp["FrameName"] = diag_data[0]
            DiagTemp["FrameID"] = diag_data[1]
            DiagTemp["Signals"] = []
            DiagTemp["Signals"].append(SignalTemp)
            Diag.append(DiagTemp)

    f.write('Diagnostic_signals {\n')
    for each_frm in Diag:
        #print("def : dump - dumpp - DIAG FRAME : {}".format(each_frm))
        for each_sig in each_frm["Signals"]:
            #print("{}: {}, {} ;".format(each_sig['SignalName'],int(each_sig['Length']),int(each_sig['InitValue'])))
            f.write("\t{}: {}, {} ;\n".format(each_sig['SignalName'],int(each_sig['Length']),int(each_sig['InitValue'])))
    f.write('}\n')

    f.write('Diagnostic_frames {\n')
    for each_frm in Diag:
        f.write("\t{}: {} {{\n".format(each_frm['FrameName'],hex(int(each_frm['FrameID']))))
        #print("def : dump - dumpp - DIAG FRAME : {}".format(each_frm))
        for each_sig in each_frm["Signals"]:
            #print("{}: {}, {} ;".format(each_sig['SignalName'],int(each_sig['Length']),int(each_sig['InitValue'])))
            f.write("\t\t{}, {} ;\n".format(each_sig['SignalName'],int(each_sig['StartBit'])))
        f.write('\t}\n')
    f.write('}\n')

    # Sporadic frames (optional)
    sheet = 'Other Frames'
    table = wb.sheet_by_name(sheet)
    sf = 0
    for row in range(table.nrows):
        frame_data = table.row_values(row)
        if frame_data[0] != 'sporadic_frames':
            continue
        else:
            f.write('Sporadic_frames {\n')
            sf = 1
            break

    for row in range(table.nrows):
        frame_data = table.row_values(row)
        if frame_data[0] != 'sporadic_frames':
            continue
        else:
            f.write(
                '\t' + frame_data[1] + ' : ' + frame_data[4] + ';\n')
    if sf == 1:
        f.write('}\n\n')

    # Event triggered frames (optional)
    sheet = 'Other Frames'
    table = wb.sheet_by_name(sheet)
    etf = 0
    for row in range(table.nrows):
        frame_data = table.row_values(row)
        if frame_data[0] != 'event_triggered_frames':
            continue
        else:
            f.write('Event_triggered_frames {\n')
            etf = 1
            break

    for row in range(table.nrows):
        frame_data = table.row_values(row)
        if frame_data[0] != 'event_triggered_frames':
            continue
        else:
            f.write('\t' + frame_data[1] + ' : ' + frame_data[2] + ', ' + str(int(frame_data[3])) + ', ' + frame_data[4] + ';\n')
    if etf == 1:
        f.write('}\n\n')
    # Diagnostic frames (optional)

    # Node attributes (Required)
    sheet = 'Node Attributes'
    table = wb.sheet_by_name(sheet)
    f.write('Node_attributes {\n')

    # read and write node attributes
    for row in range(table.nrows):
        node_data = table.row_values(row)

        # only slave node in node attributes (use if to ensure data available)
        if node_data[1] == 'slave':
            f.write('\t' + node_data[0] + ' {\n')
            f.write('\t\t' + 'LIN_protocol = "' + str(node_data[6]) + '";\n')
            f.write('\t\t' + 'configured_NAD = ' + str(format(int(node_data[4]), '#x')) + ';\n')
            if node_data[5] != '/':
                f.write('\t\t' + 'initial_NAD = ' + str(format(int(node_data[5]), '#x')) + ';\n')
            f.write('\t\t' + 'product_id = ' + str(format(int(node_data[7]), '#x')) + ', ' +
                    str(format(int(node_data[8]),'#x')) + ', ' + str(int(node_data[9])) + ';\n')
            if node_data[14] != '/':
                f.write('\t\t' + 'response_error = ' + str(node_data[14]) + ';\n')
            if node_data[15] != '/':
                f.write('\t\t' + 'fault_state_signals = ' + str(node_data[15]) + ';\n')
            f.write('\t\t' + 'P2_min = ' + str(int(node_data[10])) + ' ms;\n')
            f.write('\t\t' + 'ST_min = ' + str(int(node_data[11])) + ' ms;\n')
            if node_data[12] != '/':
                f.write('\t\t' + 'N_As_timeout = ' + str(int(node_data[12])) + ' ms;\n')
            if node_data[13] != '/':
                f.write('\t\t' + 'N_Cr_timeout = ' + str(int(node_data[13])) + ' ms;\n')
            f.write('\t\tconfigurable_frames {\n')  # + '\t\t}\n\t}\n')

            print("def : dump - dumpp - TRACE BUG : {}".format(node_data[16]))
            print("def : dump - dumpp - TRACE BUG : {}".format(node_data[16]))

            cf = node_data[16].split(', ')

            if(len(cf) >= 2):
                if cf[1].isdigit():
                    for i in range(0, len(cf), 2):
                        f.write('\t\t\t' + cf[i] + ' = ' + str(format(int(cf[i + 1]), '#06x')) + ';\n')
                    f.write('\t\t}\n\t}\n')
                elif type(cf[1]) == str:
                    for i in range(len(cf)):
                        f.write('\t\t\t' + cf[i] + ';\n')
                    f.write('\t\t}\n\t}\n')
            else:
                f.write('\t\t\t' + cf[0] + ';\n')
                f.write('\t\t}\n\t}\n')

    f.write('}\n\n')

    # Schedule tables (Required)
    sheet = 'Schedule Tables'
    table = wb.sheet_by_name(sheet)
    f.write('Schedule_tables {\n')

    nowtable = ''
    # read and write schedule tables
    for row in range(1, table.nrows):
        st_data = table.row_values(row)

        # common tables
        if not st_data[2].startswith('assign'):

            # new table detected
            if st_data[0] != '':

                # first table in excel
                if nowtable == '':
                    f.write('\t' + st_data[0] + ' {\n')
                    nowtable = st_data[0]

                # other tables in excel
                elif nowtable != '':
                    f.write('\t}\n')
                    f.write('\t' + st_data[0] + ' {\n')
                    nowtable = st_data[0]
                f.write('\t\t' + st_data[1] + ' delay ' + str(int(st_data[3])) + ' ms;\n')

            # slots in current table
            elif st_data[0] == '':
                f.write('\t\t' + st_data[1] + ' delay ' + str(int(st_data[3])) + ' ms;\n')

        # assign tables (leak of other types tables)
        else:

            # use dict to convert data formats
            assigndict = {'assign_nad': 'AssignNAD',
                          'assign_frame_id_range': 'AssignFrameIdRange',
                          'assign_frame_id': 'AssignFrameId'}

            # new table detect
            if st_data[0] != '':

                # first table in excel
                if nowtable == '':
                    f.write('\t' + st_data[0] + ' {\n')
                    nowtable = st_data[0]

                # other table in excel
                elif nowtable != '':
                    f.write('\t}\n')
                    f.write('\t' + st_data[0] + ' {\n')
                    nowtable = st_data[0]

                # writer assign tables
                f.write('\t\t' + assigndict[st_data[2]] + ' {')

                # assign nad
                if st_data[2] == 'assign_nad':
                    f.write(st_data[4] + '}' + ' delay ' + str(int(st_data[3])) + ' ms;\n')
                # assign frame id range
                elif st_data[2] == 'assign_frame_id_range':
                    f.write(
                        st_data[4] + ', ' + str(int(st_data[6])) + '}' + ' delay ' + str(int(st_data[3])) + ' ms;\n')

                # assign frame id
                elif st_data[2] == 'assign_frame_id':
                    f.write(st_data[4] + ', ' + str(st_data[5]) + '}' + ' delay ' + str(int(st_data[3])) + ' ms;\n')

            # slots in current table
            elif st_data[0] == '':

                # write assign table
                f.write('\t\t' + assigndict[st_data[2]] + ' {')

                # assign nad
                if st_data[2] == 'assign_nad':
                    f.write(st_data[4] + '}' + ' delay ' + str(int(st_data[3])) + ' ms;\n')

                # assign frame id range
                elif st_data[2] == 'assign_frame_id_range':
                    f.write(
                        st_data[4] + ', ' + str(int(st_data[6])) + '}' + ' delay ' + str(int(st_data[3])) + ' ms;\n')

                # assign frame id
                elif st_data[2] == 'assign_frame_id':
                    f.write(st_data[4] + ', ' + str(st_data[5]) + '}' + ' delay ' + str(int(st_data[3])) + ' ms;\n')
    f.write('\t}\n}\n\n')
    # Signal encoding type (optional)
    sheet = 'Frame and Signal Attributes'
    table = wb.sheet_by_name(sheet)
    encode = 0
    for row in range(1,table.nrows):
        encode_data = table.row_values(row)
        print("def : dump - dumpp - FIND BUG : SIGNAL ENCODING : {}".format(encode_data))
        if encode_data[9] != '/':
            encode = 1
            break
    if encode == 1:
        f.write('Signal_encoding_types {\n')
        signal_representation = dict()
        for row in range(1, table.nrows):
            encode_data = table.row_values(row)
            if encode_data[9] != '/':
                print("def : dump - dumpp - SIGNAL ENCODING TYPES - BEFORE : {}".format(encode_data[9]))
                encode_data[9] = encode_data[9].replace(' ', '')
                encode_data[9] = encode_data[9].replace('\n', '')
                print("def : dump - dumpp - SIGNAL ENCODING TYPES - AFTER : {}".format(encode_data[9]))
                encoding = encode_data[9].split(',')
                if encoding[0] not in signal_representation.keys():
                    f.write('\t' + encoding[0] + ' {\n')
                    signal_representation[encoding[0]] = encode_data[3]
                    for idx in range(len(encoding[1:])):
                        if encoding[idx] == 'logical':
                            f.write('\t\tlogical_value, ' + encoding[idx + 1] + ', "' + encoding[idx + 2] + '";\n')
                            idx += 3
                        elif encoding[idx] == 'physical':
                            if encoding[idx + 5] != "None":
                                f.write('\t\tphysical_value, ' + encoding[idx + 1] + ', ' + encoding[idx + 2] + ', ' +
                                        encoding[idx + 3] + ', ' + encoding[idx + 4] + ', "' + encoding[idx + 5] + '";\n')
                            else:
                                f.write('\t\tphysical_value, ' + encoding[idx + 1] + ', ' + encoding[idx + 2] + ', ' +
                                        encoding[idx + 3] + ', ' + encoding[idx + 4] + ', ;\n')
                            idx += 6
                    f.write('\t}\n')

                else:
                    signal_representation[encoding[0]] += ', ' + encode_data[3]

        f.write('}\n\n')

    # Signal representation (optional)
    if encode == 1:
        f.write('Signal_representation {\n')
        for key, val in signal_representation.items():
            f.write('\t' + key + ': ' + val + ';\n')
        f.write('}\n')
    f.close()
