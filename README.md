# What is this?
A working example of communication between `cpython` and `c` via the `ctypes` module.

# How can I run this?
Make sure you have docker install and then run:

`docker run  $(docker build -q .)`

The output will display `python` and `c` interacting via `ctypes`:

```
c-side primitive_function received args: [intArg={1111},strArg={Don't}]
OurStruct([number={0},string={(null)}])
OurStruct([number={3333},string={Be}])
OurStruct([number={4444},string={Happy!}])
```