# email2country (Python Package)
This is an easy-to-use Python package to look up the country given an email address. The GitHub project is at [email2country](https://github.com/zhijing-jin/email2country).

## Installation
Requirement: Python 3
```bash
pip install --upgrade git+git://github.com/zhijing-jin/email2country.git
```

## How to Run
(All country names are conssitent with ISO 3166-1)

Function 1: Find the country where the email server is located:
```python
>>> from email2country import Email, email2country
>>> email2country('connect.hku.hk')
'Hong Kong'

>>> email2country('zhijing@mit.edu')
'United States'

>>> addr = 'zhijing@mit.edu'
>>> Email(addr).country
'United States'
```
Function 2: Find the country where the institution of this email address is located:
```python
>>> from email2country import Email, email2institution_country
>>> email2institution_country('connect.hku.hk')
'Hong Kong'

>>> email2institution_country('zhijing@gmail.com')
[Info] Email domain "gmail.com" is generic. There is no specific country.

>>> email2institution_country('zhijing@gmail.com111')
[Info] Country not found for "gmail.com111"

>>> addr = 'connect.hku.hk'
>>> Email(addr).institution_country
'Hong Kong'
```
Function 3: Look up in batches:
```python
>>> from email2country import batch_email2institution_country
>>> batch_email2institution_country(['nyu.edu','gmail.com', 'hku.hk'], enable_warning=False)
['United States', None, 'Hong Kong']

# or you can enable the "enable warning" option:
>>> batch_email2institution_country(['nyu.edu','gmail.com', 'hku.hk'], enable_warning=True)
[Info] Email domain "gmail.com" is generic. There is no specific country.
['United States', None, 'Hong Kong']

# Similarly, you can try email2country lookup
>>> from email2country import batch_email2country
>>> batch_email2country(['nyu.edu','gmail.com', 'hku.hk'])
```
Function 4: Customize your own function
```python
>>> from email2country import EmailCountryChecker
>>> checker = EmailCountryChecker()
>>> checker.get_institution_country('hku.hk', enable_warning=True)
'Hong Kong'
>>> # ... Perform your own actions

```
## Contact
If you have more questions, feel free to contact the author [Zhijing Jin (Miss)](mailto:zhijing.jin@connect.hku.hk).