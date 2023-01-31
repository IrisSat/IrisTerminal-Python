#!/usr/bin/python3

# Build required code:
# $ ./examples/buildall.py
#
# Start zmqproxy (only one instance)
# $ ./build/zmqproxy
#
# Run server, default enabling ZMQ interface:
# $ LD_LIBRARY_PATH=build PYTHONPATH=build python3 examples/python_bindings_example_server.py
#

import os
import time
import sys
import serial
import threading

import libcsp_py3 as libcsp

# def breakPacket(packet):
#     data = bytearray(libcsp.packet_get_data(packet))
#     return data
#
# def makePacket(data : bytearray):
#     packet = libcsp.buffer_get(len(data))
#     if len(data) > 0:
#         libcsp.packet_set_data(packet, data)
#         return packet
#     return None
#
# def getConn(server, port):
#     if server not in self.server_connection or port not in self.server_connection[server]:
#         try:
#             if server == 4 or server == 5 or server == 6:  # I hate this
#                 conn = libcsp.connect(libcsp.CSP_PRIO_NORM, server, port, 1000, libcsp.CSP_O_CRC32)
#             else:
#                 conn = libcsp.connect(libcsp.CSP_PRIO_NORM, server, port, 1000000000,
#                                       libcsp.CSP_SO_HMACREQ | libcsp.CSP_SO_CRC32REQ | libcsp.CSP_SO_XTEAREQ)
#         except Exception as e:
#             print(e)
#             return None
#
#         self.server_connection[server][port] = conn
#     return self.server_connection[server][port]

def csp_server():
    sock = libcsp.socket()
    libcsp.bind(sock, libcsp.CSP_ANY)
    libcsp.listen(sock, 5)

    libcsp.ping(4)

    # buf = bytearray([0, 1, 3, 4, 5, 6])
    # packet = makePacket(buf)
    # conn = getConn(server, port)
    # libcsp.send(conn, packet)
    # libcsp.buffer_free(packet)
    #
    # packet_addr = libcsp.csp_buffer_get(100)
    # packet = cast(packet_addr, p_packet)
    # msg = "Hello " + str(i)
    # # print "Client sending: " + msg
    # msg_str_bytes = array("B", msg)
    # msg_byte_array = bytearray(msg_str_bytes)
    # raw_bytes = (c_ubyte * 256)(*(msg_byte_array))
    # packet.contents.data = raw_bytes
    # packet.contents.length = sizeof(raw_bytes)
    # libcsp.csp_send(conn, packet, 1000)

    # while True:
    #     # wait for incoming connection
    #     conn = libcsp.accept(sock, libcsp.CSP_MAX_TIMEOUT)
    #     if not conn:
    #         continue
    #
    #     print ("connection: source=%i:%i, dest=%i:%i" % (libcsp.conn_src(conn),
    #                                                      libcsp.conn_sport(conn),
    #                                                      libcsp.conn_dst(conn),
    #                                                      libcsp.conn_dport(conn)))
    #
    #     while True:
    #         # Read all packets on the connection
    #         packet = libcsp.read(conn, 100)
    #         if packet is None:
    #             break
    #
    #         if libcsp.conn_dport(conn) == 10:
    #             # print request
    #             data = bytearray(libcsp.packet_get_data(packet))
    #             length = libcsp.packet_get_length(packet)
    #             print ("got packet, len=" + str(length) + ", data=" + ''.join('{:02x}'.format(x) for x in data))
    #             # send reply
    #             data[0] = data[0] + 1
    #             reply = libcsp.buffer_get(1)
    #             libcsp.packet_set_data(reply, data)
    #             libcsp.sendto_reply(packet, reply, libcsp.CSP_O_NONE)
    #
    #         else:
    #             # pass request on to service handler
    #             libcsp.service_handler(conn, packet)


if __name__ == "__main__":

    # Get input arguments
    print('\nIrisTerminal')
    if len(sys.argv) < 3:
        print('***ERROR: not enough input arguments. Please specify the serial port and baud rate.')
        quit()
    port = sys.argv[1]
    baud_rate = sys.argv[2]
    print(f'-Port: {port}\n-Baud Rate: {baud_rate}\n')

    # Open serial port
    # ser = serial.Serial(port, baud_rate, timeout=1000000, parity=serial.PARITY_EVEN, rtscts=1)
    ser = serial.Serial(port,
                        baudrate=baud_rate,
                        bytesize=8,
                        parity='N',
                        stopbits=2,
                        timeout=1)

    # init csp
    libcsp.init(9, "Iris Ground", "bindings", "1.2.3", 100, 1024)

    # ser = serial.Serial("/dev/ttyVirtualS0",
    #                     baudrate=115200,
    #                     bytesize=8,
    #                     parity='N',
    #                     stopbits=2,
    #                     timeout=1)

    libcsp.kiss_init(port, ser.baudrate, 512, 'uart')
    # #libcsp.zmqhub_init(27, "localhost")
    #libcsp.rtable_set(0, 0, "KISS")
    stringBuild = "4/5 UART"
    libcsp.rtable_load(stringBuild)
    libcsp.route_start_task()

    print("Hostname: %s" % libcsp.get_hostname())
    print("Model:    %s" % libcsp.get_model())
    print("Revision: %s" % libcsp.get_revision())
    #
    print("Routes:")
    libcsp.print_routes()

    # start CSP server
    threading.Thread(target=csp_server).start()

    # if not ser.isOpen():
    #     ser.open()
    # Example: write to the serial port
    # ser.write(b'Welcome to IrisTerminal')
    # ser.write(b'TESTE1\n')
    # response = ser.readline()
    # print(f'Response: {response}')
    # for i, x in enumerate(response):
    #     print(f'-[{i}]: {x}')
    # response = response.strip()
    # response = response.decode('ascii')
    # print(f'Response: {response}')
    #
    # # response = response.decode('utf-8')
    # print(f'Response: {response}')
    # for i in range(3):
    #     response = ser.readline(10000)
    #     try:
    #         response = response.decode('utf-8')
    #     except:
    #         print('Could not convert to UTF-8')
    #     print(f'Response: {response}')
    # # Close serial port
    # ser.close()
