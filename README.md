# What is this?
A working example of communication between `cpython` and `c` via the `ctypes` module.

# How can I run this?
Make sure you have docker install and then run:

`docker run  $(docker build -q .)`

The output will display `python` and `c` interacting via `ctypes`:

```
[2022-04-17 20:26:54,770]: Calling test_primitive_function
[LogFromC]: c-side primitive_function received args: [intArg={1111},strArg={Be}]
[2022-04-17 20:26:54,771]: Calling test_pointer_all_c_side
[LogFromC]: OurStruct([number={0},string={(null)}])
[2022-04-17 20:26:54,771]: Calling test_mixed_pointers
[LogFromC]: OurStruct([number={3333},string={Not}])
[2022-04-17 20:26:54,771]: Calling test_mixed_pointers_2
[LogFromC]: OurStruct([number={4444},string={Judgmental}])
[2022-04-17 20:26:54,771]: Calling test_py_primes_vs_c_primes
[2022-04-17 20:26:54,771]: Computing the first 350,000 primes in both c and python. This can take a minute...
[2022-04-17 20:27:28,859]: It took python 30 seconds and c 4 seconds to complete the computation. Using c gives you a 7.66x speedup.
```