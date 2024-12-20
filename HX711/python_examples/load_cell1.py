#!/usr/bin/env python3
import RPi.GPIO as GPIO  # import GPIO
from hx711 import HX711  # import the class HX711
from server_raspi import ServerRas

server_ras = ServerRas()

try:
    GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
    # Create an object hx which represents your real hx711 chip
    # Required input parameters are only 'dout_pin' and 'pd_sck_pin'
    hx = HX711(dout_pin=6, pd_sck_pin=5)
    #hx2 = HX711(dout_pin=19, pd_sck_pin=13)

    #print(f'DOUT: {GPIO.input(DOUT_PIN)}')
    
    # measure tare and save the value as offset for current channel
    # and gain selected. That means channel A and gain 128
    print(hx)
    #print(hx2)
    
    err = hx.zero()
    #err2 = hx2.zero()

    print(err)
    #print(err2)


    # check if successful
    if err:
        raise ValueError('Tare is unsuccessful.')

    reading = hx.get_raw_data_mean()
    #reading2 = hx2.get_raw_data_mean()

    if reading:  # always check if you get correct value or only False
        # now the value is close to 0
        print('Data subtracted by offset but still not converted to units:',
              reading)
        #print('Data subtracted by offset but still not converted to units2:',
              #reading2)
    else:
        print('invalid data', reading)
        #print('invalid data2', reading2)

    # In order to calculate the conversion ratio to some units, in my case I want grams,
    # you must have known weight.
    input('Put known weight on the scale and then press Enter')
    reading = hx.get_data_mean()
    #reading2 = hx2.get_data_mean()

    if reading:
        print('Mean value from HX711 subtracted by offset:', reading)
        #print('Mean value from HX711 subtracted by offset2:', reading2)
        known_weight_grams = input(
            'Write how many grams it was and press Enter: ')
        try:
            value = float(known_weight_grams)
            print(value, 'grams')
        except ValueError:
            print('Expected integer or float and I have got:',
                  known_weight_grams)

        # set scale ratio for particular channel and gain which is
        # used to calculate the conversion to units. Required argument is only
        # scale ratio. Without arguments 'channel' and 'gain_A' it sets
        # the ratio for current channel and gain.
        ratio = reading / value  # calculate the ratio for channel A and gain 128
        #ratio2 = reading2 / value
        
        hx.set_scale_ratio(ratio)  # set ratio for current channel
        #hx2.set_scale_ratio(ratio2)


        print('Ratio is set.')
    else:
        raise ValueError('Cannot calculate mean value. Try debug mode. Variable reading:', reading)
        #raise ValueError('Cannot calculate mean value. Try debug mode. Variable reading2:', reading2)

    # Read data several times and return mean value
    # subtracted by offset and converted by scale ratio to
    # desired units. In my case in grams.
    print("Now, I will read data in infinite loop. To exit press 'CTRL + C'")
    input('Press Enter to begin reading')
    print('Current weight on the scale in grams is: ')
    
    while True:
        weight = hx.get_weight_mean(30)
        #weight2 = hx2.get_weight_mean(30)

        print(weight, 'g')
        #print(weight2, 'g')

        server_ras.send_data(f"{weight}")
        
        #server_ras.send_weight(weight)

        #obj = server_ras.receive_data()
        #print(f'obj = {obj}')
        #if obj is None:
           # print('no receive data')
        #elif obj is not None:
            #real_weight = hx.get_weight_mean(25)
            #print('--------')
            #print(real_weight)
            #server_ras.send_data(f"{real_weight}")

except (KeyboardInterrupt, SystemExit):
    print('Bye :)')

finally:
    server_ras.close()
    GPIO.cleanup()
