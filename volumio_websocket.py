from socketIO_client import SocketIO
import RPi.GPIO as GPIO

# TODO: instead of static configuration encode this in a json and provide facility to load config from file.
BUTTON_VOLUME_UP = 12
BUTTON_VOLUME_DOWN = 16
BUTTON_MUTE_UNMUTE = 5
BUTTON_PAUSE_PLAY = 6
BUTTON_GO_NEXT = 13
BUTTON_GO_PREV = 9

class Volumio:
    """A connection to Volumio"""

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._socketIO = SocketIO(host, port, wait_for_connection=False)
        self._socketIO.on('connect', self.on_connect)
        self._socketIO.on('disconnect', self.on_disconnect)
        self._socketIO.on('reconnect', self.on_reconnect)
        self._socketIO.on('pushState', self.statusInfo)
        self.status = None

    def wait_for_server(self, timeout=None):
        self._socketIO.wait(timeout)

    def on_connect(self):
        print(f'connected to {self.host}:{self.port}')

    def on_disconnect(self):
        print(f'disconnected from {self.host}:{self.port}')

    def on_reconnect(self):
        print(f'reconnected to {self.host}:{self.port}')

    def statusInfo(self, *args):
        print(args)
        self.status = args

    def volume_up(self, pin_unused):
        print("volume_up")
#        self._socketIO.emit('volume', '+')

    def volume_down(self, pin_unused):
        print("volume_down")
#        self._socketIO.emit('volume', '-')

    def mute_unmute(self, pin_unused):
        print("mute_unmute")
#        self.getStatus(timeout=0.1)
#        while self.status == None:
#            self.wait_for_server(timeout=0.1)
#        cmd = 'mute'
#        if self.status['mute'] == True:
#            cmd = 'unmute'
#        self._socketIO.emit(cmd)

    def pause_play(self, pin_unused):
        print("pause_play")
#        self.getStatus(timeout=0.1)
#        while self.status == None:
#            self.wait_for_server(timeout=0.1)
#        cmd = 'play'
#        if self.status['status'] == 'play':
#            cmd = 'pause'
#        self._socketIO.emit(cmd)

    def go_prev(self, pin_unused):
        print("go_prev")
#        self._socketIO.emit('prev')

    def go_next(self, pin_unused):
        print("go_next")
#        self._socketIO.emit('next')

    def getStatus(self, timeout=None):
        self.status = None
        self._socketIO.emit('getState')
        self.wait_for_server(timeout=timeout)

def config_gpio(volumio):
    default_bouncetime=300
    GPIO.setmode(GPIO.BCM)
    # volume up
    GPIO.setup(BUTTON_VOLUME_UP, GPIO.IN)
    GPIO.add_event_detect(BUTTON_VOLUME_UP, GPIO.RISING, bouncetime=default_bouncetime)
    GPIO.add_event_callback(BUTTON_VOLUME_UP, volumio.volume_up)
    # volume down
    GPIO.setup(BUTTON_VOLUME_DOWN, GPIO.IN)
    GPIO.add_event_detect(BUTTON_VOLUME_DOWN, GPIO.RISING, bouncetime=default_bouncetime)
    GPIO.add_event_callback(BUTTON_VOLUME_DOWN, volumio.volume_down)
    # mute_unmute
    GPIO.setup(BUTTON_MUTE_UNMUTE, GPIO.IN)
    GPIO.add_event_detect(BUTTON_MUTE_UNMUTE, GPIO.RISING, bouncetime=default_bouncetime)
    GPIO.add_event_callback(BUTTON_MUTE_UNMUTE, volumio.mute_unmute)
    # pause_play
    GPIO.setup(BUTTON_PAUSE_PLAY, GPIO.IN)
    GPIO.add_event_detect(BUTTON_PAUSE_PLAY, GPIO.RISING, bouncetime=default_bouncetime)
    GPIO.add_event_callback(BUTTON_PAUSE_PLAY, volumio.pause_play)
    # go_prev
    GPIO.setup(BUTTON_GO_PREV, GPIO.IN)
    GPIO.add_event_detect(BUTTON_GO_PREV, GPIO.RISING, bouncetime=default_bouncetime)
    GPIO.add_event_callback(BUTTON_GO_PREV, volumio.go_prev)
    # go_next
    GPIO.setup(BUTTON_GO_NEXT, GPIO.IN)
    GPIO.add_event_detect(BUTTON_GO_NEXT, GPIO.RISING, bouncetime=default_bouncetime)
    GPIO.add_event_callback(BUTTON_GO_NEXT, volumio.go_next)


if __name__ == '__main__':
    v = Volumio('localhost', 3000)
    config_gpio(v)
    v.getStatus()
    while(1):
        # TODO: instead of polling switch to callbacks for all buttons
        v.wait_for_server(timeout=0.1)

