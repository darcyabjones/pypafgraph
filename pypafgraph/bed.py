from typing import NamedTuple
from typing import List, Sequence, Iterator, Iterable
from typing import Tuple
from typing import Dict

from collections import defaultdict

from intervaltree import Interval, IntervalTree


class BED(NamedTuple):

    seqid: str
    start: int
    end: int

    def __str__(self) -> str:
        return f"{self.seqid}\t{self.start}\t{self.end}"

    @classmethod
    def parse(cls, line: str) -> 'BED':
        sline = line.strip().split("\t")
        return cls(sline[0], int(sline[1]), int(sline[2]))

    @classmethod
    def from_file(cls, handle: Sequence[str]) -> Iterator['BED']:
        for line in handle:
            yield cls.parse(line)
        return

    def as_interval(self) -> Tuple[str, Interval]:
        return self.seqid, Interval(self.start, self.end)


def bed_to_itree(beds: Iterable[BED]) -> IntervalTree:
    intervals: Dict[str, List[Interval]] = defaultdict(list)

    for record in beds:
        seqid, interval = record.as_interval()
        intervals[seqid].append(interval)

    itree = {s: IntervalTree(i) for s, i in intervals.items()}

    for it in itree.values():
        it.merge_overlaps()
    return itree
