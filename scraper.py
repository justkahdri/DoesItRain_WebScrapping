import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://www.cenital.com/'
XPATH_LINK_TO_ARTICLE = '//h2[@class="SecondaryNoteTitle"]/a/@href'
XPATH_TITLE = '//header[@class="entry-header"]/h1/text()'
XPATH_SUMMARY = '//header/div[@class="bajadaNota BajadaSingle"]/text()'
XPATH_ENTRY_CONTENT = '//div[@class="entry-content"]/p/text()'
NOT_SUPPORTED = ['\"', '?', '¿', '*', ':']


def parse_notice(link, today):
    try:
        response = requests.get(link, headers={"User-Agent": "J5"})
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(XPATH_TITLE)[0].rstrip()
                for char in NOT_SUPPORTED:
                    title = title.replace(char, '')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_ENTRY_CONTENT)
            except IndexError:
                return

            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title + '\n\n' + summary + '\n\n')
                for p in body:
                    f.write(p + '\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError:
        print(ValueError)


def parse_home():
    try:
        response = requests.get(HOME_URL, headers={"User-Agent": "J5"})
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)

            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)

            for link in links_to_notices:
                parse_notice(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


if __name__ == '__main__':
    parse_home()
