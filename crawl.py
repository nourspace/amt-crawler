import time
from datetime import datetime

import click
import pytz
from requests_html import HTMLSession

from notify import update_worksheet, post_to_slack
from safe_schedule import SafeScheduler

BOOKABLE_CLASS_SELECTOR = '.buchbar'


@click.command()
@click.argument('url')
@click.option('--worksheet', '-w', 'worksheet', default='Amt Crawls')
@click.option('--channel', '-s', 'channel', default='#amt-crawls')
@click.option('--rand-lo', '-l', 'rand_lo', default=5)
@click.option('--rand-up', '-u', 'rand_up', default=10)
@click.option('--min-bookable', '-m', 'min_bookable', default=1)
def crawl(**kwargs):
    scheduler = SafeScheduler()
    rand_lo = kwargs.pop('rand_lo')
    rand_up = kwargs.pop('rand_up')
    scheduler.every(rand_lo).to(rand_up).seconds.do(work, **kwargs)
    while True:
        scheduler.run_pending()
        time.sleep(1)


def work(url, worksheet, channel, min_bookable):
    print(f'Crawling: {url}')
    session = HTMLSession()
    res = session.get(url)
    print(res)
    bookable = res.html.find(BOOKABLE_CLASS_SELECTOR)
    bookable_count = len(bookable) - 1
    print(f'Bookable appointments: {bookable_count}')
    timestamp = datetime.now(tz=pytz.timezone('CET')).strftime('%Y-%m-%d %H:%M:%S')
    values = [timestamp, bookable_count]
    update_worksheet(worksheet, values)
    if bookable_count >= min_bookable:
        post_to_slack(channel, f'Found {bookable_count} appointments on {timestamp}\nBook now: {url}')
    print('-----')


if __name__ == '__main__':
    crawl()
