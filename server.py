import asyncio
import logging
import ssl

from binascii import Error as BaError
from base64 import b64encode, b64decode
from aiosmtpd.controller import Controller
from aiosmtpd.handlers import Sink, Debugging
from aiosmtpd.smtp import SMTP
from email import message_from_bytes
from pprint import pprint


# FIXME: This should be config.
USERNAME = 'x'
PASSWORD = 'x'


class ExtendedSMTP(SMTP):
    async def smtp_AUTH(self, arg):
        if arg.upper() == 'LOGIN':
            await self.push('334 {}'.format(b64encode(b'Username').decode()))
            try:
                username = await self._reader.readline()
                username = b64decode(username.rstrip(b'\r\n')).decode('ascii')
                await self.push(
                    '334 {}'.format(b64encode(b'Password').decode()))
                password = await self._reader.readline()
                password = b64decode(password.rstrip(b'\r\n')).decode('ascii')
            except BaError:
                # FIXME: correct error code?
                await self.push('500 Challenge must be Base64 encoded')
            # FIXME: Captured that correct exceptions?
            # probably need to break out into separate branches also.
            # ConnectionReset should be handled separately.
            except (ConnectionResetError, asyncio.CancelledError):
                await self.push(
                    '503 for AUTH LOGIN supply username then password')
            if username == USERNAME and password == PASSWORD:
                await self.push('235 Authentication successful')
            else:
                await self.push('535 Invalid credentials')
        else:
            await self.push('504 AUTH {} Not Implemented'.format(arg))


class MessageForwarder:
    async def handle_DATA(self, server, session, envelope):
        data = envelope.content
        message = message_from_bytes(data)
        msg_dict = {k: v for k, v in message.items()}
        msg_dict['Body'] = message.get_payload()
        pprint(msg_dict)
        return '250 OK'


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain('cert.pem', 'key.pem')
    
    loop = asyncio.get_event_loop()
    smtp = lambda: ExtendedSMTP(
        MessageForwarder(), enable_SMTPUTF8=True, loop=loop)

    server = loop.run_until_complete(
        loop.create_server(
            smtp,
            host='0.0.0.0',
            port=8025,
            ssl=context))
    loop.run_forever()
