from distutils.core import setup

setup(name='Game Server',
      version='0.1',
      description='Simple game server',
      author='Mark Jennings',
      author_email='jenningsm42@gmail.com',
      packages=[],
      entry_points={
          'console_scripts': ['game-server=server.main:main'],
      })
