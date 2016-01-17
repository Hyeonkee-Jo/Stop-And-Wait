# Stop-And-Wait
Stop-­‐and-­‐wait protocol also can be referred as Alternating bit protocol a method used to send information between two connected devices. It ensures that information is not lost due to dropped packets and that packets are received in the correct order. It is the simplest kind of automatic repeat-­‐request (ARQ) method. A stop-­‐and-­‐wait ARQ sender sends one packet at a time. After sending each packet, the sender doesn't send any further packets until it receives an acknowledgement (ACK) signal. After receiving a valid packet, the receiver sends an ACK, if the ACK does not reach the sender before a certain time, known as the timeout, the sender sends the same packet again.

About the code:

1. The SYN packet is sent and received in the stage 1.

2. The DATA is sent and received in the stage2.

3. The FIN packet is sent and received in stage 3.

4. The bonus termination was handled in stage 4

Refer in line comments for precise info about functioning.
