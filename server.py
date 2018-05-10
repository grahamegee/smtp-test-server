import asyncio
import logging
import ssl

from aiosmtpd.controller import Controller
from aiosmtpd.handlers import Sink, Debugging
from aiosmtpd.smtp import SMTP


class ExtendedSMTP(SMTP):
    async def smtp_AUTH(self, arg):
        import ipdb; ipdb.set_trace()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain('cert.pem', 'key.pem')
    
    loop = asyncio.get_event_loop()

    server = loop.run_until_complete(
        loop.create_server(
            smtp,
            host='0.0.0.0',
            port=8025,
            ssl=context))
    loop.run_forever()
