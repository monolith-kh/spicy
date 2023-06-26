# automatically generated by the FlatBuffers compiler, do not modify

# namespace: fbs

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class Response(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Response()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsResponse(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # Response
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Response
    def RequestedCommand(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int8Flags, o + self._tab.Pos)
        return 0

    # Response
    def ErrorCode(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # Response
    def Detail(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

def ResponseStart(builder):
    builder.StartObject(3)

def Start(builder):
    ResponseStart(builder)

def ResponseAddRequestedCommand(builder, requestedCommand):
    builder.PrependInt8Slot(0, requestedCommand, 0)

def AddRequestedCommand(builder, requestedCommand):
    ResponseAddRequestedCommand(builder, requestedCommand)

def ResponseAddErrorCode(builder, errorCode):
    builder.PrependInt32Slot(1, errorCode, 0)

def AddErrorCode(builder, errorCode):
    ResponseAddErrorCode(builder, errorCode)

def ResponseAddDetail(builder, detail):
    builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(detail), 0)

def AddDetail(builder, detail):
    ResponseAddDetail(builder, detail)

def ResponseEnd(builder):
    return builder.EndObject()

def End(builder):
    return ResponseEnd(builder)
