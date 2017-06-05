from distutils.core import setup

setup(
  name = 'http_api_exporter',
  packages = ['http_api_exporter'],
  version = '1.0.6',
  description = 'A simple api exporter for py',
  author = 'Sraw',
  author_email = 'lzyl888@gmail.com',
  url = 'https://github.com/Sraw/http_api_exporter', 
  download_url = 'https://github.com/Sraw/http_api_exporter/tarball/v1.0.6', 
  keywords = ['http', 'web', 'api', 'export'], 
  classifiers = [
      'Programming Language :: Python :: 3'
    ],
  install_requires=[
          'tornado>=4.4.3,<=4.5',
      ],
)
