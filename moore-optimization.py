#!/usr/bin/env python
# -*- coding: utf-8 -*-
class C:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    @classmethod
    def bold(cls, s):
        return f'{cls.BOLD}{s}{cls.ENDC}'

from terminaltables import AsciiTable


def make_correlation_table(ct, st):
    table_to_print = [[]]
    for y in ct:

        row = [C.bold(y)]
        for x in ct[y]:
            value = ct[y][x]
            if value is None:
                row.append('X')
            else:
                row.append(str(value))
        table_to_print.append(row)
    table_to_print.append([' '] + list(map(C.bold, st[:-1:])))

    return AsciiTable(table_to_print).table


outputs = input('wyjścia: ').split(' ')
states = list(map(int, input('stany: ').split(' ')))
print(outputs)
print(AsciiTable([['stan'] + outputs + ['wyjscie']]).table)

table_of_transitions = {}

for state in states:
    values = list(map(int, input(f'{state}> ').split(' ')))
    output = values.pop()
    row = {
        'transitions': values,
        'output': output
    }
    table_of_transitions[state] = row

table_of_correlation = {}
print('\n\n')
for y in states:
    for x in states:
        if x < y:
            if y not in table_of_correlation:
                table_of_correlation[y] = {}
            if table_of_transitions[x]['output'] != table_of_transitions[y]['output']:
                table_of_correlation[y][x] = None
            else:
                table_of_correlation[y][x] = []
                for i in range(len(table_of_transitions[x]['transitions'])):
                    xv = table_of_transitions[x]['transitions'][i]
                    yv = table_of_transitions[y]['transitions'][i]
                    if xv != yv:
                        table_of_correlation[y][x].append({xv, yv})

print(make_correlation_table(table_of_correlation, states))

somethingChanged = True
while somethingChanged:
    somethingChanged = False
    for y in table_of_correlation:
        for x in table_of_correlation[y]:
            ct_value = table_of_correlation[y][x]
            if ct_value is not None:
                for transition_set in ct_value:
                    sx, sy = sorted(list(transition_set))
                    if table_of_correlation[sy][sx] is None:
                        table_of_correlation[y][x] = None
                        somethingChanged = True
                        continue


print(make_correlation_table(table_of_correlation, states))

