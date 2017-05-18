## About

A test bed for the game _Human Resource Machine_.

## Deviations from the game
### Comments
All input after and including '//' is ignored on each line.  Whitespace is trimmed after dropping comments.

### Labels
For readability, I have introduced labels for jump commands.  Labels as arguments cause jump commands to jump to the line containing the label.  Labels are marked with \#.  The following program:
```asm
1 INBOX     //read the inbox
2 OUTBOX    //write to the outbox
3 JUMP 1    //repeat
```
is the same as:
```asm
1 INBOX #start
2 OUTBOX
3 JUMP start
```
## Usage
```bash
python hrm.py <program file> <inputs> (-d option [show stack trace])
```
## Examples
```bash
python hrm.py programs/fib.asm 100 15
```
```bash
python hrm.py programs/fib.asm 4 -d
```
