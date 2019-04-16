import tkinter, time
from lib import Image
# open test
i=Image.open('/home/marcos/Imagens/Eu/FILE1128.JPG')
if 1:
    txt=Image.Text('''{Mar"Cos Bento da cunha e amor é falso não adianta 123

{Marcos Bento da cunha e amor é falso não adianta
test hahah''')
    txt.style({
        'padding': 10,
        'text-align': 'center',
        'font-family': 'impact',
        'font-size': 20,
        'word-break': 'normal',
        'text-shadow': (-3, -3, 3, 'red'),
        'letter-spacing': 0,
        'line-height': 10,
        'select-background': 'pink',
        'select-color': 'yellow'
    })
    txt.select = 0, 0, 50, 10
    txt.show()
elif 0:
    c = Image.Color('#000')
    i = Image.new((300, 300))
    d = Image.Draw(i)
    d.rectangle((0, 0, 100, 100), c)
    print(c)
    d.rectangle((100, 0, 200, 100), c.light(0.1).rgba)
    print(c.rgba)
    d.rectangle((200, 0, 300, 100), c.light(0.2).rgba)
    print(c.rgba)
    i.show()
elif 0:
    n=Image.new((200, 15), 'white')
    n.corners(3)
    n.expand(5, 10)
    n.shadow_inside(0, 0, 10, 0, (0, 0, 0, 0.5))
    n.border(1, 'black')
    t=Image.Text('Marcos Bento')
    t.bar(0, 10)
    t.background(n)
    t.show()
elif 1:
    i = Image.new((420, 200))
    i.expand(10)
    i.fill('white')
    i.shadow_inside(0, 0, 20, 0, 'black')
    i.corners(10)
    i.border(2, 'red')
    t=Image.Text('''{Mar"Cos Bento da cunha e amor é falso não adianta 123

{Marcos Bento da cunha e amor é falso não adianta
test hahah''')
    t.style({
        'align': 'center',
        'size': 20,
        'wrap': False,
        'shadow': (-3, -3, 3, 'red'),
        'spacing': 0,
        'line-height': 10,
        'select-background': 'pink',
        'select-color': 'yellow',
        'bar-width': 1
    })
    t.delete = ''
    t.bar = 30, 0
    ic = i.copy()
    print('// real\n------------------\n', t.text)
    t.background(i)
    print('// select\n------------------\n', t.selectText)
    print('// text\n------------------\n', t.text)
    i.show()
    back, next = t.barBack, t.barNext
    if 1:
        # back
        t.bar = back
        ib = ic.copy()
        t.background(ib)
        ib.show()
        # next
        t.bar = next
        ib = ic.copy()
        t.background(ib)
        ib.show()

elif 1:
    t=Image.Text('{Marcos Bento da cunha e amor é falso não adianta\n\ntest hahah')
    t.style({
        'align': 'center',
        'size': 20,
        'wrap': False,
        'padding': 10,
        'shadow': (-3, -3, 3, 'red'),
        'spacing': 0,
        'line-height': 10,
        'select-background': 'pink',
        'select-color': 'yellow',
        'bar-width': 2
    })
    t.select = 30, 0, 150, 40
    print('// real\n------------------\n', t.text)
    i = t.image()
    print('// select\n------------------\n', t.selectText)
    print('// text\n------------------\n', t.text)
    i.fill('white')
    i.shadow_inside(0, 0, 20, 0, 'black')
    i.corners(10)
    i.border(2, 'red')
    i.show()
elif 0:
    i=Image.open('/home/marcos/Downloads/bitmap.png')
    i.fill('pink')
    i.expand(30)
    i.show()
elif 0:
    n=Image.new((200, 200), 'red')
    n.append(Image.new((200, 200), 'blue'))
    n.padding(20)
    n.show()
elif 0:
    n=Image.new((200, 200), 'red').set
    i=Image.new((100, 100)).set
    i.linear_gradient(['blue', 'transparent', 'yellow'])
    n.paste(i, 50, 50)
    n.show()
elif 0:
    print(Image.Color('#58554d').light(0.5).rgb)
elif 0:
    i=Image.open('/home/marcos/Downloads/bitmap.png').set
    i.resize(width=90)
    i.repeat((500, 500), 'loop-stretch')
    i.show()
elif 0:
    color=Image.Color('white').light(0.5)
    n=Image.new((500, 500), 'white').set
    n.radius(200, 500, 200, 500)
    n.show()
elif 1:
    n=Image.new((300, 300))
    n.fill('white')
    n.expand(20)
    n.corners(50, 75, 100, 150)
    n.linear_gradient((('red', 30), 'blue', 'green', 'yellow', 'transparent'), 'right')
    n.shadow_inside(0, 0, 30, 0, 'black')
    i=Image.open('/home/marcos/Downloads/bitmap.png')
    i.resize(width=60)
    i.repeat((380, 380), 'loop-round')
    n.corners(0)
    n.border(20, 'black', image=i)
    n.shadow_outside(0, 0, 30, 0, 'black')
    n.fill('red')
    n.show()
elif 0:
    i=i.set.resize((200, 300), 'cover')
    n=Image.new((200, 300), 'green').set
    n.paste(i).radius(30, 50, 75, 100)
    n.shadow(0, 0, 50, 0, 'black', 1)
    n.border(10, 'red')
    n.show()
elif 0:
    c=i.set.crop(200, 200, 100, 100)
    c.show()
elif 0:
    b=i.set.resize(width=200, mode='cover').radius(30, 50, 100, 10)
    b.blur(0.3).border(210, 210, 5, 5, 'red')
    b.border(220, 220, 5, 5, 'blue')
    b.show()
    b.brightness(0.2)
    b.show()
# repeat
elif 0:
    i.set.resize(width=100, mode='cover').repeat((350, 350), 'none').show()
    i.set.resize(width=100, mode='cover').repeat((350, 350), 'repeat').show()
    i.set.resize(width=100, mode='cover').repeat((350, 350), 'repeat-x').show()
    i.set.resize(width=100, mode='cover').repeat((350, 350), 'repeat-y').show()
    i.set.resize(width=100, mode='cover').repeat((350, 350), 'round').show()
    i.set.resize(width=100, mode='cover').repeat((350, 350), 'round-x').show()
    i.set.resize(width=100, mode='cover').repeat((350, 350), 'round-y').show()
# resize test
else:
    i.set.resize(height=200, mode='normal').show()
    # radius test
    i.set.resize(width=200, mode='cover').radius(100, 25, 25, 100).show()
    # alpha test
    i.set.resize(width=300, height=700, mode='contain').alpha(0.5).show()
    # rotate test
    i.set.resize(width=200, height=200, mode='fill').rotate(180).show()
