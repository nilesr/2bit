# This is directly copy pasted from pip
# https://github.com/pypa/pip/blob/master/pip/_vendor/progress/bar.py
# I take no credit
#


#
from time import time
HIDE_CURSOR = '\x1b[?25l'
SHOW_CURSOR = '\x1b[?25h'
from collections import deque
class WritelnMixin(object):
    hide_cursor = False

    def __init__(self, message=None, **kwargs):
        super(WritelnMixin, self).__init__(**kwargs)
        if message:
            self.message = message

        if self.file.isatty() and self.hide_cursor:
            print(HIDE_CURSOR, end='', file=self.file)

    def clearln(self):
        if self.file.isatty():
            print('\r\x1b[K', end='', file=self.file)

    def writeln(self, line):
        if self.file.isatty():
            self.clearln()
            print(line, end='', file=self.file)
            self.file.flush()

    def finish(self):
        if self.file.isatty():
            print(file=self.file)
            if self.hide_cursor:
                print(SHOW_CURSOR, end='', file=self.file)
class Infinite(object):
    import sys
    file = sys.stderr
    sma_window = 10

    def __init__(self, *args, **kwargs):
        self.index = 0
        self.start_ts = time()
        self._ts = self.start_ts
        self._dt = deque(maxlen=self.sma_window)
        for key, val in kwargs.items():
            setattr(self, key, val)

    def __getitem__(self, key):
        if key.startswith('_'):
            return None
        return getattr(self, key, None)

    @property
    def avg(self):
        return sum(self._dt) / len(self._dt) if self._dt else 0

    @property
    def elapsed(self):
        return int(time() - self.start_ts)

    @property
    def elapsed_td(self):
        return timedelta(seconds=self.elapsed)

    def update(self):
        pass

    def start(self):
        pass

    def finish(self):
        pass

    def next(self, n=1):
        if n > 0:
            now = time()
            dt = (now - self._ts) / n
            self._dt.append(dt)
            self._ts = now

        self.index = self.index + n
        self.update()

    def iter(self, it):
        for x in it:
            yield x
            self.next()
        self.finish()

class Progress(Infinite):
    def __init__(self, *args, **kwargs):
        super(Progress, self).__init__(*args, **kwargs)
        self.max = kwargs.get('max', 100)

    @property
    def eta(self):
        return int(ceil(self.avg * self.remaining))

    @property
    def eta_td(self):
        return timedelta(seconds=self.eta)

    @property
    def percent(self):
        return self.progress * 100

    @property
    def progress(self):
        return min(1, self.index / self.max)

    @property
    def remaining(self):
        return max(self.max - self.index, 0)

    def start(self):
        self.update()

    def goto(self, index):
        incr = index - self.index
        self.next(incr)

    def iter(self, it):
        try:
            self.max = len(it)
        except TypeError:
            pass

        for x in it:
            yield x
            self.next()
        self.finish()
class Bar(WritelnMixin, Progress):
    width = 32
    message = ''
    suffix = '%(index)d/%(max)d'
    bar_prefix = ' |'
    bar_suffix = '| '
    empty_fill = ' '
    fill = '#'
    hide_cursor = True
class IncrementalBar(Bar):
    phases = (u' ', u'▏', u'▎', u'▍', u'▌', u'▋', u'▊', u'▉', u'█')

    def update(self):
        nphases = len(self.phases)
        expanded_length = int(nphases * self.width * self.progress)
        filled_length = int(self.width * self.progress)
        empty_length = self.width - filled_length
        phase = expanded_length - (filled_length * nphases)

        message = self.message % self
        bar = self.phases[-1] * filled_length
        current = self.phases[phase] if phase > 0 else ''
        empty = self.empty_fill * max(0, empty_length - len(current))
        suffix = self.suffix % self
        line = ''.join([message, self.bar_prefix, bar, current, empty,
                        self.bar_suffix, suffix])
        self.writeln(line)
