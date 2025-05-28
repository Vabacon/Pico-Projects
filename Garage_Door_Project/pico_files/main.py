from microdot import Microdot, Response
import network
from machine import Pin
import urequests
import time

print('Initializing...')

# Start connection to the local wireless network.

nic = network.WLAN(network.WLAN.IF_STA)
nic.active(True)
nic.ifconfig(('192.168.30.205', '255.255.255.0', '192.168.30.1', '0.0.0.0'))
nic.connect('BaconWireless', '1905B@c0n')
print('Connecting to wireless network...')
connection_timeout = 60
while not nic.isconnected():
    if connection_timeout > 0:
        connection_timeout -= 1
        time.sleep(1)
    else:
        print('Error: Failed to connect. Timeout.')
        break
    
# ip_info variable contains nic imoup information for retrival.
if nic.isconnected():
    ip_info = nic.ifconfig()
    print('Wireless network connected:')
    print(f'IPv4: {ip_info[0]} \
    \nMask: {ip_info[1]} \
    \nGateway: {ip_info[2]} \
    \nDNS: {ip_info[3]}\n')


# Assignment of relays 1 and 2 to GPIO pins.
relay_pin_1 = Pin(28, Pin.OUT)
relay_pin_2 = Pin(27, Pin.OUT)

def open_relay(relay, delay):
    while delay > 0:
        if relay.value() == True:
            relay.toggle()
            time.sleep(0.2)
            delay -= 1
        else:
            relay.toggle()
            time.sleep(0.2)

# Initialize web services application.

app = Microdot()

@app.route('/', methods=['GET'])
async def index(request):
    return "Garage Door Main Page.\n\r You're not supposed to be here."

@app.get('/door1')
async def index(request):
    open_relay(relay_pin_1, 3)
    
@app.get('/door2')
async def index(request):
    open_relay(relay_pin_2, 5)

# This starts the application after checking if wireless connection is established.

if not nic.isconnected():
    print('Failure to connect to the wireless network. \
    \nExiting application.')
else:
    app.run(host='192.168.30.205', port=8000, debug=True)
