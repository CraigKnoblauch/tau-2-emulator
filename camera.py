import json
import os
import platform

# An import must be added for each command a developer impolements
from commands import no_op as NO_OP

class Camera:

    def __init__(self):
        self.reply = {'Process Code': '6E',
                      'Status': '|_|_|',
                      'Reserved': '00',
                      'Function': '|_|_|',
                      'Byte Count (MSB)': '|_|_|',
                      'Byte Count (LSB)': '|_|_|',
                      'CRC1 (MSB)': '|_|_|',
                      'CRC1 (LSB)': '|_|_|',
                      'Argument': '|_|_|',
                      'CRC2 (MSB)': '|_|_|',
                      'CRC2 (LSB)': '|_|_|',
                     }

        # Load current settings from the curr_settings json file
        self.settings = self.load_settings()

        # Must be edited to include each command a developer implements
        self.function_codes = {'00': NO_OP,
                            #   '01': SET_DEFAULTS,
                            #   '02': CAMERA_RESET,
                            #   '03': RESTORE_FACTORY_DEFAULTS,
                            #   '04': SERIAL_NUMBER,
                            #   '65': SERIAL_NUMBER,
                            #   '05': GET_REVISION,
                            #   '07': BAUD_RATE,
                            #   '0A': GAIN_MODE,
                            #   '0B': FFC_MODE_SELECT,
                            #   '0C': DO_FFC,
                            #   '0D': FFC_PERIOD,
                            #   '0E': FFC_TEMP_DELTA,
                            #   '0F': VIDEO_MODE,
                            #   '10': VIDEO_PALETTE,
                            #   '11': VIDEO_ORIENTATION,
                            #   '12': DIGITAL_OUTPUT_MODE,
                            #   '13': AGC_TYPE,
                            #   '14': CONTRAST,
                            #   '15': BRIGHTNESS,
                            #   '18': BRIGHTNESS_BIAS,
                            #   '1C': ACE_CORRECT,
                            #   '1E': LENS_NUMBER,
                            #   '1F': SPOT_METER_MODE,
                            #   '20': READ_SENSOR,
                            #   '21': EXTERNAL_SYNC,
                            #   '22': ISOTHERM,
                            #   '23': ISOTHERM_THRESHOLDS,
                            #   '25': TEST_PATTERN,
                            #   '26': VIDEO_COLOR_MODE,
                            #   '2A': GET_SPOT_METER,
                            #   '2B': SPOT_DISPLAY,
                            #   '2C': DDE_GAIN,
                            #   '2F': SYMBOL_CONTROL,
                            #   '31': SPLASH_CONTROL,
                            #   '32': EZOOM_CONTROL,
                            #   '3C': FFC_WARN_TIME,
                            #   '3E': AGC_FILTER,
                            #   '3F': PLATEAU_LEVEL,
                            #   '43': GET_SPOT_METER_DATA,
                            #   '4C': AGC_ROI,
                            #   '4D': SHUTTER_TEMP,
                            #   '55': AGC_MIDPOINT,
                            #   '66': CAMERA_PART,
                            #   '68': READ_ARRAY_AVERAGE,
                            #   '6A': MAX_AGC_GAIN,
                            #   '70': PAN_AND_TILT,
                            #   '72': VIDEO_STANDARD,
                            #   '79': SHUTTER_POSITION,
                            #   '82': TRANSFER_FRAME,
                            #   '8E': TLIN_COMMANDS,
                            #   'B1': CORRECTION_MASK,
                            #   'C4': MEMORY_STATUS,
                            #   'C6': WRITE_NVFFC_TABLE,
                            #   'D2': READ_MEMORY,
                            #   'D4': ERASE_MEMORY_BLOCK,
                            #   'D5': GET_NV_MEMORY_SIZE,
                            #   'D6': GET_MEMORY_ADDRESS,
                            #   'D8': GAIN_SWITCH_PARAMS,
                            #   'E2': DDE_THRESHOLD,
                            #   'E3': SPATIAL_THRESHOLD,
                            #   'E5': LENS_RESPONSE_PARAMS,
                            }

        self.valid_function_codes = ['00', '01', '02', '03', '04', '65', '05',
                                     '07', '0A', '0B', '0C', '0D', '0E', '0F',
                                     '10', '11', '12', '13', '14', '15', '18',
                                     '1C', '1E', '1F', '20', '21', '22', '23',
                                     '25', '26', '2A', '2B', '2C', '2F', '31',
                                     '32', '3C', '3E', '3F', '43', '4C', '4D',
                                     '55', '66', '68', '6A', '70', '72', '79',
                                     '82', '8E', 'B1', 'C4', 'C6', 'D2', 'D4',
                                     'D5', 'D6', 'D8', 'E2', 'E3', 'E5']

    def command(self, packet):
        """Calls the appropriate command function based on the function code
        recieved
        """
        self.restore_reply()
        try: # Keep this try until all commands are implemented

            # Reply if the user provided an invalid funciton code
            if not packet['Function'] in self.valid_function_codes:
                self.invalid_function_code_reply(packet['Function'])
            else:
                self.settings, self.reply = self.function_codes[packet['Function']]()
        except TypeError: # If there was no return from the command function,
                          # it has not yet been implemented
            command_name = self.function_codes[packet['Function']].__name__  # commands.command_name
            command_name = command_name[9:].upper() # COMMAND_NAME
            raise Exception("\nEmulator has no support for "
                            + command_name
                            + "\n")

    def restore_reply(self):
        """Restores reply to default"""
        self.reply = {'Process Code': '6E',
                      'Status': '|_|_|',
                      'Reserved': '00',
                      'Function': '|_|_|',
                      'Byte Count (MSB)': '|_|_|',
                      'Byte Count (LSB)': '|_|_|',
                      'CRC1 (MSB)': '|_|_|',
                      'CRC1 (LSB)': '|_|_|',
                      'Argument': '|_|_|',
                      'CRC2 (MSB)': '|_|_|',
                      'CRC2 (LSB)': '|_|_|',
                     }

    def invalid_function_code_reply(self, function):
        """Sets the reply for an invalid funciton code"""
        self.reply['Function'] = function
        self.reply['Status'] = '06'  # CAM_UNDEFINED_FUNCTION_ERROR

    def where_settings(self):
        """Determines the correct path to the curr_settings json file"""
        work_dir = os.getcwd()

        if platform.system().lower() == 'windows':
            work_dir = work_dir + "\\" + "storage\\"
        else:
            work_dir = work_dir + "/" + "storage/"

        filename = work_dir + "curr_settings.json"
        return filename

    def load_settings(self):
        """Loads current settings from the curr_settings json file"""
        filename = self.where_settings()
        with open(filename) as f:
            s = json.load(f)

        return s

    def save_settings(self):
        """Saves the settings of this instance to the curr_settings json file"""
        filename = self.where_settings()
        with open(filename, 'w') as f:
            json.dump(self.settings, f)
