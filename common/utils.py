import os
import sys
import time
import codecs
import contextlib
import numpy
from collections import deque


class Logger(object):
    """ Convenient double logger that redirects `stdout` and save the output also to the file """
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = codecs.open(filename, "wb", encoding="utf8")

    def write(self, message, terminal=True, log=True):
        if terminal:
            self.terminal.write(message)
        if log:
            self.log.write(message)

    def __del__(self):
        if sys:
            sys.stdout = self.terminal

    def __getattr__(self, attr):
        return getattr(self.terminal, attr)


class Throttler(object):
    def __init__(self, rate):
        self.clock = time.time()
        self.rate = rate
        self.output = True

    def update(self):
        curr_time = time.time()

        if curr_time - self.clock < self.rate:
            self.output = False
            return False

        self.clock = curr_time
        self.output = True
        return True


class ring_deque(deque):
    """ Circular deque implementation """

    max = 0
    min = 0

    def __init__(self, data, length):
        self.length = length
        super(ring_deque, self).__init__(data)

    def append_more(self, data):

        if len(self) > self.length:
            self.popleft()

        self.max = max(data, self.max)
        self.min = min(data, self.min)
        super(ring_deque, self).append(data)

    def append(self, data):
        self.max = data
        self.min = data

        self.append = self.append_more

        super(ring_deque, self).append(data)


class benchmark(object):
    """ Simple benchmarking context manager """
    def __init__(self, name, show=True):
        self.name = name
        self.show = show

    def __enter__(self):
        if self.show:
            self.start = time.time()

    def __exit__(self, ty, val, tb):
        if self.show:
            end = time.time()
            print("{:s} : {:0.3f} seconds \n"
                  .format(self.name if not callable(self.name) else self.name(), end-self.start))
        return False


@contextlib.contextmanager
def printoptions(*args, **kwargs):
    original = numpy.get_printoptions()
    numpy.set_printoptions(*args, **kwargs)
    yield
    numpy.set_printoptions(**original)


def getenv(var, default=None):
    return os.getenv(var, default)


def getboolenv(var, default=None):
    value = getenv(var, default)
    return (value is not False and value is not None and value not in ['false', 'f', '0', '-1'])


def ensure_path(*chunks):
    path = os.path.join(*chunks)
    dir = os.path.dirname(path)
    ensure_dir(dir)
    return path


def ensure_dir(*chunks):
    dir = os.path.join(*chunks)
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir


class reaction_type(object):
    def __init__(self, interaction):
        self.sumsides = sum([item.side for item in interaction.reaction])
    @property
    def CREATION(self):
        if self.sumsides in [-1, -2]:
            return True
        return False
    @property
    def SCATTERING(self):
        if self.sumsides in [0]:
            return True
        return False
    @property
    def DECAY(self):
        if self.sumsides in [1, 2]:
            return True
        return False


def interaction_filter(names, interaction, first_only=True, reaction_type=[None]):
    for inter in interaction:
        if first_only:
            inter.integrals = [integral for integral in inter.integrals
                            if integral.reaction[0].specie.name not in names\
                            and sum([item.side for item in integral.reaction]) not in reaction_type]
        else:
            inter.integrals = [integral for integral in inter.integrals
                            if all(item.specie.name not in names for item in integral.reaction)\
                            and sum([item.side for item in integral.reaction]) not in reaction_type]
    return interaction


def particle_filter(names, particles):
    particles = [particle for particle in particles if particle.name not in names]
    return particles


def particle_orderer(particles):
    particles = [part for (mass, part) in
                sorted(zip([particle.mass for particle in particles], particles), reverse=True)]
    return particles


class Dynamic2DArray(object):
    def __init__(self, header):
        self.header = header

        self.length = 0
        self.size = 10
        self._data = numpy.zeros((self.size, len(self.header)))

    def __len__(self):
        return self.length

    def __getitem__(self, index):
        return self._data[:self.length][index]
        # if isinstance(index, Iterable):
        #     index = list(index)
        #     if index[0] < 0:
        #         index[0] = self.length+1-index[0]
        #     elif isinstance(index[0], slice):
        #         index[0] = slice(*index[0].indices(self.length))
        # elif isinstance(index, slice):
        #     index = slice(*index.indices(self.length))
        # elif index < 0:
        #     index = self.length+1-index
        # return self._data[index]

    def append(self, row):
        if self.length == self.size or self.length == len(self._data) - 2:
            self.size = int(1.5*self.size)
            self._data = numpy.resize(self._data, (self.size, len(self.header)))
        self._data[self.length][:] = row
        self.length += 1

    def extend(self, rows):
        for row in rows:
            self.append(row)

    @property
    def data(self):
        return self._data[:self.length]

    def truncate(self):
        self._data = numpy.delete(self._data, self.length + 1, axis=0)
        self.length -= 1

    def savetxt(self, f):
        numpy.savetxt(f, self.data, delimiter='\t',
                      header='\t'.join(['{:e}'.format(h) for h in self.header]))


class DynamicRecArray(object):
    def __init__(self, columns, dtypes=None):
        if dtypes is None:
            dtypes = [float] * len(columns)

        self.columns = [column[0] for column in columns]

        self.dtypes = dtypes
        self.structure = list(zip(self.columns, self.dtypes))

        self.unit_names = [column[1] for column in columns]
        self.units = numpy.array([column[2] for column in columns])

        self.length = 0
        self.size = 10
        self._data = numpy.zeros(self.size, dtype=self.structure)

    def __len__(self):
        return self.length

    # Unfortunately, this method causes infinite recursion with multiprocessing
    # def __getattr__(self, column):
    #     if column in self.__dict__:
    #         return self.__dict__[column]
    #     if column in self.columns:
    #         return self._data[column][:self.length]
    #     else:
    #         raise KeyError

    def __getitem__(self, index):
        if index in self.columns:
            return self._data[index][:self.length]
        index = int(index)
        if index < 0:
            index = self.length+1-index
        return self._data[:][index]

    def append(self, rec):
        if isinstance(rec, dict):
            rec = tuple(rec[column] for column in self.columns)

        if self.length == self.size or self.length == len(self._data) - 2:
            self.size = int(1.5*self.size)
            self._data = numpy.resize(self._data, self.size)
        self._data[self.length] = rec
        self.length += 1

    def extend(self, recs):
        for rec in recs:
            self.append(rec)

    @property
    def data(self):
        return self._data[:self.length]

    def row_repr(self, index, names=False):
        row = self.data[index]
        if names:
            heading = [
                '{} = {:.2e}'.format(name, row[name] / unit)
                + (' ' + unit_name if unit_name else '')
                for name, unit_name, unit in zip(self.columns, self.unit_names, self.units)
            ]
        else:
            heading = [
                '{:e}'.format(row[name] / unit)
                for name, unit_name, unit in zip(self.columns, self.unit_names, self.units)
            ]
        return '\t'.join(heading)

    def truncate(self):
        self._data = numpy.delete(self._data, self.length + 1, axis=0)
        self.length -= 1

    def savetxt(self, f):
        heading = [
            name + (', ' + unit if unit else '')
            for name, unit in zip(self.columns, self.unit_names)
        ]

        numpy.savetxt(
            f,
            self.data.view((numpy.float_, len(self._data.dtype))) / self.units[None, :],
            delimiter='\t', header='\t'.join(heading)
        )
