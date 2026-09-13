import socket
import threading

services = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    5432: "PostgreSQL",
    8080: "HTTP"
}

target = input("Enter the target IP: ")
start = int(input("Enter the starting port: "))
end = int(input("Enter the ending port: "))

open_ports = 0
open_ports_lock = threading.Lock()


def scan_port(port):
    global open_ports

    s = socket.socket()
    s.settimeout(1)

    try:
        s.connect((target, port))

        service = services.get(port, "Unknown")

        try:
            banner = s.recv(1024).decode(errors="ignore").strip()
        except:
            banner = "No banner received"

        with open_ports_lock:
            open_ports += 1

        print("Port", port, "is OPEN")
        print("    Service:", service)
        print("    Banner:", banner)

    except:
        pass

    finally:
        s.close()


threads = []

print()
print("====================================")
print("       PYTHON PORT SCANNER")
print("====================================")
print("Target:", target)
print("Ports:", start, "-", end)
print()
print("Scanning...")
print()


for port in range(start, end + 1):

    thread = threading.Thread(
        target=scan_port,
        args=(port,)
    )

    threads.append(thread)
    thread.start()


for thread in threads:
    thread.join()


print()
print("====================================")
print("Scan completed.")
print("Total open ports found:", open_ports)
print("====================================")
       



