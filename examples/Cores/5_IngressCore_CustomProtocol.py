'''
    www.youtube.com/@Pypelineer
'''
from pypelineer.cores import IngressCore, IngressType

import socket
import struct

class DataTransferProtocol(IngressCore, Type=IngressType.FUNCTION):
    def constructor(self):
        server_host = '127.0.0.1'
        server_port = 65432
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.max_bytes = 1024

        # Connect to the server
        self.client_socket.connect((server_host, server_port))
        # Receive header with total lines of data
        header = self.client_socket.recv(4)

        self.dataset_size, = struct.unpack('>I', header)
        self.offset = 0
        self.limit = 5

    def destructor(self, exc_type, exc_value, traceback):
        if self.client_socket is not None:
            self.client_socket.close()

    def available(self):
        return self.offset < self.dataset_size
    
    def iterate(self):
        self.offset += self.limit
    
    def produce(self):
        # Send offset and limit to the server
        request = struct.pack('>II', self.offset, self.limit)
        self.client_socket.sendall(request)

        # Calculate for each batch
        recieved_rows = 0
        expected_rows = min(self.limit, self.dataset_size - self.offset)

        # Receive until the expected number is reached
        while recieved_rows < expected_rows:
            data_bytes = self.client_socket.recv(self.max_bytes)
            data_text = data_bytes.decode("utf-8")
            rows = data_text.split('\n')

            # Process each row
            for row in rows:
                # Only non-empty rows
                if row:
                    yield row
                    recieved_rows += 1
                    
                    if recieved_rows >= expected_rows:
                        break

if __name__ == "__main__":
    with DataTransferProtocol() as protocol:
        for row in protocol:
            print(row)