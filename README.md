# email2country (Python Package)
This is an easy-to-use Python package to look up the country given an email address. The GitHub project is at [email2country](https://github.com/zhijing-jin/email2country).

## Installation
Requirement: Python 3
```bash
pip install --upgrade git+git://github.com/zhijing-jin/email2country.git
```

## How to Run
Function 1: Find the country where the email server is located:
```python
>>> from email2country import Email, email2country
>>> email2country('zhijing@mit.edu')
'United States'

>>> addr = 'zhijing@mit.edu'
>>> Email(addr).country
'United States'

>>> addr = 'connect.hku.hk'
>>> Email(addr).country
'Hong Kong'
```
Function 2: Find the country where the institution of this email address is located:
```python
>>> from email2country import Email, email2institution_country
>>> email2institution_country('connect.hku.hk')

>>> addr = 'connect.hku.hk'
>>> Email(addr).institution_country
'Hong Kong'

>>> addr = 'zhijing@gmail.com'
>>> Email(addr).institution_country
[Info] Email domain "gmail.com" is generic. There is no specific country.

>>> addr = 'zhijing@gmail.com1'
>>> Email(addr).institution_country
[Info] Country not found for "gmail.com1"
```

## Contact
If you have more questions, feel free to contact the author [Zhijing Jin (Miss)](mailto:zhijing.jin@connect.hku.hk).