from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='email2country',
    version='0.1.0',
    packages=find_packages(exclude=['tests*']),
    package_dir={'mypkg': 'email2country'},
    package_data={'mypkg': ['data/*.json']},
    license='MIT',
    description='A package to look up the country of email addresses and domains',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['numpy'],
    url='https://github.com/zhijing-jin/email2country',
    author='Zhijing Jin',
    author_email='zhijing.jin@connect.hku.hk'
)
