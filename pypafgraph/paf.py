from typing import NamedTuple
from typing import Sequence, Iterator, List

from intervaltree import Interval


class PAF(NamedTuple):

    query: str
    qlen: int
    qstart: int
    qend: int
    strand: str
    target: str
    tlen: int
    tstart: int
    tend: int
    nmatch: int
    alilen: int
    mq: int
    attrs: List[str]

    @staticmethod
    def columns() -> List[str]:
        return [
            "query",
            "qlen",
            "qstart",
            "qend",
            "strand",
            "target",
            "tlen",
            "tstart",
            "tend",
            "nmatch",
            "alilen",
            "mq",
        ]

    @classmethod
    def parse(cls, line: str) -> 'PAF':
        sline = line.strip().split("\t")
        if len(sline) < len(cls.columns()):
            raise AssertionError(f"Wrong number of columns {line}")

        dline = dict(zip(cls.columns(), sline))
        qlen = int(dline["qlen"])
        qstart = int(dline["qstart"])
        qend = int(dline["qend"])
        tlen = int(dline["tlen"])
        tstart = int(dline["tstart"])
        tend = int(dline["tend"])
        nmatch = int(dline["nmatch"])
        alilen = int(dline["alilen"])
        mq = int(dline["mq"])
        attrs = sline[len(cls.columns()):]
        return cls(dline["query"], qlen, qstart, qend, dline["strand"],
                   dline["target"], tlen, tstart, tend, nmatch, alilen,
                   mq, attrs)

    @classmethod
    def from_file(cls, handle: Sequence[str]) -> Iterator['PAF']:
        for line in handle:
            yield cls.parse(line)
        return

    def __str__(self) -> str:
        line = [str(getattr(self, c)) for c in self.columns()]
        line.extend(self.attrs)
        return "\t".join(line)

    def query_as_interval(self) -> Interval:
        start = min([self.qstart, self.qend])
        end = max([self.qstart, self.qend])
        return self.query, Interval(start, end)

    def target_as_interval(self) -> Interval:
        start = min([self.tstart, self.tend])
        end = max([self.tstart, self.tend])
        return self.target, Interval(start, end)
