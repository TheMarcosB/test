from lib import Url, Number
from PIL import Image
import io

start = ('-' * 50) + '\n//'
center = '\n' + ('-' * 50) + '\n'
end = '\n'
link = 'http://facebook.com'
print(start, 'url check:',         center, Url.check(link),         end)
print(start, 'url split:',         center, Url.split(link),         end)
print(start, 'url protocol code:', center, Url.protocol(link),      end)
print(start, 'url encode:',        center, Url.encode(link),        end)
print(start, 'url get:',           center, Url.get(link+'?test=123&marcos'),           end)
print(start, 'url get parse:',     center, Url.get_parse(link+'?test=123&marcos'),     end)
print(start, 'url get join:',      center, Url.get_join(Url.get_parse(link+'?test=123&marcos')), end)

# open url
url = Url.open(link)
print(start, 'url head:',        center, url.head,          end)
print(start, 'url header:',      center, url.header,        end)
print(start, 'url status code:', center, url.status,        end)
print(start, 'url status info:', center, url.status.info(), end)
print(start, 'url status full:', center, url.status.full(), end)
print(start, 'url exists:',      center, url.exists,        end)
print(start, 'url location:',    center, url.location,      end)
print(start, 'url length:',      center, url.length,        end)
print(start, 'url mime:',        center, url.mime,          end)
print(start, 'url type:',        center, url.type,          end)

if 0:
    # get image
    image_data = url.bytes()
    image = Image.open(io.BytesIO(image_data))
    image.show()

elif 0:
    # send post
    link = 'http://localhost:8888'
    print(start, 'url sendpost:', Url.sendpost(link, {'marcos': 'abc 123 /*', 'test':'real fire'}), end)

elif 0:
    print(start, 'url content:', center, url.content, end)

else:
    url.save('${ETC}')
