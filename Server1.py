import socket
import threading
from zlib import decompress

import pygame

WIDTH = 800
HEIGHT = 650

Threads = []
Connections = []
Addresses = []


def recvall(conn, length):
    """ Retreive all pixels. """
    buf = b''
    while len(buf) < length:
        data = conn.recv(length - len(buf))
        if not data:
            return data
        buf += data
    return buf

def handleClient(conn):
    print("1 for viewing clients ")
    print("2 for connecting clients ")
    print("3 to quit")
    options = int(input("Enter choice :"))
    if options == "":
        print("Empty Input ")
    if options == 1:
        print("Available Clients :")
        for i in range(len(Addresses)):
            print(i, " ", Addresses[i])
        handleClient(conn)
    elif options == 2:
        clientNO = int(input("Enter client no. "))
        if (clientNO <= len(Addresses) and len(Addresses) != 0):
            conn = Connections[clientNO]
            addr = Addresses[clientNO]
            command = input("Enter command start")
            conn.send(command.encode())
            pygame.init()
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            clock = pygame.time.Clock()
            # watching = True
            try:
                while(True):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            watching = False
                            break
                    # Retreive the size of the pixels length, the pixels length and pixels
                    size_len = int.from_bytes(conn.recv(1), byteorder='big')
                    size = int.from_bytes(conn.recv(size_len), byteorder='big')
                    pixels = decompress(recvall(conn, size))

                    # Create the Surface from raw pixels
                    img = pygame.image.fromstring(pixels, (WIDTH, HEIGHT), 'RGB')

                    # Display the picture
                    screen.blit(img, (0, 0))
                    pygame.display.flip()
                    clock.tick(60)
                    # while input('') != 'STOP':
                    #     continue
                    # break
            finally:
                print("PIXELS: ")
                handleClient(conn)
            handleClient(conn)
        else:
            print("Invalid Input")
            handleClient(conn)
    elif options == 3:
        exit()
    else:
        print("Invalid input")



host = '127.0.0.1'
port = 6969
sock = socket.socket()
sock.bind((host, port))

def main():
    ''' machine lhost'''
    print("Listening ....")
    sock.listen(10)
    while True:
        conn, addr = sock.accept()
        Connections.append(conn)
        Addresses.append(addr)
        print("Accepted ....", addr)
        t = threading.Thread(target=handleClient(conn))
        t1 = threading.Thread(target=main())
        t1.start()
        while input('') == 'client':
            continue


        # pygame.init()
        # screen = pygame.display.set_mode((WIDTH, HEIGHT))
        # clock = pygame.time.Clock()
        # watching = True

        # try:
        #     while watching:
        #         for event in pygame.event.get():
        #             if event.type == pygame.QUIT:
        #                 watching = False
        #                 break
        #
        #         # Retreive the size of the pixels length, the pixels length and pixels
        #         size_len = int.from_bytes(conn.recv(1), byteorder='big')
        #         size = int.from_bytes(conn.recv(size_len), byteorder='big')
        #         pixels = decompress(recvall(conn, size))
        #
        #         # Create the Surface from raw pixels
        #         img = pygame.image.fromstring(pixels, (WIDTH, HEIGHT), 'RGB')
        #
        #         # Display the picture
        #         screen.blit(img, (0, 0))
        #         pygame.display.flip()
        #         clock.tick(60)
        # finally:
        #     print("PIXELS: ", pixels)
        #     sock.close()


if __name__ == "__main__":
    main()  