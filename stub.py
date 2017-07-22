from camera import Camera

print("\n----------------------------------------------\n"
      + "--------- FLIR Tau 2 Camera Emulator ---------\n"
      + "--------------- Version 0.1 ------------------\n"
      + "----------------------------------------------\n"
      + "\n"
      + "Enter packet\n"
      + "   - For now, start each packet with \'0x6E\'.\n"
      + "   - CRC1 and CRC2 currently have no effect,\n"
      + "     but should be included.\n\n"
      + "To quit, enter \'q\'\n")

cam = Camera()
message = ''
while True:
    message = input(">>> ").upper()

    # Check for quit condition
    if message == 'Q':
        cam.save_settings()
        break

    # In case the user didn't enter 0x at the start
    if not message[1] == 'X':
        message = '0x' + message

    packet = {'Process Code': message[2:4],
              'Status': message[4:6],
              'Reserved': message[6:8],
              'Function': message[8:10],
              'Byte Count (MSB)': message[10:12],
              'Byte Count (LSB)': message[12:14],
              'CRC1 (MSB)': message[14:16],
              'CRC1 (LSB)': message[16:18],
              'Argument': message[18:-4],
              'CRC2 (MSB)': message[-4:-2],
              'CRC2 (LSB)': message[-2:]
              }

    try:
        cam.command(packet)
    except Exception as e:
        print(e)
    else:
        reply_str = '0x'
        for v in cam.reply.values():
            reply_str += v

        print("\n" + reply_str + "\n")
