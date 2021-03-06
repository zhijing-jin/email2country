# email2country (Python Package)
[![Pypi](https://img.shields.io/pypi/v/email2country.svg)](https://pypi.org/project/email2country)
[![Downloads](https://pepy.tech/badge/email2country)](https://pepy.tech/project/email2country)
[![Month_Downloads](https://pepy.tech/badge/email2country/month)](https://pepy.tech/project/email2country/month)
[![MIT_License](https://camo.githubusercontent.com/890acbdcb87868b382af9a4b1fac507b9659d9bf/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6c6963656e73652d4d49542d626c75652e737667)](LICENCE)

This is an easy-to-use Python package to look up the country given an email address. 
- GitHub project: [https://github.com/zhijing-jin/email2country](https://github.com/zhijing-jin/email2country).
- PyPI package: `pip install`[`email2country`](https://pypi.org/project/email2country/) 

## Installation
Requirement: Python 3
```bash
pip install --upgrade git+git://github.com/zhijing-jin/email2country.git
```

## How to Run
(All country names are consistent with [ISO 3166-1](email2country/data/countries_3166-1.json).)

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

## In Case of Unexpected Outputs
The main mechanism is in `EmailCountryChecker` > `get_country()`[here](email2country/email2country.py).
1. Not distinguishable if domain is in `generic_emails` (e.g. gmail.com). `domain` is `email_addr.rsplit('@')[-1].strip('.')`.
2. Return country if `code2country[suffix]` exists. `suffix` is `domain.rsplit('.')[-1]`.
3. Return country if `uni_domain2country[domain]` exists.
4. `domain2` is `'.'.join(domain.rsplit('.', 2)[-2:])`. Return country if `uni_domain2country[domain2]` exists.
5. Last resort is `domain2ip2country(domain)`, first looking up the IP of the domain, and then look up the country of the IP.

## Contact
If you have more questions, feel free to [Q&A](https://github.com/zhijing-jin/email2country/issues?utf8=%E2%9C%93&q=is%3Aissue), or raise a new GitHub issue.

In case of really urgent needs, contact the author [Zhijing Jin (Miss)](mailto:zhijing.jin@connect.hku.hk).
