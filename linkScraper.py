# geoLocatoScraper.py
'''
This program will be corrected and changed to OOP.
This program:
1. Scrapes links, image's file links, info using module mechanize, BeautifulSoup library.
2. Dowload image files.

'''
from genericpath import isdir
import os
import re
import mechanize
from bs4 import BeautifulSoup
import requests
from pathlib import Path

print(f'home:{Path.home()}')

urls = ['https://virtualpeople.pl',
        'https://virtualpeople.pl/realizacje']  # enter your urls

#
#   setting the path
#

# home directory path is always the same so will not be changed after next iteration ! always remove 1st slash inide Path():
pat_h = Path.home() / Path('Python projects/Python Projects/Intro_to_python_for_computer_since/7_Ndarray_Series_DataFrames/scraper1/virtual')

# check if pat_h is existing directory
if pat_h.exists():
    # change current working directory
    os.chdir(str(Path.home() / Path('Python projects/Python Projects/Intro_to_python_for_computer_since/7_Ndarray_Series_DataFrames/scraper1/virtual')))
else:
    try:
        # change current working directory
        os.chdir(str(Path.home(
        ) / Path('Python projects/Python Projects/Intro_to_python_for_computer_since/7_Ndarray_Series_DataFrames/Scraper1')))

        os.mkdir('virtual')
        # changing current working dirwctory
        os.chdir(str(Path.home(
        ) / Path('Python projects/Python Projects/Intro_to_python_for_computer_since/7_Ndarray_Series_DataFrames/Scraper1/virtual')))

        # convert path object to string
        pat_h = str(Path.cwd())
    except FileExistsError:
        pass


for fb_url in urls:
    print('================')
    print(f"Ekstrkting links and jpg files for the:\n{fb_url}")
    print(f"{len(fb_url)*'*'}")

    # setting mechanize!
    br = mechanize.Browser()
    br.set_handle_robots(False)
    print('br1: ', br)
    # out: <Browser (not visiting a URL)>
    
    html = br.open(fb_url)
    htmltext = html.read()
    # print('htmltext: ',htmltext)  # print all html code

    print(f'br.open: {br}')
    # out: br.open: <Browser visiting https://virtualpeople.pl>

    print('br.geturl(): ', br.geturl())

    # out: br.geturl():  https://virtualpeople.pl
    print()

    full_html1 = br.response()
    print('full_html1', full_html1)
    # out: full_html1 <response_seek_wrapper at 0x7f9de8289750 ...
    print(3 * '--------------')

    full_html = br.response().get_data()  # the same line 64
    # print(f'full_html:\n{full_html}') # printing all html code from web page

    print('title: ', br.title())
    # out: title:  Marketing internetowy oraz projektowanie stron www Szczecin

    ln = 'https://www.linkedin.com/in/grzegorz-kozak-961758125?trk=nav_responsive_tab_profile_pic'
    pr = (f"{'Link':<{len(ln) + 4}}{'Description:'}")
    print(f"{pr}\n{len(pr) * '='}")
    count = 0

    #
    #
    # looping through the links
    #

    for link in br.links():
        count += 1
        # print(link)
        # out: Link(base_url='https://virtualpeople.pl/', url='javascript:void(0)', text='Oferta', tag='a', attrs=[('href', 'javascript:void(0)'), ('class', 'offer')])
        # Link(base_url='https://virtualpeople.pl/', url='https://virtualpeople.pl/realizacje', text='Realizacje', tag='a', attrs=[('href', 'https://virtualpeople.pl/realizacje')])

        if link.url == 'javascript:void();':
            continue
        elif link.url == 'javascript:void(0)':
            continue
        elif link.url == 'javascript:void(0);':
            continue
        elif link.url == 'javascript:void()':
            continue
        print(f"{count}.{link.url:<{len(ln) + 4}}{link.text}")
        # out: 4.https://virtualpeople.pl/realizacje                                                        Realizacje

    # preparing the table
    line = (
        len('https://virtualpeople.pl/assets/gfx/person/grzegorz.jpg ') + len('Name:'))
    print(f"\n{'Extractin links with .jpg pictures from:'}\n{fb_url}")
    print(f"{'Links with photo':<{line}}  {'Name:'}")
    print(f"{(line + 7) * '~'}")

    #
    #
    #   scraping img files
    #

    # object
    soup = BeautifulSoup(htmltext, features='lxml')  # features = parser

    # object
    results = soup.find_all('img')

    '''print('printing reusult from soup.find_all("img")')
    for result in results:
      print(result)
    out: <img alt="Grzegorz" src="https://virtualpeople.pl/assets/gfx/person/grzegorz.jpg"/> '''

    count = 0
    for result in results:

        #   extracting only img files
        if result['src'].endswith('.jpg'):
            count += 1
            print(f"{count}.{result['src']}")

            print(f"file name to download: {os.path.basename(result['src'])}")

            #
            #
            # downloading jpg files
            #

            # creating files which will be loaded with data from .jpg photos
            vir_file = open(os.path.join(pat_h, os.path.basename(
                result['src'])), 'wb')  # 'wb' must be obligatory
            # print(f'vir_file:{vir_file}')

            # downloaging the file using request.iter_content(nr of bytes)
            # downloading the url for only jpg files
            res = requests.get(result['src'])

            # looping through url to save jpg file file
            for chunk in res.iter_content(100_000):  # 100_000 bytes
                vir_file.write(chunk)
            vir_file.close()


print(20*'+++')
