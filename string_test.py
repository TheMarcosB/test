from lib import Code, String, Array
jump = ('-' * 50) + '\n//'
print(jump, 'split\n', String.split('a=1,b=2,c=3', '%k=%v,'))
print(jump, 'combine\n', String.combine('1234', 'abc'))
print(jump, 'trim\n', String.trim('   1   2   3   45   '))
print(jump, 'swap\n', String.swap('$1,$2', {'$1': 'a', '$2': 'b'}))
print(jump, 'clean\n', String.clean('Atenção = evolução'))
print(jump, 'pad left\n', String.pad('abc', '$', 5, False))
print(jump, 'pad right\n', String.pad('abc', '@', 7, True))
print(jump, 'space\n', String.space('   a   b   c   df   '))
find = '''marcos run ${123} vai ${script} ddd'''
print(jump, 'find string\n', find)
print(jump, 'find\n', Array.show(String.find(find, '(\$\{(.*?)\})')))
split=String.split('form-data; name="fieldName"; filename="filename.jpg"; marcos', '%k=("%v"); ')
print(jump, 'split\n', split)
print(jump, 'split\n', String.join(split, '%k=("%v"); '))
print(jump, 'query\n', String.query('%k=("\(%v)+(%v\)*); '))
print(jump, 'query\n', String.query('%k=("\(%v+%v\)*); '))
