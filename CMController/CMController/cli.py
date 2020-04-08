'''
CLI
Use to send instructions to the Merlin via serial connection.

March 2, 2020: Still need to finishing implementing sending serial commands.
'''

from CMController.cmc import CMController
import re
import subprocess
import sys
import fileinput


def cli_run():
    print("\n*** Welcome to CMController Demo Mode! ***")
    cm_controller = CMController()
    cm_controller.connect()

    if (cm_controller.is_connected() == False):
        devices = cm_controller.list_serial_devices()
        while True:
            buffer = input("\nPlease select one of the available serial devices: ")
            if (buffer == "done"):
                sys.exit(0)
            try:
                cm_controller.connect(devices[int(buffer)])
                if (cm_controller.is_connected()):
                    break
            except:
                print("Invalid. Try again.")


    while True:
        buffer = input(':: ')
        if (buffer == "done"):
            cm_controller.device.close()
            sys.exit(0)
        else: 
            command = buffer
            cm_controller.send_command(command)


if __name__ == "__main__":
    cli_run()