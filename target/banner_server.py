#!/usr/bin/env python3
"""
Banner server for the Nmap CTF lab.
Listens on a port and serves a fake service banner the way real services do.
Handles concurrent connections and stays responsive to nmap's various probes.
"""
import socket
import sys
import threading
import time

def handle_client(conn, banner, protocol):
    try:
        if protocol == "ftp":
            # FTP servers send the banner immediately on connect
            conn.sendall(banner.encode() + b"\r\n")
            # Then wait for commands and respond generically
            conn.settimeout(2)
            try:
                data = conn.recv(1024)
                if data:
                    conn.sendall(b"500 Command not understood\r\n")
            except socket.timeout:
                pass

        elif protocol == "ssh":
            # SSH servers send the banner immediately
            conn.sendall(banner.encode() + b"\r\n")
            # Wait briefly for client response
            conn.settimeout(2)
            try:
                conn.recv(1024)
            except socket.timeout:
                pass

        elif protocol == "http":
            # HTTP servers wait for a request first, then respond
            conn.settimeout(2)
            try:
                request = conn.recv(4096)
                # Build a proper HTTP response with the banner as the Server header
                body = b"<html><body><h1>NovaCorp Web Portal</h1></body></html>"
                response = (
                    b"HTTP/1.1 200 OK\r\n"
                    b"Server: " + banner.encode() + b"\r\n"
                    b"Content-Type: text/html\r\n"
                    b"Content-Length: " + str(len(body)).encode() + b"\r\n"
                    b"Connection: close\r\n"
                    b"\r\n" + body
                )
                conn.sendall(response)
            except socket.timeout:
                pass

    except Exception as e:
        pass
    finally:
        try:
            conn.close()
        except:
            pass


def serve(port, banner, protocol):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", port))
    sock.listen(50)
    print(f"[*] Listening on port {port} ({protocol})", flush=True)
    while True:
        try:
            conn, addr = sock.accept()
            t = threading.Thread(target=handle_client, args=(conn, banner, protocol), daemon=True)
            t.start()
        except Exception as e:
            print(f"[!] Error on port {port}: {e}", flush=True)
            time.sleep(0.1)


if __name__ == "__main__":
    port = int(sys.argv[1])
    protocol = sys.argv[2]
    banner = sys.argv[3]
    serve(port, banner, protocol)
