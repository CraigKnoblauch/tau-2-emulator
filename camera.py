import json
import os
import platform

# imports lines from command.py
from command_imports import *

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
        self.function_codes = {'00': no_op.NO_OP,
                            #   '01': set_defaults.SET_DEFAULTS,
                            #   '02': camera_reset.CAMERA_RESET,
                            #   '03': restore_factory_defaults.RESTORE_FACTORY_DEFAULTS,
                            #   '04': serial_number.SERIAL_NUMBER,
                            #   '65': serial_number.SERIAL_NUMBER,
                            #   '05': get_revision.GET_REVISION,
                            #   '07': baud_rate.BAUD_RATE,
                            #   '0A': gain_mode.GAIN_MODE,
                            #   '0B': ffc_mode_select.FFC_MODE_SELECT,
                            #   '0C': do_ffc.DO_FFC,
                            #   '0D': ffc_period.FFC_PERIOD,
                            #   '0E': ffc_temp_delta.FFC_TEMP_DELTA,
                            #   '0F': video_mode.VIDEO_MODE,
                            #   '10': video_palette.VIDEO_PALETTE,
                            #   '11': video_orientation.VIDEO_ORIENTATION,
                            #   '12': digital_output_mode.DIGITAL_OUTPUT_MODE,
                            #   '13': agc_type.AGC_TYPE,
                            #   '14': contrast.CONTRAST,
                            #   '15': brightness.BRIGHTNESS,
                            #   '18': brightness_bias.BRIGHTNESS_BIAS,
                            #   '1C': ace_correct.ACE_CORRECT,
                            #   '1E': lens_number.LENS_NUMBER,
                            #   '1F': spot_meter_mode.SPOT_METER_MODE,
                            #   '20': read_sensor.READ_SENSOR,
                            #   '21': external_sync.EXTERNAL_SYNC,
                            #   '22': isotherm.ISOTHERM,
                            #   '23': isotherm_thresholds.ISOTHERM_THRESHOLDS,
                            #   '25': test_pattern.TEST_PATTERN,
                            #   '26': video_color_mode.VIDEO_COLOR_MODE,
                            #   '2A': get_spot_meter.GET_SPOT_METER,
                            #   '2B': spot_display.SPOT_DISPLAY,
                            #   '2C': dde_gain.DDE_GAIN,
                            #   '2F': symbol_control.SYMBOL_CONTROL,
                            #   '31': splash_control.SPLASH_CONTROL,
                            #   '32': ezoom_control.EZOOM_CONTROL,
                            #   '3C': ffc_warn_time.FFC_WARN_TIME,
                            #   '3E': agc_filter.AGC_FILTER,
                            #   '3F': plateau_level.PLATEAU_LEVEL,
                            #   '43': get_spot_meter_data.GET_SPOT_METER_DATA,
                            #   '4C': agc_roi.AGC_ROI,
                            #   '4D': shutter_temp.SHUTTER_TEMP,
                            #   '55': agc_midpoint.AGC_MIDPOINT,
                            #   '66': camera_part.CAMERA_PART,
                            #   '68': read_array_average.READ_ARRAY_AVERAGE,
                            #   '6A': max_agc_gain.MAX_AGC_GAIN,
                            #   '70': pan_and_tilt.PAN_AND_TILT,
                            #   '72': video_standard.VIDEO_STANDARD,
                            #   '79': shutter_position.SHUTTER_POSITION,
                            #   '82': transfer_frame.TRANSFER_FRAME,
                            #   '8E': tlin_commands.TLIN_COMMANDS,
                            #   'B1': correction_mask.CORRECTION_MASK,
                            #   'C4': memory_status.MEMORY_STATUS,
                            #   'C6': write_nvffc_table.WRITE_NVFFC_TABLE,
                            #   'D2': read_memory.READ_MEMORY,
                            #   'D4': erase_memory_block.ERASE_MEMORY_BLOCK,
                            #   'D5': get_nv_memory_size.GET_NV_MEMORY_SIZE,
                            #   'D6': get_memory_address.GET_MEMORY_ADDRESS,
                            #   'D8': gain_switch_params.GAIN_SWITCH_PARAMS,
                            #   'E2': dde_threshold.DDE_THRESHOLD,
                            #   'E3': spatial_threshold.SPATIAL_THRESHOLD,
                            #   'E5': lens_response_params.LENS_RESPONSE_PARAMS,
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

    # TODO: This is giving strange string outs for certain functional inupts
    # We may need to run through this on a debugger and see what's getting
    # activated where.
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
                # self.settings, self.reply = self.determine_command(packet['Function'])
                print(self.determine_name(self.function_codes[packet['Function']].__name__))
                self.settings, self.reply = self.function_codes[packet['Function']](self.settings, self.reply)

        # This will need to be modified for new implementation
        except TypeError: # If there was no return from the command function,
                          # it has not yet been implemented
            raise Exception("\nEmulator has no support for "
                            + self.determine_name(self.function_codes[packet['Function']].__name__)
                            + "\n")

    def determine_name(self, full_name):
        """Parses command_name.COMMAND_NAME to return COMMAND_NAME"""
        dot_i = full_name.index('.')
        return full_name[dot_i+1:]

    def determine_command(self, function_code):
        """Uses multiple if statements to check the function code and call the
        correct command. When the correct command is found, Exception is raised
        """
        # The try except mentality from command function will have to be used here
        if function_code == '00':
            settings, reply = no_op.NO_OP(self.settings, self.reply)
            return settings, reply

        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')
        #
        # if function_code == '':
        #     self.settings, self.reply = _()
        #     raise Exception('_ command determined')

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
