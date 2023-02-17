import os
import json
import sys
import ldfparser
import LDFstruct
import attr
from load import loadd
from load import loadfs
from load import loadst
import xlsxwriter

def write_excel_line(worksheet, row, col, row_array, style):

    print("def : dump - write_excel_line")

    # type: (xlsxwriter.workbook.Worksheet, int, int, typing.Sequence[typing.Any], xlsxwriter.workbook.Format) -> int

    for item in row_array:
        worksheet.write(row, col, item, style)
        col += 1
    return col


def dumpp(ldf, outfile):

    print("def : dump - dumpp")

    workbook = xlsxwriter.Workbook(outfile)
    worksheet = workbook.add_worksheet('LIN Attributes')
    global sty_header
    sty_header = workbook.add_format({'bold': True,
                                      'font_name': 'Verdana',
                                      'font_size': 8,
                                      'align': 'center',
                                      'valign': 'vcenter'})
    sty_header.set_text_wrap()

    global sty_first_frame
    sty_first_frame = workbook.add_format({'font_name': 'Verdana',
                                           'font_size': 8,
                                           'font_color': 'black', 'top': 1,
                                           'align': 'center',
                                           'valign': 'vcenter'
                                           })

    global sty_signal_representation
    sty_signal_representation = workbook.add_format({'font_name': 'Verdana',
                                                     'font_size': 8,
                                                     'font_color': 'black', 'top': 1,
                                                     'valign': 'vcenter'
                                                     })
    sty_signal_representation.set_text_wrap()

    global sty_white
    sty_white = workbook.add_format({'font_name': 'Verdana',
                                     'font_size': 8,
                                     'font_color': 'white',
                                     'align': 'center',
                                     'valign': 'vcenter'
                                     })

    global sty_norm
    sty_norm = workbook.add_format({'font_name': 'Verdana',
                                    'font_size': 8,
                                    'font_color': 'black',
                                    'align': 'center',
                                    'valign': 'vcenter',
                                    })
    sty_norm.set_text_wrap()

    LIN_head_top = [
        'LIN protocol version',
        'LIN language version',
        'LIN speed [kbps]',
        'Channel name'
    ]

    row_array = LIN_head_top

    for col in range(0, len(row_array)):
        worksheet.set_column(col, col, 10)

    # write head_top
    write_excel_line(worksheet, 0, 0, row_array, sty_header)

    # set row to row 1 (row = 0 is header)
    row = 1

    # get data from load.py
    frontRow = loadd("LIN", ldf)

    # write excel lines and return col
    col = write_excel_line(worksheet, row, 0, frontRow, sty_first_frame)

    # add filter and freeze head_top
    worksheet.freeze_panes(1, 0)

    # second worksheet
    worksheet = workbook.add_worksheet('Node Attributes')

    Node_head_top = [
        'Node name',
        'Role',
        'Time base [ms]',
        'Jitter [ms]',
        'Configured NAD',
        'Init NAD',
        'Protocol version',
        'Supplied ID',
        'Function ID',
        'Variant ID',
        'P2 min [ms]',
        'ST min [ms]',
        'N_As_timeout [ms]',
        'N_Cr_timeout [ms]',
        'Response error',
        'Fault state signals',
        'Configurable frames'
    ]

    row_array = Node_head_top

    for col in range(0, len(row_array)):
        worksheet.set_column(col, col, 10)

    # write head_top
    write_excel_line(worksheet, 0, 0, row_array, sty_header)

    # set row to row 1 (row = 0 is header)
    row = 1

    # get data from load.py
    frontRow = loadd("node master", ldf)

    # write excel lines and return col
    col = write_excel_line(worksheet, row, 0, frontRow, sty_first_frame)
    row += 1

    for ldfnode in ldf["node_attributes"]:
        frontRow = loadd("node slaves", ldfnode)
        col = write_excel_line(worksheet, row, 0, frontRow, sty_first_frame)
        row += 1

    # add filter and freeze head_top
    worksheet.freeze_panes(1, 0)

    # third worksheet
    worksheet = workbook.add_worksheet('Frame and Signal Attributes')
    fs_head_top = [
        'Frame name',
        'Frame ID',
        'Size [Byte]',
        'Signal name',
        'Startbit',
        'Width [bit]',
        'Init value',
        'Publisher',
        'Subscribers',
        'Signal representation'
    ]

    row_array = fs_head_top

    for col in range(0, len(row_array)):
        worksheet.set_column(col, col, 10)
    worksheet.set_column(9, 9, 30)

    # write head_top
    write_excel_line(worksheet, 0, 0, row_array, sty_header)

    # set row to row 1 (row = 0 is header)
    row = 1

    # get data from load.py
    for ldff in ldf["frames"]:
        for signal in ldff["signals"]:
            frontRow = loadfs("frame and signal", ldff, ldf, signal)
            worksheet.set_row(row, 60)
            # write excel lines and return col
            col = write_excel_line(worksheet, row, 0, frontRow, sty_signal_representation)

            # Signal representation exist
            if frontRow[-1] != '/':
                col = write_excel_line(worksheet, row, 0, frontRow[0:-1], sty_first_frame)
            else:
                col = write_excel_line(worksheet, row, 0, frontRow, sty_first_frame)
            row += 1

    # add filter and freeze head_top
    worksheet.autofilter(0, 0, row, len(fs_head_top) - 1)
    worksheet.freeze_panes(1, 0)

    # forth worksheet
    worksheet = workbook.add_worksheet('Other Frames')
    etf_head_top = [
        'Type',
        'Event name',
        'Collision resolving table',
        'Frame ID',
        'Frames'
    ]

    row_array = etf_head_top

    for col in range(0, len(row_array)):
        worksheet.set_column(col, col, 15)

    # write head_top
    write_excel_line(worksheet, 0, 0, row_array, sty_header)

    # set row to row 1 (row = 0 is header)
    row = 1

    # get data from load.py
    if 'event_triggered_frames' in ldf.keys():
        for etf in ldf["event_triggered_frames"]:
            frontRow = loadd("event_triggered_frames", etf)
            col = write_excel_line(worksheet, row, 0, frontRow, sty_first_frame)
            row += 1

    if 'sporadic_frames' in ldf.keys():
        for sf in ldf["sporadic_frames"]:
            frontRow = loadd("sporadic_frames", sf)
            col = write_excel_line(worksheet, row, 0, frontRow, sty_first_frame)
            row += 1

    # add filter and freeze head_top
    worksheet.autofilter(0, 0, row, len(etf_head_top) - 1)
    worksheet.freeze_panes(1, 0)

    # fifth worksheet
    worksheet = workbook.add_worksheet('Schedule Tables')

    st_head_top = [
        'Table name',
        'Slot',
        'Type',
        'Delay [ms]',
        'Node',
        'Frame',
        'Frame index'
    ]

    row_array = st_head_top

    for col in range(0, len(row_array)):
        worksheet.set_column(col, col, 15)

    # write head_top
    write_excel_line(worksheet, 0, 0, row_array, sty_header)

    # set row to row 1 (row = 0 is header)
    row = 1

    # get data from load.py
    nowtable = str()
    for ldfst in ldf["schedule_tables"]:
        for ldfstslot in ldfst["schedule"]:
            frontRow = loadst("schedule_tables", ldfst, ldfstslot)

            # new table detected
            if nowtable != frontRow[0]:
                col = write_excel_line(worksheet, row, 0, frontRow, sty_first_frame)

            # slots in same table
            else:
                col = write_excel_line(worksheet, row, 1, frontRow[1:], sty_norm)

            nowtable = frontRow[0]
            row += 1

    # add filter and freeze head_top
    worksheet.autofilter(0, 0, row, len(st_head_top) - 1)
    worksheet.freeze_panes(1, 0)

    # save file
    workbook.close()
