from setuptools import setup, find_packages

setup(
    name='aiosmtpmod',
    version='0.1',
    description='Extensions to aiosmtp to provide USER LOGIN',
    author='Grahame Gardiner',
    author_email='grahamegee@gmail.com',
    url='https://github.com/grahamegee/smtp-test-server',
    install_requires=[
        'aiosmtpd',
        'aiohttp',
        'argparse'
    ],
    package_data={
        'data': ["*.pem"]
    },
    extras_require={}
)
