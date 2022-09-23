- More pytests
    - [ ] examples in README
    - [ ] exceptions raised when key does/does not exist for put get delete...
- [x] Exact implementation of `len`
- [x] Implement `__iter__`
- [ ] Add generic type hinting when you allow non string keys, it actually kinda makes sense because
tables key type cant change (unless I generate tables behind the scenes but that should be implemented if
at all after generics). See https://docs.python.org/3.8/library/typing.html#typing.MutableMapping
- [ ] The >1MB table scan (I don't need this soon but for larger timeline queries it might come
in handy)
