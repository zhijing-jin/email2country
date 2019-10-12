class Email:
    def __init__(self, email_addr, enable_warning=True):
        self.email_addr = email_addr
        self.country_checker = EmailCountryChecker()
        self.enable_warning = enable_warning

    @property
    def institution_country(self):
        return self.country_checker.get_institution_country(
            self.email_addr, enable_warning=self.enable_warning)

    @property
    def country(self):
        return self.country_checker.get_country(
            self.email_addr, enable_warning=self.enable_warning)


class EmailCountryChecker:
    '''
    original files:
    https://raw.githubusercontent.com/flyingcircusio/pycountry/master/src/pycountry/databases/iso3166-1.json
    https://raw.githubusercontent.com/Hipo/university-domains-list/master/world_universities_and_domains.json
    https://en.wikipedia.org/wiki/List_of_Internet_top-level_domains#Country_code_top-level_domains
    '''

    def __init__(self):
        self.code2country, self.alpha2country, self.uni_domain2country = \
            self.load_dicts()
        self.cache_domain2ip2country = {}

    @staticmethod
    def load_dicts():
        import os
        import json
        import pkg_resources

        FILE1 = pkg_resources.resource_filename('email2country',
                                                'src_data/countries_3166-1.json')
        FILE2 = pkg_resources.resource_filename('email2country',
                                                'src_data/universities.json')

        if os.path.isfile(FILE1):
            with open(FILE1) as f:
                countries = json.load(f)
        else:
            from .utils import countries

        code2country = {
            c['tld'] if 'tld' in c else c['alpha_2'].lower():
                c['common_name'] if 'common_name' in c else c['name']
            for c in countries}
        alpha2country = {
            c['alpha_2']: c['common_name'] if 'common_name' in c else c['name']
            for c in countries if 'alpha_2' in c}

        if os.path.isfile(FILE1):
            with open(FILE2) as f:
                universities = json.load(f)
        else:
            from .utils import universities

        uni_domain2country = {}
        for u in universities:
            for domain in u['domains']:
                alpha2 = u['alpha_two_code']
                uni_domain2country[domain] = alpha2country[alpha2]

        return code2country, alpha2country, uni_domain2country

    @property
    def generic_emails(self):
        return {
            '126.com', '163.com', '263.net', 'aol.com', 'gmail.com',
            'googlemail.com', 'hotmail.com', 'live.com', 'me.com',
            'outlook.com', 'qq.com', 'rediffmail.com', 'sina.com', 'sohu.com',
            'vip.sina.com', 'yahoo.com', 'yeah.net',
        }

    def domain2ip2country(self, domain):
        '''
        invalid domains by ipsearch:
            'mail.mil'
            'gwu.edu'
            'uabmc.edu'
        '''
        import socket
        import requests

        if domain in self.cache_domain2ip2country:
            return self.cache_domain2ip2country[domain]

        try:
            ip = socket.gethostbyname(domain)
        except:
            short_domain = '.'.join(domain.split('.')[1:])
            try:
                ip = socket.gethostbyname(short_domain)
            except:
                self.cache_domain2ip2country[domain] = None
                return None

        url = 'https://ipvigilante.com/{}/country_iso_code'.format(ip)
        r = requests.get(url)
        if r.status_code == 200:
            alpha2 = r.json()['data']['country_iso_code']
            country = self.alpha2country[alpha2]
            self.cache_domain2ip2country[domain] = country
            return country

        self.cache_domain2ip2country[domain] = None
        return None

    def get_institution_country(self, email_addr, enable_warning=True):
        domain = email_addr.rsplit('@')[-1].strip('.')
        domain2 = '.'.join(domain.rsplit('.', 2)[-2:])
        if domain2 in self.generic_emails:
            if enable_warning:
                print(
                    '[Info] Email domain "{}" is generic. There is no specific country.'
                        .format(domain))
        else:
            return self.get_country(domain, enable_warning=enable_warning)

    def get_country(self, email_addr, enable_warning=True):
        domain = email_addr.rsplit('@')[-1].strip('.')

        code2country = self.code2country
        uni_domain2country = self.uni_domain2country

        suffix = domain.rsplit('.')[-1]

        if suffix in code2country: return code2country[suffix]
        if domain in uni_domain2country: return uni_domain2country[domain]

        domain2 = '.'.join(domain.rsplit('.', 2)[-2:])
        if domain2 in uni_domain2country: return uni_domain2country[domain2]

        country = self.domain2ip2country(domain)
        if country: return country

        if enable_warning:
            print('[Info] Country not found for "{}"'.format(domain))

    @staticmethod
    def download_tld():
        import requests
        try:
            import lxml
        except ImportError:
            import os
            os.system('pip install lxml')
        from lxml.html import fromstring

        url = 'https://en.wikipedia.org/wiki/List_of_Internet_top-level_domains#Country_code_top-level_domains'
        r = requests.get(url)
        html = fromstring(r.text)
        tld_header = html.get_element_by_id("Country_code_top-level_domains")
        tld_elem = tld_header.getparent().getnext().getnext().getnext()

        tld = {}

        for line in tld_elem.xpath('.//tbody//tr')[1:]:
            suffix = line.xpath('.//td//a')[0].text
            country = line.xpath('.//td//a')[1].text
            tld[suffix] = country
        import pdb;
        pdb.set_trace()
        return tld


def email2country(email_addr, enable_warning=True):
    return Email(email_addr, enable_warning=enable_warning).country


def email2institution_country(email_addr, enable_warning=True):
    return Email(email_addr, enable_warning=enable_warning).institution_country


def batch_email2country(list_email_addr, enable_warning=False):
    if not isinstance(list_email_addr, list):
        list_email_addr = [list_email_addr]
    checker = EmailCountryChecker()
    countries = [checker.get_country(i, enable_warning=enable_warning)
                 for i in list_email_addr]
    return countries


def batch_email2institution_country(list_email_addr, enable_warning=False):
    if not isinstance(list_email_addr, list):
        list_email_addr = [list_email_addr]
    checker = EmailCountryChecker()
    countries = [
        checker.get_institution_country(i, enable_warning=enable_warning)
        for i in list_email_addr]
    return countries


def test():
    email2country('zhijing@csail.mit.edu')
    batch_email2institution_country(['zhijing@csail.mit.edu'])

    addr = 'zhijing@csail.mit.edu'
    country = Email(addr).country

    addr = 'connect.hku.hk.'
    country = Email(addr).country

    addr = 'zhijing@nyu.edu'
    country = Email(addr).country

    addr = 'zhijing@gmail.com'
    country = Email(addr).institution_country

    addr = 'zhijing@gmail.com1'
    country = Email(addr).institution_country


if __name__ == '__main__':
    test()
