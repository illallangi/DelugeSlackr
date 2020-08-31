from atexit import register as atexit_register
from os.path import basename
from sys import argv, stderr
from time import time

from click import Choice as CHOICE, STRING, argument, group, option, version_option

from loguru import logger

from notifiers.logging import NotificationHandler

start_time = time()


def duration_human(seconds):
    seconds = int(round(seconds))
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    years, days = divmod(days, 365.242199)

    minutes = int(minutes)
    hours = int(hours)
    days = int(days)
    years = int(years)

    duration = []
    if years > 0:
        duration.append('%d year' % years + 's' * (years != 1))
    else:
        if days > 0:
            duration.append('%d day' % days + 's' * (days != 1))
        if hours > 0:
            duration.append('%d hour' % hours + 's' * (hours != 1))
        if minutes > 0:
            duration.append('%d minute' % minutes + 's' * (minutes != 1))
        if seconds > 0:
            duration.append('%d second' % seconds + 's' * (seconds != 1))
    return ' '.join(duration)


@group()
@version_option()
def main():
    pass


@main.command('added')
@argument('torrent_id')
@argument('torrent_name')
@argument('torrent_path')
@option('--log-level',
        type=CHOICE(['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'SUCCESS', 'TRACE'],
                    case_sensitive=False),
        envvar='LOG_LEVEL',
        default='DEBUG')
@option('--slack-message',
        type=STRING,
        envvar='SLACK_MESSAGE',
        default='Torrent {event} with ID "{id}", name "{name}", path "{path}"')
@option('--slack-webhook',
        type=STRING,
        envvar='SLACK_WEBHOOK',
        default=None)
@option('--slack-username',
        type=STRING,
        envvar='SLACK_USERNAME',
        default='Deluge')
@option('--slack-format',
        type=STRING,
        envvar='SLACK_FORMAT',
        default='{message}')
@option('--slack-log-level',
        type=CHOICE(['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'SUCCESS', 'TRACE'],
                    case_sensitive=False),
        envvar='SLACK_LOG_LEVEL',
        default='SUCCESS')
def added(**kwargs):
    event("Added", **kwargs)


@main.command('complete')
@argument('torrent_id')
@argument('torrent_name')
@argument('torrent_path')
@option('--log-level',
        type=CHOICE(['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'SUCCESS', 'TRACE'],
                    case_sensitive=False),
        envvar='LOG_LEVEL',
        default='DEBUG')
@option('--slack-message',
        type=STRING,
        envvar='SLACK_MESSAGE',
        default='Torrent {event} with ID "{id}", name "{name}", path "{path}"')
@option('--slack-webhook',
        type=STRING,
        envvar='SLACK_WEBHOOK',
        default=None)
@option('--slack-username',
        type=STRING,
        envvar='SLACK_USERNAME',
        default='Deluge')
@option('--slack-format',
        type=STRING,
        envvar='SLACK_FORMAT',
        default='{message}')
@option('--slack-log-level',
        type=CHOICE(['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'SUCCESS', 'TRACE'],
                    case_sensitive=False),
        envvar='SLACK_LOG_LEVEL',
        default='SUCCESS')
def complete(**kwargs):
    event("Complete", **kwargs)


def event(event, torrent_id, torrent_name, torrent_path, log_level, slack_message, slack_webhook, slack_username, slack_format, slack_log_level):
    logger.remove()
    logger.add(stderr, level=log_level)

    if slack_webhook:
        params = {
            "username": slack_username,
            "webhook_url": slack_webhook
        }
        slack = NotificationHandler("slack", defaults=params)
        logger.add(slack, format=slack_format, level=slack_log_level)

    logger.info('{} Started with Event "{}", Torrent ID "{}", Torrent Name "{}", Torrent Path "{}"',
                basename(argv[0]),
                event,
                torrent_id,
                torrent_name,
                torrent_path)
    logger.info('  --log-level "{}"', log_level)
    logger.info('  --slack-webhook "{}"', slack_webhook)
    logger.info('  --slack-username "{}"', slack_username)
    logger.info('  --slack-format "{}"', slack_format)

    try:
        logger.success(slack_message,
                       event=event,
                       id=torrent_id,
                       name=torrent_name,
                       path=torrent_path)
        pass
    finally:
        lwt()


def lwt():
    logger.info('{} Exiting after {}', basename(argv[0]), duration_human(time() - start_time))


if __name__ == "__main__":
    atexit_register(lwt)
    main()
