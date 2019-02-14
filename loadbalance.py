import socket
import threading

srv_ip = ''
port = 1883

brokeraddr = '192.168.1.21'


def HandleConnection():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    sock.bind((srv_ip,port))
    sock.listen(1)
    print('Listening at ',sock.getsockname())
    while True:
        try:
            sc, accsock = sock.accept()
            print('Connection Accept...', accsock)
            data = sc.recvfrom()
            #sendsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #sendsock.connect(brokeraddr,port)
            #sendsock.sendall(msg)
            threading._start_new_thread(balancing, (data,port))

        except KeyboardInterrupt:
            break

#tambahkan dan implementasikan

def balancing(data,prt):
    #wS adalah berat server
    #cConn adalah koneksi server saat ini
    server = ['192.168.1.21','192.168.1.22','192.168.23']
    fwdsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    wS = [10,7,3]
    cConn = [0,0,0]

    for m in range(len(server)):
        if wS[m] > 0:
            for i in range(m+1, len(server)):
                if cConn[m] == 0:
                    fwdsock.connect(server[0],prt)
                elif cConn[m]*wS[i] > cConn[i]*wS[m]:
                    m=i
                    fwdsock.connect(server[m],prt)
                    cConn[m] += 1
                return server[m]

HandleConnection()

