import socket
import os
import base64
import sys

os.chdir("C:\\Users\\Saim\\OneDrive - University of Colorado at Boulder- Office 365\\Eclipse_Workspace\\STOP AND WAIT PROJECT")
start_flagR="stage1"
file_created_flag=False


UDP_IP = "127.0.0.1"
UDP_PORT = int(sys.argv[1])
RN=0                                #receive next
received_header={}


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    if(start_flagR)=="stage1":
        header, addr = sock.recvfrom(1500)
        print(addr)
        if header: 
            
            header=header.decode("utf8")
            (received_header["SN"],received_header["flag"],received_header["file_name"])=header.split("|||",2)
            print("received header:", received_header)
            
            if received_header["SN"]==str(RN):
                print("\n BEGIN RECEIVING "+ str(received_header["file_name"])+"\n")
                RN=RN^1
                if (file_created_flag==False):
                    received_file_name="Received-"+str(received_header["file_name"])
                    sender_file_name=received_header["file_name"]
                    fh2 = open(received_file_name, 'wb')
                    file_created_flag=True
            else:
                continue
                
            #part of FRAME SEND COMMAND AT THE END
            ack=received_header["SN"]+"|||ACK"  
            MESSAGE = ack.encode(encoding='utf8')
            sock.sendto(MESSAGE, (addr[0], addr[1]))
            start_flagR="stage2"
            print("the ack sent is:    "+ack)
                 
    if(start_flagR)=="stage2":
        header, addr = sock.recvfrom(1500)
        print(addr)
        if header: 
            
            header=header.decode("utf8")
            (received_header["SN"],received_header["flag"],received_header["data"])=header.split("|||",2)
            print("received data:", received_header)
            data_in_bytes=base64.b64decode(received_header["data"])
            
            if not data_in_bytes:
                print("\n ALL DATA RECEIVED")
                start_flagR="stage3"
                continue
                
            if received_header["SN"]==str(RN):
                RN=RN^1
                if not data_in_bytes:
                    print("\n ALL DATA RECEIVED")
                    start_flagR="stage3"
                    continue
                fh2.write(data_in_bytes)
            else:
                continue
            
                
            ack=received_header["SN"]+"|||ACK"  
            MESSAGE = ack.encode(encoding='utf8')
            sock.sendto(MESSAGE, (addr[0], addr[1]))
                        
            print("the ack sent is:    "+ack)
        
    
    
    if(start_flagR)=="stage3":
        #print("entered stage 3")
        fh2.close()
        header, addr = sock.recvfrom(1500)

        if header: 

            header=header.decode("utf8")
            (received_header["SN"],received_header["flag"],received_header["file_name"])=header.split("|||",2)
            #print("received header:", received_header)

            if received_header["SN"]==str(RN) and received_header["flag"]=="FIN":
                RN=RN^1
                print("\n "+str(sender_file_name)+" RECEIVED")
            else:
                continue            
                #print("\n SYN packet successfully received.")
                
            ack=received_header["SN"]+"|||ACK"  
            print("THE LAST ACK SENT BY RECEIVER  "+ack)
            MESSAGE = ack.encode(encoding='utf8')
            sock.sendto(MESSAGE, (addr[0], addr[1]))
            start_flagR="stage4"
            continue
    
    if(start_flagR)=="stage4":
        
        transmissions=1
        while transmissions<7:
            transmissions=transmissions+1        
            fin="0"+"|||FIN"
            print("The Second FIN being sent by receiver  "+fin)
            MESSAGE = fin.encode(encoding='utf8')
            sock.sendto(MESSAGE, (addr[0], addr[1]))
            
            data, addr = sock.recvfrom(1500)
            if data:
                data=data.decode("utf8")
                (received_header["ACK"],received_header["flag"])=data.split("|||")
                if received_header["ACK"]=="0" and received_header["flag"]=="ACK":
                    print("\n This is the received final most ack to the receiver's fin  "+str(received_header))
                    print("\n CONNECTION BEING CLOSED GRACEFULLY AT THE RECEIVER'S END")
                    sock.close()
                    raise SystemExit
                
                    

