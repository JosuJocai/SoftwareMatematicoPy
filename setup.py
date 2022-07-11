from setuptools import setup

setup(
   name='entregapack',
   version='0.0.1',
   author='Josu Oca',
   author_email='joca002@ikasle.ehu.eus',
   packages=['permupack', 'permupack.test'],
   url='Indicar una URL para el paquete...',
   license='LICENSE.txt',
   description='Paquete para la entrega de Software Matematico y Estadistico',
   long_description=open('README.ipynb').read(),
   tests_require=['pytest'],
   install_requires=[
      "pandas >= 0.25.1",
      "matplotlib >= 3.1.1",
      "numpy >=1.17.2"
   ],
)