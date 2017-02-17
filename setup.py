from setuptools import setup, find_packages

setup(name='gqrxHamlib',
      version = '2.4',
      description = 'gqrx-Hamlib interface',
      url='http://github.com/g0fcu/gqrx-hamlib-gui',
      author='Simon Kennedy',
      license='GPL',
      packages=find_packages(),
      #install_requires=['PyQt4'],
      entry_points={
          'console_scripts': [
               'gqrxHamlib=gqrxHamlib:main'
                  ]
                }
)
