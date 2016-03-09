import socket
import os
import base64
import sys

i=1

os.chdir("C:\\Users\\Saim\\OneDrive - University of Colorado at Boulder- Office 365\\Eclipse_Workspace\\STOP AND WAIT PROJECT")
start_flagS="stage1"

UDP_IP,UDP_PORT=(sys.argv[2]).split(":")

UDP_PORT=int(UDP_PORT)
sock =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
received={}

SN=0                            #send next
flag=["SYN","DATA","FIN"]
can_send=True
sending_file_name=str(sys.argv[1])

def read_in_parts():
    while True:
        data = fh.read(1024)
        yield data


while True:
    if(start_flagS=="stage1"):
        if(can_send==True):
            frame_header= str(SN)+"|||"+str(flag[0])+"|||"+str(sending_file_name)
            MESSAGE = frame_header.encode(encoding='utf8')
            sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
            print(" SYN PACKET SENT BY SENDER")
            SN=SN^1
            sock.settimeout(0.5)
            can_send=False
    
        try:
            data, addr = sock.recvfrom(1024)
            
            if data:
                data=data.decode("utf8")
                (received["ACK"],received["flag"])=data.split("|||")
                print("\n This ack has been received from the receiver  "+str(received))

                if received["ACK"]==str(SN^1) and received["flag"]=="ACK":
                    can_send=True
                    start_flagS="stage2"
                    print("\n VALID ACK. SYN handshake done successfully. Ready to transfer file.")
                    
        except:
            can_send=True
            continue                   #will again send the SYN packet
        
        
    if start_flagS=="stage2":
        if(can_send==True):
            
            fh=open(sending_file_name,'rb')
            for filepiece in read_in_parts():       
                
                filepiece=base64.b64encode(filepiece).decode()
                frame_data= str(SN)+"|||"+str(flag[1])+"|||"+filepiece
                MESSAGE = frame_data.encode(encoding='utf8')
                sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
                print("\n Part of data sent")
                SN=SN^1
                
                if not filepiece:
                    print("\n ALL DATA SENT")
                    start_flagS="stage3"
                    fh.close()
                    print("\n File Closed")
                    break
                
                sock.settimeout(0.5)
                can_send=False
                
                while True:
                    try:
                        data, addr = sock.recvfrom(1024)
                        
                        if data:
                            data=data.decode("utf8")
                            (received["ACK"],received["flag"])=data.split("|||")
                                
                            if received["ACK"]==str(SN^1) and received["flag"]=="ACK":
                                print("\n VALID ACK TO DATA RECEIVED"+ str(received))
                                can_send=True
                                start_flag=False
                                break
                                
                                print("\n VALID ACK TO DATA RECEIVED"+ str(received))
                                
                    except:
                        can_send=True
                        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
                        continue
                    
    if(start_flagS=="stage3"):
        if(can_send==True):
            frame_header= str(SN)+"|||"+str(flag[2])+"|||"              #FIRST FIN SENT BY SENDER
            MESSAGE = frame_header.encode(encoding='utf8')
            sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
            print("\n FIRST FIN PACKET SENT BY SENDER IS : "+ frame_header)
            SN=SN^1
            sock.settimeout(0.5)
            can_send=False
    
        try:
            data, addr = sock.recvfrom(1024)
            
            if data:
                data=data.decode("utf8")
                (received["ACK"],received["flag"])=data.split("|||")
                print("\n This ack has been received from the receiver  "+str(received))
                    
                if received["ACK"]==str(SN^1) and received["flag"]=="ACK":
                    start_flagS="stage4"
                    can_send=True
                    continue
                    

                    ##print("ACK OF FIRST FIN RECEIVED BY RECEIVER IS: "+received)
                    #can_send=True
                    ##start_flagS="stage4"
                    #print("\n "+sending_file_name+" is successfully sent to "+str(sys.argv[2]))
                    #break
        except:
            can_send=True
            continue 
        
    if(start_flagS=="stage4"):
        if(can_send==True):
            
            if i==1:
                print("\n "+sending_file_name+" is successfully sent to "+str(sys.argv[2]))       
                i=2
            
            sock.settimeout(2.0)
            try:
                data, addr = sock.recvfrom(1024)
                sock.settimeout(None)
                if data:
                    data=data.decode("utf8")
                    (received["ACK"],received["flag"])=data.split("|||")
                    print("This Is The Received second FIN from receiver: "+str(received))
                    
                    if received["ACK"]=="0" and received["flag"]=="FIN":
                        last_ack= "0"+"|||"+"ACK"
                        MESSAGE = last_ack.encode(encoding='utf8')
                        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
                        print("\n ACK TO THE RECEIVER'S FIN SENT "+str(MESSAGE))
                        continue
                    
            except:
                print("CONNECTION CLOSED GRACEFULLY ON RECEIVERS SIDE")
                sock.close()
                raise SystemExit
            
            
            continue
                                 

            

