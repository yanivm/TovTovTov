from sys import stdout as so


class TovTovTov(object):
    """See README"""
    VERSION = '1.0.0'
    OP_NAMES = {0: 'NOP',
                1: 'PUSH_TOV', 2: 'PUSH_SEP', 6: 'PUSH_INPUT', 18: 'PUSH_LEN', 9: 'COPY_LAST', 10: 'POP',
                19: 'PUSH_FROM_POP',
                3: 'PRINT',
                4: 'SOP_CHR', 5: 'SOP_NUM',
                7: 'INCPC', 8: 'JUMP',
                12: 'INT', 13: 'CHR',
                11: 'PUSH_CMP',
                14: 'ADD', 15: 'SUB', 16: 'MULT',
                17: 'DUP_OPS',
                20: 'INSERT_AT'}
    HUMAN_NAMES = {'CMP': 'PUSH_CMP', 'INP': 'PUSH_INPUT', 'INPUT': 'PUSH_INPUT', 'OUTPUT': 'PRINT'}
    HUMAN_NAMES.update({v: v for v in OP_NAMES.itervalues()})
    OP_NAMES_INV = {v: k for k, v in OP_NAMES.iteritems()}

    def __init__(self, TOV="tov", SEP="\n"):
        self.TOV = TOV
        self.SEP = SEP
        TovTovTov.OP_NAMES[TOV] = 'QUIT'

    def decompile(self, ints_arr, join=' '):
        return self.SEP.join([join.join([self.TOV] * x) for x in ints_arr])

    def compile(self, program):
        return [len(line.split(self.TOV)) - 1 for line in program.split(self.SEP)]

    def compile_highlevel(self, highlevel_strings_arr, comment_prefix='#'):
        return [self.OP_NAMES_INV[s] for s in highlevel_strings_arr if not s.startswith(comment_prefix)]

    def run(self, program, debug=False):
        self.run_ints_arr(self.compile(program), debug)

    def is_true(self, v):
        return v != 0 if type(v) == int else v == self.TOV

    def run_ints_arr_v1(self, s, debug=False):
        pc = -1
        while 1:
            pc += 1
            op = s[pc]
            if debug: print "DEBUG s: %s\tpc: %d, op: %s (%s)" % (str(s), pc, op, self.OP_NAMES.get(op, 'number'))
            if op in self.OP_NAMES:
                if op == self.TOV: break
                if op == 0: continue
                if op == 1: s.append(self.TOV); continue
                if op == 2: s.append(self.SEP); continue
                if op == 3: s.append(s.pop() + s.pop()); continue
                if op == 4: s.append(s.pop() - s.pop()); continue
                if op == 5: s.append(s.pop() * s.pop()); continue
                if op == 6: s.append(1 if s.pop() == s.pop() else 0); continue
                if op == 7: s.append(raw_input(">>")); continue
                if op == 8: s.append(s[s.pop()]); continue
                if op == 9: i = s.pop(); s[i:i] = [s.pop()]; continue
                if op == 10: i = s.pop(); pc = i - 1 if self.is_true(s.pop()) else pc; continue  # JUMP_COND
                if op == 11: s.append(chr(s.pop())); continue
                if op == 12: s.append(int(s.pop())); continue
                if op == 13: so.write(s.pop()); so.flush(); continue
                if op == 14: i = s.pop(); s[pc + 1: pc + 1 + i] = s[pc + 1: pc + 1 + i] * s.pop(); continue
                if op == 15: s.append(len(s)); continue;
            else:
                s.append(op - 16)

    def run_ints_arr(self, s, debug=False):
        pc = -1
        sop = 0  # If !=0, then special handling of op
        while 1:
            pc += 1
            op = s[pc]
            if debug: print "DEBUG s: %s\t(%s)" % (
                '[' + ', '.join([x + ('"' if type(e) == str else '') + str(e) for x, e in
                                 zip([''] * pc + [chr(35 + sop)] + [''] * len(s), s)]) + ']',
                self.OP_NAMES.get(op, 'number'))
            # Possibly interpret this op in a special manner
            if sop == 1: sop = 0; s.append(chr(op)); continue
            if sop == 2: sop = 0; s.append(op); continue
            # Otherwise, normal treatment
            if op in self.OP_NAMES:  # Could instead simply condition on op<21 (but then get if op==self.TOV outside!)
                # QUIT, NOP
                if op == self.TOV: break  # QUIT!
                if op == 0: continue  # NOP
                # Push special stuff
                if op == 1: s.append(self.TOV); continue  # PUSH_TOV
                if op == 2: s.append(self.SEP); continue  # PUSH_SEP
                if op == 6: s.append(raw_input(">> ")); continue  # PUSH_INPUT
                if op == 18: s.append(len(s)); continue;  # PUSH_LEN
                if op == 9: i = s.pop(); s.append(i); s.append(i); continue  # COPY_LAST
                if op == 10: s.pop(); continue  # POP
                if op == 19: s.append(s[s.pop()]); continue  # PUSH_FROM_POP
                # Output
                if op == 3: so.write(str(s.pop())); so.flush(); continue  # PRINT
                # Special interpretation to next op
                if op == 4: sop = 1; continue  # SOP_CHR
                if op == 5: sop = 2; continue  # SOP_NUM
                # Conditionally update PC
                if op == 7: i = s.pop(); pc = pc + i if self.is_true(s.pop()) else pc; continue  # INCPC, relative
                if op == 8: i = s.pop(); pc = i - 1 if self.is_true(s.pop()) else pc; continue  # JUMP, absolute
                # Modify last (str <-> int)
                if op == 12: s.append(int(s.pop())); continue  # INT
                if op == 13: s.append(chr(s.pop())); continue  # CHR
                # Compare
                if op == 11: s.append(1 if s.pop() == s.pop() else 0); continue  # PUSH_CMP
                # Arithmetic
                if op == 14: s.append(s.pop() + s.pop()); continue  # ADD
                if op == 15: s.append(s.pop() - s.pop()); continue  # SUB
                if op == 16: s.append(s.pop() * s.pop()); continue  # MULT
                # Duplicate commands (maybe to be used as unrolled loop)
                if op == 17: i = s.pop(); s[pc + 1: pc + 1 + i] = s[pc + 1: pc + 1 + i] * s.pop(); continue  # DUP_OPS
                # Insert (rare usage)
                if op == 20: i = s.pop(); s[i:i] = [s.pop()]; continue  # INSERT, absolute position
            else:
                s.append(op - 21)
