from setuptools import setup

setup(
    name='django-hibpwned',
    version='0.1',
    description='Django password validator based on haveibeenpwned.com API',
    url='https://github.com/tombiasz/django-hibpwned',
    download_url='https://github.com/tombiasz/django-hibpwned/archive/v0.1.zip',
    author='tombiasz',
    author_email='tomasz.m.nowacki@gmail.com',
    license='MIT',
    packages=['haveibeenpwned'],
    zip_safe=False,
    install_requires=[
        'Django>=1.9',
        'requests>=2'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Framework :: Django',
        'Programming Language :: Python :: 3 :: Only',
    ]
)
