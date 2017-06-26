from setuptools import setup, find_packages

from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'http_api_exporter',
  packages = find_packages(),
  version = '1.2.3',
  license = 'MIT',
  description = 'A simple api exporter for py',
  long_description = long_description,
  author = 'Sraw',
  author_email = 'lzyl888@gmail.com',
  url = 'https://github.com/Sraw/http_api_exporter', 
  download_url = 'https://github.com/Sraw/http_api_exporter/tarball/v1.2.3', 
  keywords = "http web api export", 
  classifiers = [
      'Development Status :: 5 - Production/Stable',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python',
      'Topic :: Internet :: WWW/HTTP :: HTTP Servers'
    ],
  install_requires=[
          'tornado>=4.0.0,<5.0.0',
      ],
  test_suite="tests.main"
)
