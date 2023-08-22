import os
from time import sleep
from load_django import *
from facebook_ads.models import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


countries = {'Australia': 'AU', 'Austria': 'AT', 'Azerbaijan': 'AZ', 'Aland Islands': 'AX', 'Albania': 'AL', 'Algeria': 'DZ', 'American Virgin Islands': 'VI', 'Anguilla': 'AI', 'Angola': 'AO', 'Andorra': 'AD', 'Antarctica': 'AQ', 'Antigua': 'AG', 'Argentina': 'AR', 'Armenia': 'AM', 'Aruba': 'AW', 'Bahamas': 'BS', 'Bangladesh': 'BD', 'Barbados': 'BB', 'Bahrain': 'BH', 'Belarus': 'BY', 'Belize': 'BZ', 'Belgium': 'BE', 'Benin': 'BJ', 'Bermuda Islands': 'BM', 'Bulgaria': 'BG', 'Bolivia': 'BO', 'Bonaire, Sint Eustatius, and Saba': 'BQ', 'Bosnia and Herzegovina': 'BA', 'Botswana': 'BW', 'Brazil': 'BR', 'British Indian Ocean Territory': 'IO', 'British Virgin Islands': 'VG', 'Brunei': 'BN', 'Burkina Faso': 'BF', 'Burundi': 'BI', 'Bhutan': 'BT', 'Vanuatu': 'VU', 'United Kingdom': 'GB', 'Hungary': 'HU', 'Venezuela': 'VE', 'United States Minor Outlying Islands': 'UM', 'Eastern Samoa': 'AS', 'East Timor': 'TL', 'Vietnam': 'VN', 'Gabon': 'GA', 'Haiti': 'HT', 'Guyana': 'GY', 'Gambia': 'GM', 'Ghana': 'GH', 'Guadeloupe': 'GP', 'Guatemala': 'GT', 'Guinea': 'GN', 'Guinea-Bissau': 'GW', 'Germany': 'DE', 'Guernsey': 'GG', 'Gibraltar': 'GI', 'Honduras': 'HN', 'Vatican City State': 'VA', 'Grenada': 'GD', 'Greenland': 'GL', 'Greece': 'GR', 'Georgia': 'GE', 'Guam': 'GU', 'Denmark': 'DK', 'Democratic Republic of the Congo': 'CD', 'Jersey': 'JE', 'Djibouti': 'DJ', 'Dominican Republic': 'DO', 'Dominica': 'DM', 'Egypt': 'EG', 'Zambia': 'ZM', 'Zimbabwe': 'ZW', 'India': 'IN', 'Indonesia': 'ID', 'Jordan': 'JO', 'Iraq': 'IQ', 'Ireland': 'IE', 'Iceland': 'IS', 'Spain': 'ES', 'Italy': 'IT', 'Yemen': 'YE', 'Cape Verde': 'CV', 'Kazakhstan': 'KZ', 'Cayman Islands': 'KY', 'Cambodia': 'KH', 'Cameroon': 'CM', 'Canada': 'CA', 'Qatar': 'QA', 'Kenya': 'KE', 'Cyprus': 'CY', 'Kiribati': 'KI', 'Colombia': 'CO', 'Comoros': 'KM', 'Kosovo': 'XK', 'Costa Rica': 'CR', 'Ivory Coast': 'CI', 'Kuwait': 'KW', 'Kyrgyzstan': 'KG', 'Curaçao': 'CW', 'Laos': 'LA', 'Latvia': 'LV', 'Lesotho': 'LS', 'Liberia': 'LR', 'Lebanon': 'LB', 'Libya': 'LY', 'Lithuania': 'LT', 'Liechtenstein': 'LI', 'Luxembourg': 'LU', 'Mauritius': 'MU', 'Mauritania': 'MR', 'Madagascar': 'MG', 'Mayotte': 'YT', 'North Macedonia': 'MK', 'Malawi': 'MW', 'Malaysia': 'MY', 'Mali': 'ML', 'Maldives': 'MV', 'Malta': 'MT', 'Morocco': 'MA', 'Martinique': 'MQ', 'Marshall Islands': 'MH', 'Mexico': 'MX', 'Mozambique': 'MZ', 'Moldova': 'MD', 'Monaco': 'MC', 'Mongolia': 'MN', 'Montserrat': 'MS', 'Myanmar': 'MM', 'Namibia': 'NA', 'Nauru': 'NR', 'Nepal': 'NP', 'Niger': 'NE', 'Nigeria': 'NG', 'Netherlands': 'NL', 'Nicaragua': 'NI', 'Niue': 'NU', 'New Zealand': 'NZ', 'Norway': 'NO', 'United Arab Emirates': 'AE', 'Oman': 'OM', 'Bouvet Island': 'BV', 'Isle of Man': 'IM', 'Saint Helena': 'SH', 'Cook Islands': 'CK', 'Turks and Caicos Islands': 'TC', 'Pakistan': 'PK', 'Palau': 'PW', 'Palestine': 'PS', 'Panama': 'PA', 'Papua New Guinea': 'PG', 'Paraguay': 'PY', 'Peru': 'PE', 'Pitcairn': 'PN', 'Poland': 'PL', 'Portugal': 'PT', 'Puerto Rico': 'PR', 'Republic of the Congo': 'CG', 'Réunion': 'RE', 'Rwanda': 'RW', 'Romania': 'RO', 'El Salvador': 'SV', 'Samoa': 'WS', 'San Marino': 'SM', 'São Tomé and Príncipe': 'ST', 'Saudi Arabia': 'SA', 'Eswatini': 'SZ', 'Northern Mariana Islands': 'MP', 'Seychelles': 'SC', 'Saint Barthélemy': 'BL', 'Saint Vincent and the Grenadines': 'VC', 'Saint Martin': 'MF', 'Saint Pierre and Miquelon': 'PM', 'Senegal': 'SN', 'Saint Kitts and Nevis': 'KN', 'Saint Lucia': 'LC', 'Saint Martin (French part)': 'MF', 'Serbia': 'RS', 'Singapore': 'SG', 'Slovakia': 'SK', 'Slovenia': 'SI', 'Solomon Islands': 'SB', 'Somalia': 'SO', 'Suriname': 'SR', 'United States': 'US', 'Sierra Leone': 'SL', 'Tajikistan': 'TJ', 'Thailand': 'TH', 'Taiwan': 'TW', 'Tanzania': 'TZ', 'Togo': 'TG', 'Tokelau': 'TK', 'Tonga': 'TO', 'Trinidad and Tobago': 'TT', 'Tuvalu': 'TV', 'Tunisia': 'TN', 'Turkmenistan': 'TM', 'Turkey': 'TR', 'Uganda': 'UG', 'Uzbekistan': 'UZ', 'Ukraine': 'UA', 'Uruguay': 'UY', 'Faroe Islands': 'FO', 'Federated States of Micronesia': 'FM', 'Fiji': 'FJ', 'Philippines': 'PH', 'Finland': 'FI', 'Falkland Islands': 'FK', 'France': 'FR', 'French Guiana': 'GF', 'Croatia': 'HR', 'Central African Republic': 'CF', 'Chad': 'TD', 'Montenegro': 'ME', 'Czech Republic': 'CZ', 'Chile': 'CL', 'Switzerland': 'CH', 'Sweden': 'SE', 'Svalbard and Jan Mayen': 'SJ', 'Sri Lanka': 'LK', 'Ecuador': 'EC', 'Equatorial Guinea': 'GQ', 'Eritrea': 'ER', 'Estonia': 'EE', 'Ethiopia': 'ET', 'South Africa': 'ZA', 'South Georgia and the South Sandwich Islands': 'GS', 'South Sudan': 'SS', 'Jamaica': 'JM', 'Japan': 'JP', 'Afghanistan': 'AF', 'Hong Kong': 'HK', 'Western Sahara': 'EH', 'Israel': 'IL', 'China': 'CN', 'Cocos (Keeling) Islands': 'CC', 'Macao': 'MO', 'Netherlands Antilles': 'AN', 'New Caledonia': 'NC', 'Norfolk Island': 'NF', 'Christmas Island': 'CX', 'Heard Island and McDonald Islands': 'HM', 'Russian Federation': 'RU', 'Wallis and Futuna': 'WF', 'French Polynesia': 'PF', 'French Southern Territories': 'TF', 'South Korea': 'KR'}
url = f'https://www.facebook.com/ads/library/?active_status=all&ad_type=political_and_issue_ads&country=UA&q=day%20night&search_type=keyword_unordered&media_type=all'

chrome_options = Options()
service = Service(executable_path=os.path.abspath('chromedriver'))
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--enable-javascript')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--lang=en')



for c in countries:
    CountrySettings.objects.get_or_create(name=c, code=countries.get(c))


# with webdriver.Chrome(service=service, options=chrome_options) as driver:
#     driver.get(url)
#     sleep(5)
#     platforms_list = []

#     ad = driver.find_elements(By.XPATH, '//div[@class="_7jvw x2izyaf x1hq5gj4 x1d52u69"]')[0]

#     platform_block = ad.find_element(By.XPATH, './/div[@class="xeuugli x2lwn1j x6s0dn4 x78zum5 x1q0g3np"]')
#     platform_items = platform_block.find_elements(By.XPATH, './/div[@class="xtwfq29"]')
#     print(len(platform_items))

#     styles = {
#         'width: 12px; height: 12px; -webkit-mask-image: url("https://static.xx.fbcdn.net/rsrc.php/v3/yT/r/914UXE21ZRK.png"); -webkit-mask-position: 0px -724px;' : 'Facebook',
#         'width: 12px; height: 12px; -webkit-mask-image: url("https://static.xx.fbcdn.net/rsrc.php/v3/y6/r/y1FuvrbyrJG.png"); -webkit-mask-position: -14px -601px;' : 'Instagram',
#         'width: 12px; height: 12px; -webkit-mask-image: url("https://static.xx.fbcdn.net/rsrc.php/v3/yZ/r/BIcOqnqNbE9.png"); -webkit-mask-position: -106px -186px;' : 'Audience Network',
#         'width: 12px; height: 12px; -webkit-mask-image: url("https://static.xx.fbcdn.net/rsrc.php/v3/yZ/r/BIcOqnqNbE9.png"); -webkit-mask-position: -68px -289px;' : 'Messenger',
#     }

#     for platform in platform_items:
#         try:
#             platform_name = styles.get(platform.get_attribute('style'))
#             platforms_list.append(platform_name)
#         except Exception as ex:
#             raise ex
#     print(platforms_list)

    # sleep(5)






