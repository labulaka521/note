import asyncio
from aiohttp import web

import logging
logging.basicConfig(level=logging.INFO)


async def index(request):
    await asyncio.sleep(0.5)
    return web.Response(body=b'<h1>Index</h1>\n', content_type='text/html')

async def hello(request):
    print(help(request))
    print(request.message)
    await asyncio.sleep(0.5)
    text = '<h1>hello, %s!</h1>\n' % request.match_info['name']
    return web.Response(body=text.encode('utf-8'), content_type='text/html')


async def init():
    # app = web.Application(loop=loop)
    # srv = await loop.create_server(app._make_handler(), '127.0.0.1',8000)
    app = web.Application()
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/hello/{name}', hello)
    web.run_app(app, host='127.0.0.1',port=9000)
    # logging.info('server started at http;//127.0.0.1:9000...')

    # return srv


loop = asyncio.get_event_loop()
loop.run_until_complete(init())
loop.run_forever()
