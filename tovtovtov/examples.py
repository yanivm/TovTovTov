from tovtovtov import TovTovTov

t3 = TovTovTov()

ints_arr_hello_world = [17, 13, 3,
                        1, 1, 5, 3, 18, 15, 8,
                        0, 0, 0,  # will never be reached
                        100, 108, 114, 111, 87, 32, 111, 108, 108, 101, 72,
                        11, 2]

ints_arr_arithmetic = [4, 65, 3,  # Output message 'A'
                       6, 12,  # Input first number A
                       4, 66, 3,  # Output message 'B'
                       6, 12,  # Input second number B
                       4, 80, 4, 79, 3, 3,  # Output message 'OP'
                       6,  # Input required operation C (string)
                       9, 4, 43, 11, 5, 16, 7,  # copy, push '+', compare to C, maybe inc PC by 16 to :add below
                       9, 4, 42, 11, 5, 16, 7,  # 7 copy, push '*', compare to C, maybe inc PC by 16 to :mult below
                       1, 3, 1, 1, 5, 3, 18, 15, 8,  # 9 Print TOV and quit
                       10, 14, 3, 1, 5, 3, 7,  # 7 :add pop, add, print result, inc PC by 3 to jump to :done below
                       10, 16, 3,  # :mult pop, multiply, print result (and proceed to :done)
                       1,  # :done
                       0]  # will never be reached

highlevel_print_tov = ['PUSH_TOV', 'PRINT', '# comment', '#another', 'PUSH_TOV']
ints_arr_print_tov = t3.compile_highlevel(highlevel_strings_arr=highlevel_print_tov, comment_prefix='#')

which_program, DEBUG = 1, False

if which_program == 0:
    with open('uncompiled_examples/hello_world.txt', 'r') as f:
        program = f.read()
        ints_arr = TovTovTov().compile(program)
        #ints_arr = TovTovTov(TOV='1', SEP='0').compile(program)
        #print ints_arr
        #TovTovTov().run(program=program, debug=False)
elif which_program == 1:
    ints_arr = ints_arr_hello_world
elif which_program == 2:
    ints_arr = ints_arr_arithmetic
elif which_program == 3:
    ints_arr = ints_arr_print_tov
else:
    raise ValueError("Expected value in [0,3], got instead: %s" % which_program)

# Print the PROGRAM and its OUTPUT
program_str = t3.decompile(ints_arr)  # t3.compile(t3.decompile(ints_arr)) == ints_arr
print "PROGRAM:\n%s\nOUTPUT:" % program_str
t3.run(program_str, debug=DEBUG)
print "(END OF OUTPUT)"

