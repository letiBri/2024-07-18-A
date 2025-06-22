from dataclasses import dataclass

from model.gene import Gene


@dataclass
class Arco:
    Gene1: Gene
    Chrom1: int
    Gene2: Gene
    Chrom2: int
    peso: float
