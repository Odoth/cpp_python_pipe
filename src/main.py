import os
import time
import struct


_r_fd = int(os.getenv("PY_READ_FD"))
_w_fd = int(os.getenv("PY_WRITE_FD"))


_r_pipe = os.fdopen(_r_fd, 'rb', 0)
_w_pipe = os.fdopen(_w_fd, 'wb', 0)


def _read_n(f, n):
    buf = ''
    while n > 0:
        data = f.read(n)
        if data == '':
            raise RuntimeError('unexpected EOF')
        buf += data
        n -= len(data)
    return buf


def _api_get(apiName, apiArg):
    # Python sends format
    # [apiNameSize][apiName][apiArgSize][apiArg]
    # on the pipe
    msg_size = struct.pack('<I', len(apiName))
    _w_pipe.write(msg_size)
    _w_pipe.write(apiName)

    apiArg = str(apiArg)  # Just in case
    msg_size = struct.pack('<I', len(apiArg))
    _w_pipe.write(msg_size)
    _w_pipe.write(apiArg)

    # Response comes as [resultSize][resultString]
    buf = _read_n(_r_pipe, 4)
    msg_size = struct.unpack('<I', buf)[0]

    data = _read_n(_r_pipe, msg_size)

    if data == "__BAD API__":
        raise Exception(data)

    return data


# APIs to C++
def foo(arg):
    return _api_get("foo", arg)


def bar(arg):
    return _api_get("bar", arg)


# this one doesn't actually exist
def boo(arg):
    return _api_get("boo", arg)


def main():
    print 'Script Starting'
    for i in xrange(10):
        res = foo(100 - i)
        print i, " foo: ", res
        res = bar("something " + str(i))
        print i, " bar: ", res
        time.sleep(1)

        # if i == 5:
        #     res = boo(i)


if __name__ == "__main__":
    main()
