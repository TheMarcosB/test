from lib import Interpreter
s='''
<?\\/py
#
<?py
class marcos {
    # test
    abcd = 123

?>
''
\\
}
123
<?py
}
import os.path
import re as test40
a='abcd'
b=123
zz=500
d=''
c='azs'
marcos='${b} ${a} ${c}'

ttt="<?py abc ?>"
?>
abc
<?py
def test():
    return 123

for i in range(5){
    a=123
    if 123:
        abc=123
        test='}'

haha= {
 'a':  123,
 'b': 'abc',
 'c': {
   'a': 123,
   'b': 123
 }
}
?>
carros ${marcos}
<?py if 123 { ?>
tes4
<?py abc } ?>
d444
<?py if 123 { ?>
<?py } } imported('/mnt/Arquivos/Projetos/python/marcos/include2.py') ?>
abc
file: ${__file__}
dir: ${__dir__}
os: ${os.path}
imp: $(os.path.isdir '/mnt')
re: ${test40}
cwd: $(os.getcwd)
str: $(eval '${zz} * 2')
'''

if 1:
    print(Interpreter.compiler(string=s).string)

else:
    print(Interpreter.new(s).script)
