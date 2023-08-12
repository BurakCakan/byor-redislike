class RedisProtocol:

    @staticmethod
    def encode_string(data):
        return f"+{data}\r\n"
    
    @staticmethod
    def encode_error(data):
        return f"-{data}\r\n"
    
    @staticmethod
    def encode_integer(data):
        return f":{data}\r\n"
    
    @staticmethod
    def encode_bulk_string(data):
        if data is None:
            return "$-1\r\n"
        return f"${len(data)}\r\n{data}\r\n"
    
    @staticmethod
    def encode_array(data):
        if data is None:
            return "*-1\r\n"
        encoded_items = ''.join([RedisProtocol.encode(item) for item in data])
        return f"*{len(data)}\r\n{encoded_items}"
    
    @staticmethod
    def encode(data):

        if isinstance(data, str):
            return RedisProtocol.encode_string(data)
        elif isinstance(data, int):
            return RedisProtocol.encode_integer(data)
        elif isinstance(data, bytes):
            return RedisProtocol.encode_bulk_string(data.decode())
        elif isinstance(data, list):
            return RedisProtocol.encode_array(data)
        elif data is None:
            return RedisProtocol.encode_bulk_string(None)
        else:
            return RedisProtocol.encode_error("Invalid data")
    
    @staticmethod
    def decode(data):
        if data.startswith("+"):
            return data[1:].strip()
        elif data.startswith(":"):
            return int(data[1:].strip())
        elif data.startswith("-"):
            return data[1:].strip()
        else:
            return None

if __name__ == "__main__":
    print("hello")