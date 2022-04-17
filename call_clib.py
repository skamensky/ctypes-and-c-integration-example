from ctypes import (
    CDLL,
    POINTER,
    Structure,
    c_char_p,
    c_int,
)
from pathlib import Path


class OurStruct(Structure):
    _fields_ = [("number", c_int), ("string", c_char_p)]


OurStructPtrType = POINTER(OurStruct)

our_clib = CDLL(Path(Path(__file__).parent, "our_clib.so"))
our_clib.OurStruct_new.restype = POINTER(OurStruct)
our_clib.OurStruct_display.restype = None
our_clib.OurStruct_destroy.restype = None


def test_primitive_function(*, int_arg: int, string_arg: str):
    """In this test, we pass an int on the stack and a python-allocated char pointer.
    Python will take care of freeing the allocated memory for the char pointer.
    """
    our_clib.primitive_function(c_int(int_arg), c_char_p(string_arg.encode()))


def test_pointer_all_c_side():
    """In this test, the struct is constructed, displayed, and freed on the c-side"""
    our_struct_ptr = our_clib.OurStruct_new()
    our_clib.OurStruct_display(our_struct_ptr)
    our_clib.OurStruct_destroy(our_struct_ptr)


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


test_primitive_function(int_arg=1111, string_arg="Don't")
test_pointer_all_c_side()
test_mixed_pointers(int_arg=3333, string_arg="Be")
test_mixed_pointers_2(int_arg=4444, string_arg="Happy!")
