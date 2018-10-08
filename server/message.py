import struct


class MessageError(Exception):
    pass


class Message:
    def __init__(self, data=None, message_type=None, message=None):
        if data:
            self.data = data
            if len(self.data) < 4:
                raise MessageError('The message is too short')

            self.message_type = struct.unpack('!H', self.data[:2])[0]
        elif message_type and message:
            self.message_type = message_type
            serialized_message = message.SerializeToString()
            if len(serialized_message) > 2**16 - 1:
                raise MessageError('The message is too long')

            self.data = struct.pack('!H', self.message_type)
            self.data += struct.pack('!H', len(serialized_message))
            self.data += serialized_message
        else:
            raise MessageError('Invalid parameters passed to __init__')

    def __repr__(self):
        return f'<Message type={self.message_type} data={self.data}>'

    @property
    def serialized_message(self):
        return self.data[4:]
