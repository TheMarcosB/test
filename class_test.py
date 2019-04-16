from lib import Blocker, Class

# open
new = Class.new()
print('check', Blocker.check(new))
new.test = 123

# close
Blocker.new(new, 1, 1)
print('check', Blocker.check(new))

# open
Blocker.enter(new, 1, 1)
print('check', Blocker.check(new))
new.__id__ = 123

# close
Blocker.exit(new, 1, 1)
Blocker.set(new)
print('check', Blocker.check(new))
new.__id__ = 123
