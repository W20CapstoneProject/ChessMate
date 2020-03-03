'''
Demo
Use to send instructions to the Merlin via serial connection.

March 2, 2020: Still need to finishing implementing sending serial commands.
'''

import cm
import re
import subprocess
import sys
import fileinput


print("\n*** Welcome to CMController Demo Mode! ***")
cm_controller = cm.CMController()
cm_controller.connect()
cm_controller.plot_board()

if (cm_controller.is_connected() == False):
    devices = cm.list_serial_devices()
    while True:
        command = input("\nPlease select one of the available serial devices: ")
        if (command == "done"):
            sys.exit(0)
        try:
            cm_controller.connect(devices[int(command)])
            if (cm_controller.is_connected()):
                break
        except:
            print("Invalid. Try again.")


while True:
    command = input(':: ')
    if (command == "done"):
        cm_controller.device.close()
        sys.exit(0)

    print("Sending command...")
    cm_controller.send_command(command)
