from vidstream.audio import AudioSender
from vidstream.audio import AudioReceiver
import threading
import socket

# Finding Local IP
hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)
print("System Name is: " + hostname)
print("System IP Address is: " + IPAddr)

# Basically just input your local IP for receiver/sender side.
# Make sure to change firewall settings for other connector and use local IP

# Local IP
receiver = AudioReceiver('127.0.0.1', 9999)
receive_thread = threading.Thread(target=receiver.start_server)

# Target IP
# sender = AudioSender('127.0.0.1', 5555)
# sender_thread = threading.Thread(target=sender.start_stream)

receive_thread.start()
# sender_thread.start()