from setuptools import setup

setup(
    name='zoho-crm-api',
    version='0.0.1',
    packages=['zoho_crm_api'],
    url='',
    license='MIT',
    author='Michal Bock',
    author_email='michal@ueni.com',
    description='Simple python API client for Zoho CRM.',
    install_requires=[
        'requests==2.18.4'
    ]
)
