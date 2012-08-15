import setuptools

setuptools.setup(
    name='novawiz',
    version='0.0.2',
    packages=['novawiz',],
    author='tim miller',
    author_email='name@example.com',
    url='github.com/echohead/novawiz',
    license='Do What The Fuck You Want To Public License',
    long_description=open('README.md').read(),
    entry_points={
      'console_scripts': ['novawiz = novawiz.shell:main']
    }
)
