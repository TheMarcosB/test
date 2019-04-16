from lib import Class, Main, Array
jump = ('-' * 50) + '\n//'
print(jump, 'type is array\n', Class.type(Array.new()))
print(jump, 'type is string\n', Class.type('123'))
print(jump, 'type is number\n', Class.type(123))
print(jump, 'type is bytes\n', Class.type(open('/mnt/Arquivos/Projetos/marcos/test.py')))
print(jump, 'type is string\n', Class.type(list()))
