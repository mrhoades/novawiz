import setuptools

setuptools.setup(
    name='novawiz',
    version='0.0.13',
    packages=['novawiz',],
    author='tim miller',
    author_email='name@example.com',
    url='github.com/echohead/novawiz',
    license='',
    description="a command-line wizard for nova",
    long_description=open('README').read(),
    entry_points={
      'console_scripts': ['novawiz = novawiz.shell:main']
    },
    install_requires=['python-novaclient', 'paramiko']
)
