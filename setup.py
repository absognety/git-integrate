from setuptools import setup, find_packages

setup(
    name='git_integrate',
    version='0.1',
    description='Git Integration API package',
    url='https://github.com/absognety/git-integrate', 
    author='Vikas Chitturi',
    author_email='vikasch.1994@gmail.com',
    packages=find_packages(),
    install_requires=[
        'PyGithub'
    ],
    entry_points={
        'console_scripts': ['gitapi=git_integrate.driver:main']
    }
)