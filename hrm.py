import json
import re
import sys

OK = (1,'ok')

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
        return (0,'DONE')
    cpu.read()
    cpu.increment()
    return OK

def copyto(cpu, r):
    cpu.register[r] = cpu.val
    cpu.increment()
    return OK

def copyfrom(cpu, r):
    if r in cpu.register:
        cpu.val = cpu.register[r]
        cpu.increment()
        return OK
    return (-1, 'Register %s not set' % r)

def outbox(cpu):
    if cpu.val == None:
        return (-2, 'No current value for outbox')
    print(cpu.val)
    cpu.val = None
    cpu.increment()
    return OK

def jump(cpu, c):
    if c in cpu.labels:
        cpu.cur = int(cpu.labels[c])
    else:
        cpu.cur = int(c)
    return OK

def jumpn(cpu, c):
    if cpu.val < 0:
        jump(cpu, c)
    else:
        cpu.increment()
    return OK

def add(cpu, r):
    cpu.val += cpu.register[r]
    cpu.increment()
    return OK

def sub(cpu, r):
    cpu.val -= cpu.register[r]
    cpu.increment()
    return OK

def set(cpu, r, v):
    cpu.register[r] = int(v)
    cpu.increment()
    return OK

def bump_p(cpu, r):
    return bump(cpu, r, lambda x: x+1)

def bump_n(cpu, r):
    return bump(cpu, r, lambda x: x-1)

def bump(cpu,r,op):
    if r in cpu.register:
        cpu.register[r] = op(cpu.register[r])
        cpu.val = cpu.register[r]
        return OK
    else:
        return (-1,'Register %s not set' % r)

instructions = {
    'ADD': add,
    'BUMPN': bump_n,
    'BUMPP': bump_p,
    'COPYFROM': copyfrom,
    'COPYTO': copyto,
    'INBOX': inbox,
    'JUMP': jump,
    'JUMPN': jumpn,
    'OUTBOX': outbox,
    'SET': set,
    'SUB': sub
}

def print_state(line,cmd,cpu,status):
    print('[%d] - %s\n%s\n%s' % (line,status,cpu,cmd))

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

    status = OK
    stacktrace = []
    while status[0] > 0:
        cmd = commands[cpu.cur]
        stacktrace.append([cmd, str(cpu), str(status)])
        status = instructions[cmd[0]](cpu, *cmd[1:])

    if status[0] < 0 or debug:
        for i,s in enumerate(stacktrace):
            print_state(i+1,*s)
        print_state(len(stacktrace)+1,cmd,cpu,status)

if __name__ == '__main__':
    if (sys.argv[-1] == '-d'):
        main(sys.argv[1], list(map(int, sys.argv[2:][:-1][::-1])), True)
    else:
        main(sys.argv[1], list(map(int, sys.argv[2:][::-1])))
