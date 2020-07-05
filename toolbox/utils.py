import time
from typing import Callable


def wait_print_until_complete(condition_callback: Callable[[], bool]):
    dot_ct = 1
    while condition_callback():
        print(f"{''.join(['.'] * dot_ct)}\r", end="")
        time.sleep(0.2)
        dot_ct += 1
