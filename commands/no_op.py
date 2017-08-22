def NO_OP(settings, reply):
    # For all cases where the byte may be currently unknown.
    unknown_byte = '|__|'

    reply['Process Code'] = '6E'

    # NOTE: I'm a little hesitant about hard coding this as '00'. While CAM OK
    # is an alright response, there's no setting for CAM OK, so there's no way
    # to know if the camera, or the emulator rather, really is OK.
    # NOTE: This has been marked on the github as Issue #6
    reply['Status'] = '00'
    reply['Reserved'] = '00'

    # Function code for NO_OP
    reply['Function'] = '00'

    reply['Byte Count (MSB)'] = '00'
    reply['Byte Count (LSB)'] = '00'

    # NOTE: I'm also hesitant to hard-coded CRC values as they should be able to
    # be calculated. Of course, this may mean chaging from using strings as
    # representations of bytes, to actually using bytes, which we may have to
    # do anyway.
    reply['CRC1 (MSB)'] = unknown_byte
    reply['CRC1 (LSB)'] = unknown_byte

    reply['Argument'] = ''

    reply['CRC2 (MSB)'] = unknown_byte
    reply['CRC2 (LSB)'] = unknown_byte

    return settings, reply
