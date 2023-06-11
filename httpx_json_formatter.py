#!/usr/bin/python3
import sys
import fileinput

if len(sys.argv) != 2:
    print(f"usage: python3 {sys.argv[0]} file_name")
    sys.exit(1)

lines = []
for line in fileinput.input(sys.argv[1]):
    lines.append(line.strip())


out = "{\"findings\":[" + ",".join(lines) + "]}"
print(out)

#just a small script to turn httpx output into a propper json file
#with the root key object called "findings"