from pyrf.devices.thinkrf import WSA4000
from pyrf.sweep_device import SweepDevice
import base64
from PySide import QtCore
import datetime

LINES_PER_PACKET = 2
class playBack(object):
    """
   Class that is used to store FFT data in a CSV file, or open an existing file with
   FFT data.

    :param filename: name of file to open/create 
    """
    
    def __init__(self, callback = None):
        self.file_opened = False
        self.callback = callback
        self.file = None

        self.number_lines = 0
        self.file_name = None
        
    def make_header (self,start,stop):
        import sys
        print 'make header'
        return [[str(start), str(stop), 'Pyrf', sys.byteorder]]
    
    def create_file(self, dir, fileName = None):
        print 'make file'
        if fileName == None:
            fileName =  str(datetime.datetime.now()).replace('.', '-')
            fileName = fileName.replace(':','-')
            fileName = dir + '\\' + fileName + '.csv'
        print fileName
        self.file = QtCore.QFile(fileName)
        self.file.open(QtCore.QIODevice.WriteOnly| QtCore.QIODevice.Text)
         
        
        self.file_opened = True
        
    def save_data(self, start, stop, data):
        print 'save data'
        if self.file_opened:
            header = self.make_header(start,stop)
            out = QtCore.QTextStream(self.file)
            b64_data = base64.b64encode(str(data))
            for h in header[0]:
                out << h << ','
            out << '\n'
            out << str(b64_data) << '\n'

        
    def close_file(self):
        print 'close file'
        self.file_opened = False
        self.file.close()
        self.csv_writer = None
        self.csv_reader = []
        self.curr_index = 0

    def open_file(self, fileName):

        self.file_name = fileName
        self.curr_index = 0
        
    def read_data(self):

        file = QtCore.QFile(self.file_name)
        file.open(QtCore.QIODevice.ReadOnly| QtCore.QIODevice.Text)

        num_lines = 0
        
        while not file.atEnd():

            line = file.readLine()
            if num_lines == self.curr_index:
                freq_str = line.split(',')
                start = float(freq_str[0])
                stop = float(freq_str[1])
            elif num_lines == self.curr_index + 1:
                raw_data = line
            num_lines += 1

        decoded_data = base64.b64decode(raw_data)
        split_data  = decoded_data.split(', ')
        data = []
        for x in split_data:
            if "[" in x:
                x = x.replace("[","")
            if "]" in x:
                x = x.replace("]","")
            data.append(float(x))
       
        self.curr_index += LINES_PER_PACKET
        if self.curr_index >= num_lines:
            self.curr_index = 0
        file.close()
        return start,stop, data