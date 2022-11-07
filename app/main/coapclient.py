import asyncio
from aiocoap import *

#receive the lamp status using coap. Once received, send the status to the webserver and show the status on the webpage
async def coapgetlampstatus(url):
    print('coapgetlampstatus on', url)
    protocol = await Context.create_client_context()
    request = Message(code=GET, uri=url)

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:', e)
    else:
        print('Result: %s\n%r'%(response.code, response.payload))
        return response.payload

#set the lamp status using coap. Change the value using the slider on the webpage
async def coapsetlampstatus(url, value):
    print('coapsetlampstatus on', url, 'with value', value)
    protocol = await Context.create_client_context()
    request = Message(code=PUT, uri=url, payload=value)

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:', e)
    else:
        print('Result: %s'%(response.code))
        