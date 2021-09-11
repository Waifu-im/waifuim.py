import re
from setuptools import setup
with open('horiapi/__init__.py', 'r') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='horiapi.py',
    version=version,
    packages=['horiapi'],
    url='https://github.com/Bucolo/horiapi.py',
    download_url='https://github.com/Bucolo/horiapi.py/archive/refs/tags/1.1.3.tar.gz',
    project_urls={
        'Issue tracker': 'https://github.com/Bucolo/horiapi.py/issues'
    },
    license='MIT',
    author='Buco',
    description='A Python wrapper for Hori API.',
    author_email='bucolo33fr@gmail.com',
    long_description=readme,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    install_requires=['aiohttp'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ]
)
