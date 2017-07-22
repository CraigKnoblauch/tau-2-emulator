import os
import platform
import json

# Note that this will reset curr_settings.json

# Settings dictionary is has a list as a value where:
#     element 0 is the state of the setting
#     element 1 is the description
#
# EXCEPT for ROI Coordinates which have a dictionary as
# value
#
# Empty strings mean the value is unknown and should be
# filled in as more is learned about the camer a later
# revisions are made.
#
#     VbC "Varies by Configuration"
settings = {'Baud Rate': ['0x0000', 'Auto Baud'],
            'Gain Mode': ['VbC', ''],
            'FFC Mode': ['VbC', ''],
            'FFC Interval (High-Gain State)': ['0x01C2', '7200 Frames'],
            'FFC Interval (Low-Gain State)': ['0x0708', '1800 Frames'],
            'FFC Temp Interval (High-Gain State)': ['0x0005', '0.6C'],
            'FFC Temp Interval (Low-Gain State)': ['0x0005', '0.6C'],
            'Video Palette': ['0x0000', 'Palette 0 = White Hot'],
            'Video Mode': ['0x0000', 'Real-time, unzoomed'],
            'Video Orientation': ['0x0000', 'Normal Orientation'],
            'Digital Output Modes': ['VbC', ''],
            'AGC Algorithm': ['0x0000', 'Plateau Equalization'],
            'SSO Percent': ['0x000F', '15%'],
            'Contrast': ['0x0020', '32'],
            'Brightness': ['0x2000', '8192'],
            'Brightness Bias': ['0x0000', '0'],
            'Tail Size': ['0x000A', '1%'],
            'ACE Correction': ['0x0003', '3'],
            'Lens Number': ['0x0000', '0'],
            'Spot Meter Mode': ['Vbc', ''],
            'External Sync Mode': ['0x0000', '0'],
            'Isoterhm Mode': ['VbC', ''],
            'Lower Isoterhm Threshold': ['0x005A', '90%'],
            'Middle Isoterhm Threshold': ['0x005C', '92%'],
            'Upper Isotherm Threshold': ['0x005F', '95%'],
            'Saturation Isotherm Threshold': ['0x0064', '100%'],
            'Video Color Mode': ['0x0001', 'Color Enabled'],
            'Spot Display Mode': ['VbC', ''],
            'DDE Gain': ['n/a', 'auto'],
            'Ezoom Width': ['VbC | Max Value', ''],
            'FFC Warn Time': ['0x003C', '60 Frames'],
            'AGC Filter': ['0x0010', '16'],
            'Plateau Level': ['Vcb', ''],
            'Spot Meter Coordinates': ['Vbc', ''],
            'ROI Coordinates': {'Top': '-50%',
                                'Left': '-50%',
                                'Bottom': '+50%',
                                'Right': '+50%'},
            '2x Zoom ROI Coordinates': {'Top': '',
                                        'Left': '',
                                        'Bottom': '',
                                        'Right': ''},
            '4x Zoom ROI Coordinates': {'Top': '',
                                        'Left': '',
                                        'Bottom': '',
                                        'Right': ''},
            '8x Zoom ROI Coordinates': {'Top': '',
                                        'Left': '',
                                        'Bottom': '',
                                        'Right': ''},
            'AGC Midpoint': ['0x007F', '127'],
            'Max Gain': ['0x0008', '8'],
            'Pan/Tilt Coordinates': ['0,0', ''],
            'Video Standard': ['VbC', ''],
            'TLinear Enable': ['VbC', ''],
            'TLinear Resolution': ['VbC', ''],
            'Shutter Profile': ['VbC', ''],
            'Correction Mask': ['0x083F', 'All enabled except supplemental offset'],
            'Gain Swtich, High-to-Low Temperature Threshold': ['0x008C', '140C'],
            'Gain Switch, Low-to-High Temperature Threshold': ['0x0064', '100C'],
            'Gain Swtich, High-to-Low Population Threshold': ['0x005F', '95%'],
            'Gain Switch, Low-to-High Population Threshold': ['0x0014', '20%'],
            'DDE Threshold': ['n/a', 'default mode is automatic'],
            'DDE Mode/Spatial Threshold': ['0x010A', 'Byte 0:01, automatic mode'],
            'DDE Blend Mode': ['0x0001', 'Enabled'],
            'Lens Response Parameters': ['VbC', ''],
           }

files = ["default_settings.json", "curr_settings.json"]

work_dir = os.getcwd() # Should be in cam-stub/tools
work_dir = work_dir[:-5] # Should be in cam-stub
work_dir += "storage" # Should be in cam-stub/storage

# For BOTH files
for filename in files:
    # Makes sure all Windows users will have a \ instead of a /
    if platform.system().lower == 'windows':
        filename = work_dir + "\\" + filename
    else:
        filename = work_dir + "/" + filename

    # Dump settings into a default_settings.json file in cam-stub/storage
    with open(filename, 'w') as f:
        json.dump(settings, f)
