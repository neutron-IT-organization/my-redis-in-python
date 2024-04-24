STRING = b'+'
ERROR = b'-'
INTEGER = b':'
BULK = b'$'
ARRAY = b'*'

class Value:
    def __init__(self):
        self.typ = ""
        self.str = ""
        self.num = 0
        self.bulk = ""
        self.array = []

    def __str__(self):
        if self.typ == "string":
            return f"String: {self.str}"
        elif self.typ == "integer":
            return f"Integer: {self.num}"
        elif self.typ == "bulk":
            return f"Bulk: {self.bulk}"
        elif self.typ == "array":
            return f"Array: {[str(item) for item in self.array]}"
        else:
            return "Unknown type"

class Resp:
    def __init__(self, conn):
        self.conn = conn

    def read_line(self):
        line = b""
        while True:
            b = self.conn.recv(1)
            if not b:
                break
            line += b
            if len(line) >= 2 and line[-2:] == b'\r\n':
                break
        return line[:-2], len(line), None

    def read_integer(self):
        line, n, err = self.read_line()
        if err:
            return 0, n, err
        try:
            num = int(line)
            return num, n, None
        except ValueError as e:
            return 0, n, e

    def read(self):
        _type = self.conn.recv(1)

        if not _type:
            return Value(), None

        if _type == STRING:
            value = Value()
            value.typ = "string"
            line, _, err = self.read_line()
            if err:
                return value, err
            value.str = line.decode()
            return value, None

        elif _type == INTEGER:
            value = Value()
            value.typ = "integer"
            num, _, err = self.read_integer()
            if err:
                return value, err
            value.num = num
            return value, None

        elif _type == BULK:
            return self.read_bulk()

        elif _type == ARRAY:
            return self.read_array()

        else:
            return Value(), f"Unknown type: {_type.decode()}"

    def read_array(self):
        v = Value()
        v.typ = "array"

        # read length of array
        length, _, err = self.read_integer()
        if err:
            return v, err

        v.array = []
        for _ in range(length):
            val, err = self.read()
            if err:
                return v, err
            v.array.append(val)

        return v, None

    def read_bulk(self):
        v = Value()
        v.typ = "bulk"

        length, _, err = self.read_integer()
        if err:
            return v, err

        bulk = self.conn.recv(length)
        v.bulk = bulk.decode()

        # Read the trailing CRLF
        self.read_line()

        return v, None
    
    def write_line(self, line):
        self.conn.sendall(line + b'\r\n')

    def write_integer(self, num):
        self.conn.sendall(INTEGER + str(num).encode() + b'\r\n')

    def write_bulk(self, bulk_str):
        bulk = bulk_str.encode()
        self.conn.sendall(BULK + str(len(bulk)).encode() + b'\r\n' + bulk + b'\r\n')

    def write_error(self, err_msg):
        self.conn.sendall(ERROR + err_msg.encode() + b'\r\n')

    def write_status(self, status_str):
        self.conn.sendall(STRING + status_str.encode() + b'\r\n')

    def write_array(self, array):
        self.conn.sendall(ARRAY + str(len(array)).encode() + b'\r\n')
        for item in array:
            if isinstance(item, str):
                self.write_bulk(item)
            elif isinstance(item, int):
                self.write_integer(item)
