import dhcppython

def make_offer():
    OP = bytes([0x02])
    HTYPE = bytes([0x01])
    HLEN = bytes([0x06])
    HOPS = bytes([0x00])
    XID  = bytes([0x39,0x03,0xF3,0x26])
    SECS = bytes([0x00,0x00])
    FLAGS = bytes([0x00, 0x00])
    CIADDR = bytes([0x00, 0x00, 0x00, 0x00])
    YIADDR = bytes([0xC0, 0xA8, 0x01, 0x64]) #192.168.1.100
    SIADDR = bytes([0xC0, 0xA8, 0x01, 0x01]) #192.168.1.1
    GIADDR = bytes([0x00, 0x00, 0x00, 0x00])
    CHADDR1 = bytes([0x00, 0x05, 0x3C, 0x04])
    CHADDR2 = bytes([0x8D, 0x59, 0x00, 0x00])
    CHADDR3 = bytes([0x00, 0x00, 0x00, 0x00])
    CHADDR4 = bytes([0x00, 0x00, 0x00, 0x00])
    CHADDR5 = bytes(192)
    Magiccookie = bytes([0x63, 0x82, 0x53, 0x63])
    DHCPOptions1 = bytes([53 , 1 , 2]) # DHCP Offer
    DHCPOptions2 = bytes([1 , 4 , 0xFF, 0xFF, 0xFF, 0x00]) #255.255.255.0 subnet mask
    DHCPOptions3 = bytes([3 , 4 , 0xC0, 0xA8, 0x01, 0x01]) #192.168.1.1 router
    DHCPOptions4 = bytes([51 , 4 , 0x00, 0x01, 0x51, 0x80]) #86400s(1 day) IP address lease time
    DHCPOptions5 = bytes([54 , 4 , 0xC0, 0xA8, 0x01, 0x01]) # DHCP server
        
    package = OP + HTYPE + HLEN + HOPS + XID + SECS + FLAGS + CIADDR +YIADDR + SIADDR + GIADDR + CHADDR1 + CHADDR2 + CHADDR3 + CHADDR4 + CHADDR5 + Magiccookie + DHCPOptions1 + DHCPOptions2 + DHCPOptions3 + DHCPOptions4 + DHCPOptions5

    return package


def pack_get():
    OP = bytes([0x02])
    HTYPE = bytes([0x01])
    HLEN = bytes([0x06])
    HOPS = bytes([0x00])
    XID = bytes([0x39, 0x03, 0xF3, 0x26])
    SECS = bytes([0x00, 0x00])
    FLAGS = bytes([0x00, 0x00])
    CIADDR = bytes([0x00, 0x00, 0x00, 0x00])
    YIADDR = bytes([0xC0, 0xA8, 0x01, 0x64])
    SIADDR = bytes([0xC0, 0xA8, 0x01, 0x01])
    GIADDR = bytes([0x00, 0x00, 0x00, 0x00])
    CHADDR1 = bytes([0x00, 0x05, 0x3C, 0x04])
    CHADDR2 = bytes([0x8D, 0x59, 0x00, 0x00])
    CHADDR3 = bytes([0x00, 0x00, 0x00, 0x00])
    CHADDR4 = bytes([0x00, 0x00, 0x00, 0x00])
    CHADDR5 = bytes(192)
    Magiccookie = bytes([0x63, 0x82, 0x53, 0x63])
    DHCPOptions1 = bytes([53 , 1 , 5]) #DHCP ACK(value = 5)
    DHCPOptions2 = bytes([1 , 4 , 0xFF, 0xFF, 0xFF, 0x00]) #255.255.255.0 subnet mask
    DHCPOptions3 = bytes([3 , 4 , 0xC0, 0xA8, 0x01, 0x01]) #192.168.1.1 router
    DHCPOptions4 = bytes([51 , 4 , 0x00, 0x01, 0x51, 0x80]) #86400s(1 day) IP address lease time
    DHCPOptions5 = bytes([54 , 4 , 0xC0, 0xA8, 0x01, 0x01]) #DHCP server

    package = OP + HTYPE + HLEN + HOPS + XID + SECS + FLAGS + CIADDR +YIADDR + SIADDR + GIADDR + CHADDR1 + CHADDR2 + CHADDR3 + CHADDR4 + CHADDR5 + Magiccookie + DHCPOptions1 + DHCPOptions2 + DHCPOptions3 + DHCPOptions4 + DHCPOptions5

    return package



from socket import *

DHCP_SERVER = ('', 67)
DHCP_CLIENT = ('255.255.255.255', 68)

# Create a UDP socket
s = socket(AF_INET, SOCK_DGRAM)
print("server is starting")
# Allow socket to broadcast messages
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

# Bind socket to the well-known port reserved for DHCP servers
s.bind(DHCP_SERVER)
while True:
    try:
        print("waiting for discover")
    # Recieve a UDP message
        msg, addr = s.recvfrom(1024)
        print("recieved")
        
        print("sending offer")
        data = make_offer()
        s.sendto(data,DHCP_CLIENT)
        # Print the client's MAC Address from the DHCP header
        print("Client's MAC Address is " + format(msg[28], 'x'), end = '')
        for i in range(29, 34):
    	    print(":" + format(msg[i], 'x'), end = '')


        while 1: 
            try:
                print("wait on req")
                data,addr = s.recvfrom(1024)
                print("recieved req")

                print("send pack")
                data = pack_get()
                s.sendto(data,DHCP_CLIENT)
                break
            except:
                raise
    except:
        raise

        print()
        
    # Send a UDP message (Broadcast)
    s.sendto(b'Hello World!', DHCP_CLIENT)



