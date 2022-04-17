from ctypes import (
    CDLL,
    POINTER,
    Structure,
    c_char_p,
    c_int,
)
from ctypes.wintypes import POINT
from pathlib import Path
from math import sqrt
from time import monotonic
from typing import List
from logging import getLogger,basicConfig
from functools import wraps

basicConfig(level="INFO",format="[%(asctime)s]: %(message)s")

class OurStruct(Structure):
    _fields_ = [("number", c_int), ("string", c_char_p)]


OurStructPtrType = POINTER(OurStruct)


BASE_DIR = Path(Path(__file__).parent)
our_clib = CDLL(Path(BASE_DIR, "our_clib.so"))
our_clib.OurStruct_new.restype = POINTER(OurStruct)
our_clib.OurStruct_display.restype = None
our_clib.OurStruct_destroy.restype = None
our_clib.getFirstNPrimes.restype = POINTER(c_int)

def print_when_called(func):

    @wraps(func)
    def wrapped(*args,**kwargs):
        getLogger().info(f"Calling {func.__name__}")
        return func(*args,**kwargs)

    return wrapped

    

def is_prime_py(num:int)->bool:
    if num==1:
        return False
    if num==2:
        return True
    if num%2==0:
        return False
    for i in range(3,int(sqrt(float(num)))+1):
        if num%i==0:
            return False
    return True

def get_first_n_primes(n:int)->List[int]:
    primes = [0]*n
    primes_computed = 0
    int_to_check = 2
    while primes_computed<n:
        if is_prime_py(int_to_check):
            primes[primes_computed]=int_to_check
            primes_computed+=1
        int_to_check+=1
    return primes
        
@print_when_called
def test_py_primes_vs_c_primes():
    num_primes_to_compute = 350_000
    getLogger().info(f"Computing the first {num_primes_to_compute:,} primes in both c and python. This can take a minute...")
    # first_10k_primes = [int(num) for num in Path(BASE_DIR,'first10kPrimes.txt').read_text().splitlines()]
    before_py = monotonic()
    primes_from_python = get_first_n_primes(num_primes_to_compute)
    after_py = monotonic()

    before_c = monotonic()
    primes_from_c_ptr = our_clib.getFirstNPrimes(num_primes_to_compute)
    after_c = monotonic()
    # index access to a c-type pointer is similar to pointer arithmetic
    primes_from_c = [primes_from_c_ptr[i] for i in range(num_primes_to_compute)]

    # assert primes_from_python==first_10k_primes
    # assert primes_from_c==first_10k_primes

    py_time = after_py-before_py
    c_time = after_c-before_c
    c_speedup_factor = round(py_time/c_time,2)
    
    getLogger().info(f"It took python {round(py_time)} seconds and c {round(c_time)} seconds to complete the computation. Using c gives you a {c_speedup_factor}x speedup.")

@print_when_called
def test_primitive_function(*, int_arg: int, string_arg: str):
    """In this test, we pass an int on the stack and a python-allocated char pointer.
    Python will take care of freeing the allocated memory for the char pointer.
    """
    our_clib.primitive_function(c_int(int_arg), c_char_p(string_arg.encode()))

@print_when_called
def test_pointer_all_c_side():
    """In this test, the struct is constructed, displayed, and freed on the c-side"""
    our_struct_ptr = our_clib.OurStruct_new()
    our_clib.OurStruct_display(our_struct_ptr)
    our_clib.OurStruct_destroy(our_struct_ptr)

@print_when_called
def test_mixed_pointers(*, int_arg: int, string_arg: str):
    """In this test, the struct is constructed in the python side and send to the c-side for display.
    Python will take care of freeing the allocated memory.
    """
    string_ptr = c_char_p(string_arg.encode())
    # we don't need to wrap int_arg with c_int as cpython does the conversion internally, see https://docs.python.org/3/library/ctypes.html#calling-functions
    # however, we wrap it here anyway for clarity and consistency
    our_struct = OurStruct(c_int(int_arg), string_ptr)
    our_struct_ptr = OurStructPtrType(our_struct)
    our_clib.OurStruct_display(our_struct_ptr)

@print_when_called
def test_mixed_pointers_2(*, int_arg: int, string_arg: str):
    """In this test,
    the struct is constructed in the c-side,
    struct values are allocated and set on the python side,
    the struct is sent to the c-side for display,
    the struct is deallocated on the c-side,
    Python will take care of freeing the allocated memory for the struct values.
    """
    string_ptr = c_char_p(string_arg.encode())

    our_struct = our_clib.OurStruct_new()
    our_struct.contents.string = string_ptr
    our_struct.contents.number = int_arg

    our_clib.OurStruct_display(our_struct)
    our_clib.OurStruct_destroy(our_struct)

def main():
    test_primitive_function(int_arg=1111, string_arg="Be")
    test_pointer_all_c_side()
    test_mixed_pointers(int_arg=3333, string_arg="Not")
    test_mixed_pointers_2(int_arg=4444, string_arg="Judgmental")
    test_py_primes_vs_c_primes()

if __name__=='__main__':
    main()