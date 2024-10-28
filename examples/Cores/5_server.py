import socket
import struct

# Sample CSV dataset
SAMPLE_DATA = [
    "ID,Name,Product,Quantity,Price,Date",
    "1,John Doe,Widget A,3,19.99,2023-10-01",
    "2,Jane Smith,Gadget B,1,24.99,2023-10-02",
    "3,Emily Davis,Widget C,2,15.99,2023-10-03",
    "4,Michael Brown,Widget A,5,19.99,2023-10-04",
    "5,Sarah Wilson,Gadget A,1,24.99,2023-10-05",
    "6,David Lee,Widget B,2,29.99,2023-10-06",
    "7,Laura Taylor,Gadget C,4,34.99,2023-10-07",
    "8,James Anderson,Widget A,3,19.99,2023-10-08",
    "9,Amy Thomas,Widget C,1,15.99,2023-10-09",
    "10,Robert Jackson,Gadget B,2,24.99,2023-10-10",
    "11,Linda White,Widget B,1,29.99,2023-10-11",
    "12,Chris Harris,Widget A,5,19.99,2023-10-12",
    "13,Patricia Martin,Widget C,2,15.99,2023-10-13",
    "14,Thomas Clark,Gadget A,3,24.99,2023-10-14",
    "15,Nancy Rodriguez,Widget B,4,29.99,2023-10-15",
    "16,Daniel Lewis,Widget C,3,15.99,2023-10-16",
    "17,Karen Walker,Widget A,1,19.99,2023-10-17",
    "18,Joseph Hall,Gadget B,3,24.99,2023-10-18",
    "19,Betty Allen,Widget C,2,15.99,2023-10-19",
    "20,Mark Young,Gadget A,5,24.99,2023-10-20"
]

def start_server(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Server listening on {host}:{port}")

        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")

            # Send header with total length of data (total number of lines)
            total_lines = len(SAMPLE_DATA)
            header = struct.pack('>I', total_lines)
            conn.sendall(header)
            print(f"Sent header with total lines: {total_lines}")

            # Handle client requests for offset and limit
            while True:
                try:
                    # Receive offset and limit from client
                    offset_limit_data = conn.recv(8)
                    if not offset_limit_data:
                        break  # Connection closed by client

                    offset, limit = struct.unpack('>II', offset_limit_data)
                    print(f"Received offset: {offset}, limit: {limit}")

                    # Get requested lines based on offset and limit
                    data_chunk = SAMPLE_DATA[offset:offset + limit]

                    # Send each line separately in CSV format
                    for line in data_chunk:
                        conn.sendall(line.encode() + b'\n')
                        
                except Exception as e:
                    print(f"Error: {e}")
                    break

if __name__ == "__main__":
    start_server()
