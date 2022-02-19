from socketIO_client import SocketIO
import RPi.GPIO as GPIO

# TODO: instead of static configuration encode this in a json and provide facility to load config from file.
volume_up = 12
volume_down = 16
mute_unmute = 5
pause_play = 6
go_next = 13
go_prev = 9

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
        self._socketIO.emit('volume', '+')

    def volume_down(self, pin_unused):
        print("volume_down")
        self._socketIO.emit('volume', '-')

    def mute_unmute(self, pin_unused):
        print("mute_unmute")
        self.getStatus(timeout=0.1)
        while self.status == None:
            self.wait_for_server(timeout=0.1)
        cmd = 'mute'
        if self.status['mute'] == True:
            cmd = 'unmute'
        self._socketIO.emit(cmd)

    def pause_play(self, pin_unused):
        print("pause_play")
        self.getStatus(timeout=0.1)
        while self.status == None:
            self.wait_for_server(timeout=0.1)
        cmd = 'play'
        if self.status['status'] == 'play':
            cmd = 'pause'
        self._socketIO.emit(cmd)

    def go_prev(self, pin_unused):
        print("go_prev")
        self._socketIO.emit('prev')

    def go_next(self, pin_unused):
        print("go_next")
        self._socketIO.emit('next')

    def getStatus(self, timeout=None):
        self.status = None
        self._socketIO.emit('getState')
        self.wait_for_server(timeout=timeout)

def config_gpio(volumio):
    GPIO.setmode(GPIO.BCM)
    # volume up
    GPIO.setup(volume_up, GPIO.IN)
    GPIO.add_event_detect(volume_up, GPIO.RISING)
    GPIO.add_event_callback(volume_up, volumio.volume_up)
    # volume down
    GPIO.setup(volume_down, GPIO.IN)
    GPIO.add_event_detect(volume_down, GPIO.RISING)
    GPIO.add_event_callback(volume_down, volumio.volume_down)
    # mute_unmute
    GPIO.setup(mute_unmute, GPIO.IN)
    GPIO.add_event_detect(mute_unmute, GPIO.RISING)
    GPIO.add_event_callback(mute_unmute, volumio.mute_unmute)
    # pause_play
    GPIO.setup(pause_play, GPIO.IN)
    GPIO.add_event_detect(pause_play, GPIO.RISING)
    GPIO.add_event_callback(pause_play, volumio.pause_play)
    # go_prev
    GPIO.setup(go_prev, GPIO.IN)
    GPIO.add_event_detect(go_prev, GPIO.RISING)
    GPIO.add_event_callback(go_prev, volumio.go_prev)
    # go_next
    GPIO.setup(go_next, GPIO.IN)
    GPIO.add_event_detect(go_next, GPIO.RISING)
    GPIO.add_event_callback(go_next, volumio.go_next)


if __name__ == '__main__':
    v = Volumio('localhost', 3000)
    config_gpio(v)
    v.getStatus()
    while(1):
        # TODO: instead of polling switch to callbacks for all buttons
        v.wait_for_server(timeout=0.1)

