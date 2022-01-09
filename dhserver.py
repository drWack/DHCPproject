import dhcppython
import ipaddress
from socket import *

OpenAddrs = [True,True,True,True,True,True,True,True] #192.168.1.2 - 192.168.1.9
def findFirstOpen():
    for i in range(len(OpenAddrs)):
        if (OpenAddrs[i] == True):
            return i+2
    return -1





DHCP_SERVER = ('0.0.0.0', 67)
DHCP_CLIENT = ('255.255.255.255', 68)

# Create a UDP socket
s = socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET,SO_BROADCAST,1)
print("server is starting")
# Allow socket to broadcast messages
s.bind(DHCP_SERVER)
opt_list = dhcppython.options.OptionList([
dhcppython.options.options.short_value_to_object(51,300)
    ])
while True:
    try:
        print("waiting for discover")
    # Recieve a UDP message
        msg, addr = s.recvfrom(1024)
        pkt = dhcppython.packet.DHCPPacket.from_bytes(msg)
        print("discover recieved")
       # print(pkt) works
        num = findFirstOpen()
        mac = pkt.chaddr
       # offer = dhcppython.packet.DHCPPacket.Offer(yiadder =ipaddress.IPv4Address( "192.168.1." + str(num)), seconds = 86400,tx_id = num)
        offer = dhcppython.packet.DHCPPacket.Offer(mac, seconds=0, tx_id=pkt.xid, yiaddr=ipaddress.IPv4Address('192.168.0.'+str(num)),option_list =opt_list)
        
        
        print("sending offer")
        ready = offer.asbytes
        s.sendto(ready,DHCP_CLIENT)
        # Print the client's MAC Address from the DHCP header
        print("Client's MAC Address is " + format(msg[28], 'x'), end = '')
        for i in range(29, 34):
    	    print(":" + format(msg[i], 'x'), end = '')


        while 1: 
            try:
                print("wait on req")
                data,addr = s.recvfrom(1024)
                print("recieved req")
                req = dhcppython.packet.DHCPPacket.from_bytes(data)
                if(req.op == 'BOOTREQUEST'):
                    print("send pack")
                    ack = dhcppython.packet.DHCPPacket.Ack(mac,seconds = 0,tx_id=pkt.xid, yiaddr=ipaddress.IPv4Address('192.168.0.'+str(num)),option_list =opt_list)
                    OpenAddrs[num-2] = False
                ackmsg = ack.asbytes
                print(ackmsg)
                s.sendto(ackmsg,DHCP_CLIENT)
                break
            except:
                raise
    except:
        raise

        print()
        
    # Send a UDP message (Broadcast)
    s.sendto(b'Hello World!', DHCP_CLIENT)



