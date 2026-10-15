# Executed by the pinned Unix minimal port; no device I/O.
import sys
assert sys.implementation.name == "micropython"
assert [i * i for i in range(4)] == [0, 1, 4, 9]
print("micropython fixture: pass")
