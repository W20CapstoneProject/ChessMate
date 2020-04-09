from CMController.cmc import CMController

i_setup = "0,0,0,0,180"
i_zero = "0,0,0,0,0"

def helloWorld():
    ''' Make the Moveo Arm wave! '''
    cmc = CMController()
    cmc.connect()

    if(cmc.is_connected()):
        cmc.send_command(i_zero)
        cmc.send_command(i_setup)
        cmc.send_command("0,128,0,0,0")

        for i in range(0, 10):
            cmc.send_command("0,0,1000,-50,0")
            cmc.send_command("0,0,-1000,50,180")
        
        cmc.send_command(i_zero)


if __name__ == "__main__":
    helloWorld()
