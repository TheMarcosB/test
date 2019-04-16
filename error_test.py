from lib import Error

Error.new(test=123, abc=123)
Error.new('marcos', test=123, abc=123)
Error.alert(test=123, abc=123)
Error.infor(test=123, abc=123)
e=Error.infor('marcos', 123)
print(e)
