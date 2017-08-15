from setuptools import setup

setup(
    name='django-hibpwned',
    version='0.1',
    description='Django password validator based on haveibeenpwned.com API',
    url='',
    author='tombiasz',
    author_email='',
    license='MIT',
    packages=['haveibeenpwned'],
    zip_safe=False,
    install_requires=[
        'Django>=1.9',
    ]
)
