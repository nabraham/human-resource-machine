SET 6 1        //register containing 1
INBOX #start
COPYTO 1       //goal
COPYFROM 6     //one
COPYTO 2       //F1
COPYTO 3       //F2
OUTBOX
COPYFROM 3     //F2
OUTBOX
COPYFROM 3     //F2
JUMP calc
COPYFROM 3 #inc
COPYTO 2
COPYFROM 4
COPYTO 3
OUTBOX
COPYFROM 3     //F2
ADD 2 #calc
COPYTO 4 //new F2
SUB 1
JUMPN inc
JUMP start
