from lib import Array, Blocker, Class

start = ('-' * 50) + '\n//'
end = '\n' + ('-' * 50)
jump = '\n'

array = Array.new({5:3, 'a':'1', 'b':'2', 'c':'3'})
array[3.0] = 123
update = {
  'array': Array.new({'d':'10', 'e':'20', 'f':'30'}),
  'dict' : {0: '10', 1: '20', 2: '30'},
  'tuple': ('10', '20', '30')
}

# array items
print(start, 'array-> items:', array, end)
print('items :', Array.items(array))
print('keys  :', Array.keys(array))
print('values:', Array.values(array))

# array check
print(start, 'array-> check:', array, end)
print('key index  : YES[a]->', Array.inkey(array, 'a'), '   | NOT[f]->', Array.inkey(array, 'f'))
print('value index: YES[2]->', Array.inval(array, '2'), '   | NOT[5]->', Array.inval(array, '5'))
print('is key     : YES[b]->', Array.iskey(array, 'b'), '| NOT[d]->', Array.iskey(array, 'd'))
print('is value   : YES[3]->', Array.isval(array, '3'), '| NOT[7]->', Array.isval(array, '7'))

# array update
print(start, 'array-> update:', array, end)
updated = Array.copy(array)
Array.update(updated, update['array'])
print('merge-> array:', updated)
updated = Array.copy(array)
Array.update(updated, update['dict'])
print('merge-> dict :', updated)
updated = Array.copy(array)
Array.update(updated, update['tuple'])
print('merge-> tuple:', updated, jump)

# array key to value
print(start, 'array-> current:', array, end)
Array.key2val(array)
print('value-> key:', array, jump)

# array key to value
print(start, 'array-> current:', array, end)
Array.reverse(array)
print('array-> reverse:', array)

# array sorted
sort = Array(['d', 'f', 'b', ['zz', 'yz', 'wz'], 'g', 'a', {'a': 1, 'b':2}])
print(start, 'array-> sorted:', sort, end)
Array.sort(sort)
print(sort)

print(start, 'array-> string:', sort, end)
print(Array.string(sort))

print(start, 'array-> query:', sort, end)
print(Array.tostring(sort))
print(Array.key2val({1:'a', 2:'b'}))
