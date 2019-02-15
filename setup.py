from distutils.core import setup

setup(name='framework',
      version='0.1',
      description='Framework per la raccolta di dati sviluppato durante la tesi',
      author='Andrea Giuseppe Zarola',
      packages=['framework'],
      install_requires=[
            'future',
            'pytz',
            'six',
            'apscheduler',
            'thrift',
            'pyhive',
            'flask'
      ],
      zip_safe=False)
