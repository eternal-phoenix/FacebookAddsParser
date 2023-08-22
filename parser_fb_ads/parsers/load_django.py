import sys
import os
import django

sys.path.append(os.path.abspath("parser_fb_ads"))
os.environ['DJANGO_SETTINGS_MODULE'] = 'parser_fb_ads.settings'
django.setup()
