from settings import SEASON_EPISODE_REGEX, SEASON_EPISODE_REGEX_EXTRAS
from regexes import SERIES_REGEXES
import askuser


def getepisodeinfo(txt):
    res = SEASON_EPISODE_REGEX.search(txt)
    if res is not None:
        ep = _regex(res)
        return ep[0], ep[1]

    regexmatches = []
    for regex in SEASON_EPISODE_REGEX_EXTRAS:
        res = regex.search(txt)
        if res is None:
            continue
        ep = _regex(res)
        epinfo = "S{}E{}".format(ep[0], ep[1])
        regexmatches.append((epinfo, res))
    if regexmatches == []:
        print "Couldn't find episode information!"
        return None, None

    option = askuser.multipleoptions("Which episode numbering is correct? ({})".format(txt),
                                     regexmatches, lambda x: x[0])
    if option is None:
        return None, None
    ep = _regex(option[1])
    return ep[0], ep[1]


def getshowname(txt):
    matches = _findshowmatches(txt)
    if len(matches) == 1:
        match = matches[0]
    elif len(matches) > 1:
        question = "\nWhich show does \"{}\" belong to?".format(txt)
        match = askuser.multipleoptions(question, matches, lambda x: x.showname)
    else:
        match = None
    return match.showname


def _findshowmatches(txt):
    matches = []
    for regex in SERIES_REGEXES:
        if regex.regex.search(txt):
            matches.append(regex)
    return matches


def _regex(match):
    """ Return tuple of zero-filled season and episode numbers.
    """
    return (match.group('season').zfill(2), match.group('episode').zfill(2))
