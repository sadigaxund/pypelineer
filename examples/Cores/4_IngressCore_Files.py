'''
    www.youtube.com/@Pypelineer
'''

from pypelineer.cores import IngressCore, IngressType

import io

class ReadFileBuffer(IngressCore, Type=IngressType.FUNCTION):
    def __init__(self, file_path: str, buffer_size: int = 1024):
        self.file_path = file_path
        self.buffer_size = buffer_size
        super().__init__(None, False)

    def constructor(self):
        # Open file and buffer to read it's contents
        self.file = open(self.file_path, 'rb')
        self.buffer = io.BufferedReader(self.file, self.buffer_size)
        self.chunk = self.buffer.read()
        self.end_of_file = False

    def destructor(self, exc_type, exc_value, traceback):
        if self.buffer is not None:
            self.buffer.close()
        if self.file is not None:
            self.file.close()

    def available(self):
        return not self.end_of_file
    
    def iterate(self):
        # Load next chunk of data
        self.chunk = self.buffer.read()
        
    def produce(self):
        # EOF condition
        if self.chunk == b'':
            self.end_of_file = True
            return
        
        # Decode contents and divide into seperate lines
        content = self.chunk.decode('utf-8')
        lines = content.splitlines()
        yield from lines

if __name__ == '__main__':
    
    with ReadFileBuffer('sample_file.txt', 256) as reader:
        for line in reader:
            print(line)
