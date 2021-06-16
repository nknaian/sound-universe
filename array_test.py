import random
import itertools
import numpy as np

def buf_to_num(buf):
    total = 0
    factor = 0
    for item in reversed(buf):
        total += (2**factor) * item
        factor += 8

    return total

def add_bufs(buf, add_buf):
    """Carry addition
    
    Assumes that buffers are represented as big endian.
    Has no protection against full buffer number overflow (wraps around)
    """
    assert len(buf) >= len(add_buf)

    # Iterate from the end of the buffer and end of add buffer. If the add buffer is exhausted,
    # it will be filled with 'None' by zip_longest and we can exit once there's no carry left
    carry = 0
    for buf_index, add_num in itertools.zip_longest(range( len(buf) - 1, -1, -1), reversed(add_buf)):
        # Get starting value for the buffer at this index
        curr_val = buf[buf_index]
        
        # Add to this buffer value
        if add_num:
            buf[buf_index] += add_num
        # If we're out of add nums and there's no carry, then we're done here
        elif add_num is None and carry == 0:
            break

        # Add the carry
        buf[buf_index] += carry

        # If overflow occured, then set the carry bit
        if buf[buf_index] < curr_val:
            carry = 1
        else:
            carry = 0

if __name__ == "__main__":
    # buf = np.array([9, 122, 212, 31], dtype=np.uint8)
    # add_buf = np.array([107, 197], dtype=np.uint8)
    buf = np.zeros(4, dtype=np.uint8)
    add_buf = np.zeros(3, dtype=np.uint8)
    for i in range(len(buf)):
        buf[i] = random.randint(0, 255)
    for i in range(len(add_buf)):
        add_buf[i] = random.randint(0, 255)
    print("original buf: ", buf)
    print("original num: ", buf_to_num(buf))
    print("add buf: ", add_buf)
    print("add num: ", buf_to_num(add_buf))

    # Add the 'add_buf' to the 'buf'
    add_bufs(buf, add_buf)

    print("new buf: ", buf)
    print("new num: ", buf_to_num(buf))
