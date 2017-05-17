import json
import re
import sys

class cpu_state:
    inputs = []
    register = {}
    val = None
    cur = 0
    labels = {}

    def __init__(self, inputs):
        self.inputs = inputs

    def increment(self):
        self.cur += 1

    def read(self):
        self.val = self.inputs.pop()

    def __repr__(self):
        return json.dumps({
            'inputs': self.inputs,
            'registers': self.register,
            'val': self.val,
            'cur': self.cur,
            'labels': self.labels
        }, sort_keys=True, indent=4);

def inbox(cpu):
    if len(cpu.inputs) == 0:
        exit()
    cpu.read()
    cpu.increment()

def copyto(cpu, r):
    cpu.register[r] = cpu.val
    cpu.increment()

def copyfrom(cpu, r):
    if r in cpu.register:
        cpu.val = cpu.register[r]
        cpu.increment()
    else:
        raise Exception('Register %s not set' % r)

def outbox(cpu):
    print(cpu.val)
    cpu.increment()

def jump(cpu, c):
    if c in cpu.labels:
        cpu.cur = int(cpu.labels[c])
    else:
        cpu.cur = int(c)

def jumpn(cpu, c):
    if cpu.val < 0:
        jump(cpu, c)
    else:
        cpu.increment()

def add(cpu, r):
    cpu.val += cpu.register[r]
    cpu.increment()

def sub(cpu, r):
    cpu.val -= cpu.register[r]
    cpu.increment()

def set(cpu, r, v):
    cpu.register[r] = int(v)
    cpu.increment()

instructions = {
    'ADD': add,
    'COPYFROM': copyfrom,
    'COPYTO': copyto,
    'INBOX': inbox,
    'JUMP': jump,
    'JUMPN': jumpn,
    'OUTBOX': outbox,
    'SET': set,
    'SUB': sub
}

def main(filename, inputs, debug=False):
    cpu = cpu_state(inputs)
    commands = []

    with open(filename) as f:
        for i,line in enumerate([x.strip('\n').strip(' ') for x in f.readlines()]):
            matches = re.findall(r"#.*", line)
            for m in matches:
                cpu.labels[m[1:]] = i

            cleaned = re.split(r"[#/]", line)[0]
            args = list(filter(lambda x: len(x) > 0, re.split('\s*', cleaned)))
            commands.append(args)

    while True:
        if debug:
            print(cpu)
        cmd = commands[cpu.cur]
        instructions[cmd[0]](cpu, *cmd[1:])

if __name__ == '__main__':
    main(sys.argv[1], list(map(int, sys.argv[2:][::-1])))
