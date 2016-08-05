# TovTovTov
Because life is short, and another reason, and because I like [Chicken](http://torso.me/chicken) (TovTovTov is a bit stronger, though).

## The Compiler
Real compilers can't be bothered with nonsense, so only two substrings in the input really mean anything: `TOV` and `SEP`.
Here is a Python implementation of the compiler, that outputs a list of integers (=the initial stack contents, see below).
```python
def compile(program):
    return [len(line.split(TOV))-1 for line in program.split(self.SEP)]
```
An example program:
```
tov
tov tov tov
tov
```
The latter used the default values `'tov'` and `'\n'` of `TOV` and `SEP`, but that's configurable, of course,
so the same program could be written as:
```
well
well well well
well
```
Or if `TOV='1'` and `SEP='0'`:
```
1011101
```
And equivalently: (as the impatient compiler ignores stuff he doesn't understand)
```
I used to have ten bottles of beer on my wall, 10 bottles of beer.
I took 1 down, I passed it around, but no one drank that 1 beer,
so I returned it to the wall. I still have 10 bottles there.
Maybe I'll drink that 1 beer myself later.
```
You get the idea.

## The World
A seemingly harmless `PC` was once `0`, but now increases (by `1`) every step it takes,
interpreting *a single stack*, that supports multiculturalism of numbers and strings living together,
so codes and values are interchangeable. Everything can theoretically change during runtime, but more often
than not this design will lead to horrible crashes if we're not careful.

Stack is initialized with list of integers (compiled program). `PC=0`, `sop=0` (=default: interpreting `stack[PC]` as normal ops)

## The Commands
Number of `TOV`s | Manifestation in our astral existence
--- | ---
0 | Nothing # NOP
1,2 | push(TOV), push(SEP) # PUSH_TOV, PUSH_SEP (strings; TOV interpreted as operation means QUIT the program!)
6 | push(new user input) # PUSH_INPUT, interactive!
18 | push(len(stack)) # PUSH_LEN
9 | i=pop; push(i); push(i) # COPY_LAST
10 | pop # POP
19 | push(stack[pop]) # PUSH_FROM_POP, copy a value from a specific location in the stack and push it into stack
3 | print str(pop) # PRINT
4,5 | special treatment to next op # SOP_CHR, SOP_NUM
7 | PC += pop if pop # inc PC by some number (= top pop value), if value popped immediately after is true # INCPC
8 | PC = pop if pop # jump PC to some index (= top pop value), if value popped immediately after is true # JUMP
12,13 | push(int(pop)), push(ascii[pop]) # INT, CHR
11 | push(pop == pop ? 1 : 0) # PUSH_CMP
14,15,16 | push(pop OP pop) for OP=+,-,* # ADD, SUB, MULT
17 | stack[PC+1:PC+1] = stack[PC+1:PC+pop] * pop # duplicate next ops and insert in current PC location # DUP_OPS
20 | i=pop; set stack[i:i] to be: pop # top stack pop = where to insert, second pop = value to insert # INSERT_AT
21+n | pushes number *n* to stack (can use SOP_NUM instead)
