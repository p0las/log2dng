#
class FieldTypeMeta(type):
    def __repr__(cls):
        return f"{cls.__name__} - code: {cls.short_code}, size: {cls.size}"


class FieldType(metaclass=FieldTypeMeta):
    short_code = ''
    dng_code = -1
    size = 1


class Byte(FieldType):
    short_code = 'B'
    dng_code = 1
    size = 1

class Ascii(FieldType):
    short_code = 's'
    dng_code = 2
    size = 1

class Short(FieldType):
    short_code = 'H'
    dng_code = 3
    size = 2

class Long(FieldType):
    short_code = 'I'
    dng_code = 4
    size = 4

class Rational(FieldType):
    short_code = 'II'
    dng_code = 5
    size = 8

class SByte(FieldType):
    short_code = 'b'
    dng_code = 6
    size = 1

class Undefined(FieldType):
    short_code = 'B'
    dng_code = 7
    size = 1

class SShort(FieldType):
    short_code = 'h'
    dng_code = 8
    size = 2

class SLong(FieldType):
    short_code = 'i'
    dng_code = 9
    size = 4

class SRational(FieldType):
    short_code = 'ii'
    dng_code = 10
    size = 8

class Float(FieldType):
    short_code = 'f'
    dng_code = 11
    size = 4

class Double(FieldType):
    short_code = 'd'
    dng_code = 12
    size = 8

class HalfFloat(FieldType):
    short_code = 'e'
    dng_code = -1 #unknown
    size = 2

