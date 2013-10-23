#!/usr/bin/python
"""Series everything

Usage:
    serieseverything.py <showname>... --watch-next
    serieseverything.py <showname>... --update
    serieseverything.py <showname>... --watch <episode>
    serieseverything.py <showname>... --next-episode
    serieseverything.py <showname>... --list
    serieseverything.py <showname>... --mark-watched <episode> [--mark-previous]
    serieseverything.py <showname>... --mark-unwatched <episode> [--mark-previous]
    serieseverything.py <showname>... --download <episode>
    serieseverything.py <showname>... --download-next <number>
    serieseverything.py --rename <filename>
    serieseverything.py --new-episodes

Options:
    -h --help                     Show this screen.
    --watch-next                  Watch next episode.
    --watch <episode>             Watch specific episode (e.g. s01e05).
    --next-episode                Display next episode's information, e.g. 's01e05 - title (release date)'.
    --mark-watched <episode>      Episode info (e.g. s01e05). See mark-previous option.
    --mark-unwatched <episode>    Episode info (e.g. s01e05). See mark-previous option.
    --mark-previous               Mark all previous episodes watched as well as the one specified [default: False].
    --download <episode>          Download episode (e.g. s01e05).
    --download-next               Download episode (e.g. s01e05) [default: 1].
    --update                      Force an update of the series cache.
    --new-episodes                List recently aired, unwatched episodes.
    --rename <filename>           Rename file [default: 'all'].
"""

from datetime import datetime
from os import listdir

from docopt import docopt

from utils.serieswatcher import watchepisode
from utils.seriesnamehandler import getepisodeinfo, getshowname
from utils.seriescache import SeriesCache
from utils.seriesdownloader import downloadepisode
from utils.seriesrenamer import renameepisode
from settings.settings import AIR_DATE_FORMAT


def main(args):
    cache = SeriesCache()
    if args.get('<showname>', False):
        showname = getshowname(" ".join(args['<showname>']))
    if args.get('--watch-next', False):
        watchnext(showname, cache)
    elif args.get('--watch', False):
        watch(showname, cache, args['--watch'])
    elif args.get('--next-episode', False):
        nextepisode(showname, cache)
    elif args.get('--mark-watched', False):
        markwatched(showname, cache, args['--mark-watched'], watched=True,
                    markprevious=args.get('--mark-previous', False))
    elif args.get('--mark-unwatched', False):
        markwatched(showname, cache, args['--mark-unwatched'], watched=False,
                    markprevious=args.get('--mark-previous', False))
    elif args.get('--download', False):
        download(showname, cache)
    elif args.get('--update', False):
        update(showname, cache)
    elif args.get('--rename', False):
        rename(cache, args['--rename'])
    else:
        print('Unimplemented/unknown arguments! {}'.format(args))


def watchnext(showname, cache):
    episode = cache.getnextepisode(showname)
    if watchepisode(episode):
        cache.markwatched(episode)


def watch(showname, cache, episodestring):
    seasonnum, episodenum = getepisodeinfo(episodestring)
    episode = cache.getepisode(showname, seasonnum, episodenum)
    if watchepisode(episode):
        cache.markwatched(episode)


def nextepisode(showname, cache):
    episode = cache.getnextepisode(showname)
    print u"Next episode is: {} ({}): {}".format(episode.getprettyname(),
                                                 datetime.strftime(episode.airdate, AIR_DATE_FORMAT),
                                                 episode.description).encode('utf8')


def markwatched(showname, cache, episodestring, markprevious, watched):
    seasonnum, episodenum = getepisodeinfo(episodestring)
    episode = cache.getepisode(showname, seasonnum, episodenum)
    cache.markwatched(episode, markprevious=markprevious, watched=watched)


def download(showname, cache):
    seasonnum, episodenum = getepisodeinfo(args['--download'])
    episode = cache.getepisode(showname, seasonnum, episodenum)
    downloadepisode(episode)


def rename(cache, filename):
    if filename == 'all':
        renameepisode(listdir('.'), cache=cache)
    else:
        renameepisode([filename], cache=cache)


def update(showname, cache):
    cache.getshow(showname, update=True)


if __name__ == '__main__':
    args = docopt(__doc__, version='Series everything v 0.1')
    main(args)
