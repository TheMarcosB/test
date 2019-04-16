from lib.GI import *
w = window()
w.title = 'Marcos'
w.width = 700
d = document(w)
# header
header = d.createTag('header')
header.style({
   'width': calc('100% - 20px'),
   'height': '30px',
   'float': 'left',
   'padding': '10px',
   'background-image': linear_gradient('to left', 'red', 'blue'),
   'border-color': '#c5c5c5',
   'border-bottom': '1px'
})
# sidebar
sidebar = d.createTag('sidebar')
sidebar.style({
   'width': '200px',
   'height': calc('100% - 51px'),
   'float': 'left',
   'padding': (0, '10px', 0, '10px'),
   'background-color': '#efefef',
   'border-color': '#c5c5c5',
   'border-right': '1'
})
# sidebar transition
_bool = 0
def test(event):
    global _bool
    if _bool:
        _bool = 0
        sidebar.style['-transition-width'] = 200
        transition(sidebar, 20)
    else:
        sidebar.style['-transition-width'] = 400
        transition(sidebar, 20)
        _bool = 1
w.setInterval(test, 3000)
# sidebar labels
for title, tags in [('filmes', ['ação', 'ficção', 'terror']), ('músicas', ['rock', 'rap', 'pop', ''])]:
    # add title
    label = sidebar.createTag('title')
    label.value = title.capitalize()
    label.style({
       'color': '#7f7f7f',
       'font-size': '17px',
       'height': '30px',
       'margin-top': '10px',
       'text-shadow': (1, 1, 0, 'white')
    })
    # add tags
    for tag in tags:
        label = sidebar.createTag('tag')
        label.value = tag.capitalize()
        label.style({
           'color': '#4f4f4f',
           'font-size': '13px',
           'margin-left': '20px',
           'margin-bottom': '5px',
           'font-weight': 'bold',
           'text-shadow': (1, 1, 0, 'white')
        })
# main
main = d.createTag('main')
main.style({
   'width': '100l',
   'height': '100l',
   'float': 'left',
})
# funtion add label in main
def addlabel(color='blue'):
    label = main.createTag('label')
    label.style({
      'width': '150px',
      'height': '150px',
      'float': 'left',
      'background-color': light(color, 0.5),
      'border': ('5px', 'solid', 'red'),
      'box-shadow': (5, 5, 10, 0, rgba(0, 0, 0, 0.5), 'outset'),
      'border-radius': ('50%', '35%', '20%', '5%'),
      'margin-left': '20px',
      'margin-top': '20px'
    })
# main labels
for color in ['red', 'blue', 'pink', 'orange', 'green', 'yellow']:
    addlabel(color)
# other
button1 = sidebar.createTag('button')
button2 = sidebar.createTag('button')
check = sidebar.createTag('check')
radio = sidebar.createTag('radio')
slider = sidebar.createTag('slider')
# add click in button2
button2.on.click = lambda this: addlabel()
# start GI
loop()
