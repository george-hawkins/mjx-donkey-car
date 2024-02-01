# This file contains two main functions:
# 1. `find_max_channel_values` - find the high and low values which when used in combination
#    with a master channel and a mix offset achieve the most distinct values.
# 2. `find_specific_setup` - given a specific set of master and secondary knob positions can
#    a set of high and low values be found which gives each combination a distinct value.


def calc_slave_value(master, mix_offset, hi, lo):
    multiplier = 0

    if master < 0:
        multiplier = lo
    elif master > 0:
        multiplier = hi

    slave = mix_offset + (master * multiplier)
    slave = max(-100, slave)
    slave = min(100, slave)

    return slave


def find_specific_setup():
    # Specify, a sequence of knob combinations that you want and see if a
    # setup where each can be mapped to a distinct value can be found.
    switch_states = [(0, 0), (0, 100), (100, 100), (-100, 100), (0, -100), (100, -100), (-100, -100)]
    reversed_states = [(b, a) for a, b in switch_states]
    step = 25
    for hi_percent in range(100, -101, -step):
        hi = hi_percent / 100
        for lo_percent in range(100, -101, -step):
            lo = lo_percent / 100
            for states in [switch_states, reversed_states]:
                slave_values = set()
                ordering = []
                for master, mix_offset in states:
                    slave = calc_slave_value(master, mix_offset, hi, lo)
                    slave_values.add(slave)
                    ordering.append(slave)
                count = len(slave_values)
                if count == len(switch_states):
                    flip = states == reversed_states
                    # If `flip` is True then you need to flip the relationship
                    # between the master knob and the other knob.
                    print(f"flip: {flip}, hi: {hi}, lo: {lo}, count: {count}, channel values: {ordering}")


def find_max_channel_values():
    max_count = 0
    step = 25  # Gives 7 distinct values.
    # step = 50  # Gives 5 distinct values.
    for hi_percent in range(100, -101, -step):
        hi = hi_percent / 100
        for lo_percent in range(100, -101, -step):
            lo = lo_percent / 100
            slave_values = set()
            ordering = []
            for master in [-100, 0, 100]:
                for mix_offset in [-100, 0, 100]:
                    slave = calc_slave_value(master, mix_offset, hi, lo)
                    slave_values.add(slave)
                    ordering.append(slave)
            count = len(slave_values)
            if count > max_count:
                max_count = count
                print(f"hi: {hi}, lo: {lo}, count: {count}, channel values: {ordering}")


if __name__ == '__main__':
    find_specific_setup()
    # find_max_channel_values()
