# email2country (Python Package)
This is an easy-to-use Python package to look up the country given an email address. 
- GitHub project: [https://github.com/zhijing-jin/email2country](https://github.com/zhijing-jin/email2country).
- PyPI package: `pip install `[`email2country`](https://pypi.org/project/email2country/) 

## Installation
Requirement: Python 3
```bash
pip install --upgrade git+git://github.com/zhijing-jin/email2country.git
```

## How to Run
(All country names are conssitent with ISO 3166-1)

#### Function 1: Find the country where the email server is located
```python
>>> from email2country import email2country
>>> email2country('zhijing@mit.edu')
'United States'
```
Or you can just use the domain
```python
>>> email2country('connect.hku.hk')
'Hong Kong'
```
#### Function 2: Find the country where the institution of this email address is located
```python
>>> from email2country import email2institution_country

>>> email2institution_country('zhijing@mit.edu')
'United States'

>>> email2institution_country('zhijing@gmail.com')
[Info] Email domain "gmail.com" is generic. There is no specific country.

>>> email2institution_country('zhijing@gmail.com111')
[Info] Country not found for "gmail.com111"
```
#### Function 3: Look up in batches
```python
>>> from email2country import batch_email2institution_country
>>> batch_email2institution_country(['nyu.edu','gmail.com', 'hku.hk'])
['United States', None, 'Hong Kong']

# or you can enable the "enable warning" option:
>>> batch_email2institution_country(['nyu.edu','gmail.com', 'hku.hk'], enable_warning=True)
[Info] Email domain "gmail.com" is generic. There is no specific country.
['United States', None, 'Hong Kong']

# Similarly, you can try email2country lookup
>>> from email2country import batch_email2country
>>> batch_email2country(['nyu.edu','gmail.com', 'hku.hk'])
['United States', 'United States', 'Hong Kong']
```
#### Function 4: Customize your own function
You can use the `EmailCountryChecker` object directly:
```python
>>> from email2country import EmailCountryChecker
>>> checker = EmailCountryChecker()
>>> checker.get_institution_country('hku.hk', enable_warning=True)
'Hong Kong'
>>> # ... Perform your own actions
```
Or you can use the `Email` object
```python
>>> from email2country import Email 
>>> addr = 'zhijing@mit.edu'
>>> email = Email(addr)
>>> email.country
'United States'
>>> email.institution_country
'United States'
```
## Contact
If you have more questions, feel free to contact the author [Zhijing Jin (Miss)](mailto:zhijing.jin@connect.hku.hk).