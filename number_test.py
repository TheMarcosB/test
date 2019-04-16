from lib import Number, Array, Error

jump = ('-' * 50) + '\n//'

print(jump, Number.inch('100 px', 'pt'))
print(jump, Number.inch('100'))
print(jump, Number.inch(50))
ic = Number.inchcalc('10% + 100px + 100h', 'px')
print(jump, ic, ic({'%': 500, 'h': 30}))
print(jump, Number.inch('480.0', 'pt')['px'])
print(jump, Number.byte(619606564)['kb'], 619606.564)
percent = Number.percent('30%')
print(jump, percent, percent(1000))
