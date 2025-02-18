#!/usr/bin/env python
from start_consuming_target import start_consuming_target


if __name__=='__main__':
    start_consuming_target(binding_keys=['*.*.rabbit', 'lazy.#'])