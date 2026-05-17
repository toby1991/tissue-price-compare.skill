#!/usr/bin/env python3
"""Compare facial tissue deals against User's saved baseline."""

from __future__ import annotations

import argparse
from dataclasses import dataclass

BASELINE_PRICE = 29.34
BASELINE_PACKS = 24
BASELINE_LAYERS = 3
BASELINE_DRAWS = 110
BASELINE_PER_PACK = BASELINE_PRICE / BASELINE_PACKS
BASELINE_PER_DRAW = BASELINE_PRICE / BASELINE_PACKS / BASELINE_DRAWS


@dataclass
class Offer:
    layers: int
    draws: int
    packs: int
    price: float
    name: str = "这款"

    @property
    def per_pack(self) -> float:
        return self.price / self.packs

    @property
    def per_draw(self) -> float:
        return self.price / self.packs / self.draws

    @property
    def fair_price(self) -> float:
        return BASELINE_PER_DRAW * self.packs * self.draws

    @property
    def diff_pct(self) -> float:
        return (self.per_draw / BASELINE_PER_DRAW - 1) * 100


def verdict(diff_pct: float) -> str:
    if diff_pct <= -15:
        return "非常划算，优先买"
    if diff_pct <= -5:
        return "明显划算，可以买"
    if diff_pct <= 0:
        return "小幅划算，可以买"
    if diff_pct <= 3:
        return "基本持平/小幅偏贵，尺寸或品牌更好才买"
    return "不划算，跳过"


def parse_item(raw: str) -> Offer:
    """Parse layers,draws,packs,price[,name]."""
    parts = [p.strip() for p in raw.split(",")]
    if len(parts) not in (4, 5):
        raise argparse.ArgumentTypeError("--item format: layers,draws,packs,price[,name]")
    layers = int(parts[0])
    draws = int(parts[1])
    packs = int(parts[2])
    price = float(parts[3])
    name = parts[4] if len(parts) == 5 and parts[4] else "这款"
    return Offer(layers=layers, draws=draws, packs=packs, price=price, name=name)


def render(o: Offer) -> str:
    diff = o.diff_pct
    direction = "便宜" if diff < 0 else "贵"
    layer_note = ""
    if o.layers != BASELINE_LAYERS:
        layer_note = f"\n注意：层数是{o.layers}层，基准是{BASELINE_LAYERS}层；这个结论不是完全同规格对比。"
    return (
        f"{o.name}：{verdict(diff)}。\n\n"
        f"计算：{o.price:.2f} ÷ {o.packs} ÷ {o.draws} = ¥{o.per_draw:.5f}/抽\n"
        f"单包：¥{o.per_pack:.3f}/包\n"
        f"基准：¥{BASELINE_PER_DRAW:.5f}/抽，¥{BASELINE_PER_PACK:.3f}/包\n\n"
        f"比基准{direction}约 {abs(diff):.1f}%。"
        f"按基准折算，合理价约 ¥{o.fair_price:.2f}。"
        f"{layer_note}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--layers", type=int, help="Layer count, e.g. 3")
    parser.add_argument("--draws", type=int, help="Draws/sheets per pack, e.g. 110")
    parser.add_argument("--packs", type=int, help="Total pack count, e.g. 24")
    parser.add_argument("--price", type=float, help="Final price, e.g. 29.34")
    parser.add_argument("--name", default="这款", help="Offer label")
    parser.add_argument(
        "--item",
        action="append",
        type=parse_item,
        help="Compare one item as layers,draws,packs,price[,name]. May repeat.",
    )
    args = parser.parse_args()

    offers = args.item or []
    direct_fields = (args.layers, args.draws, args.packs, args.price)
    if any(v is not None for v in direct_fields):
        if not all(v is not None for v in direct_fields):
            parser.error("--layers, --draws, --packs, and --price must be provided together")
        offers.append(Offer(args.layers, args.draws, args.packs, args.price, args.name))

    if not offers:
        parser.error("provide --item or --layers/--draws/--packs/--price")

    print("\n\n---\n\n".join(render(o) for o in offers))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
