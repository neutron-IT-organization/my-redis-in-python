import socket
import sys
from resp import Resp
import handlers

def main():
    print("Listening on port :6379")

    # Create a new server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 6379))
    server.listen(5)

    while True:
        conn, addr = server.accept()
        print(f"Connection from {addr} has been established.")

        try:
            while True:
                resp = Resp(conn)
                value, err = resp.read()
                if err:
                    print(err)
                    break

                print(value.array[0])

                cmd = value.array[0].bulk if value.array else ""
                print(cmd)
                args = [item.bulk for item in value.array[1:]] if value.array else []
                
                # Print the command and its arguments
                print(f"Received command: {cmd} with arguments: {args}")

                if hasattr(handlers, cmd):
                    getattr(handlers, cmd)(*([resp] + args))
                else:
                    resp.write_error("Unknown command")

        except Exception as e:
            print("Error reading from client:", e)
            sys.exit(1)

        finally:
            conn.close()

if __name__ == "__main__":
    main()
