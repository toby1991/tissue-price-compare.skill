---
name: tissue-price-compare
description: Compare Chinese boxed facial tissue / 抽纸 deals against User's saved best-buy baseline. Use when a user asks whether 抽纸, 纸巾, facial tissue, or tissue box parameters are 划算/便宜/值得买, especially with specs like 层数、抽数、包数、箱数、价格, or when maintaining User's tissue price baseline.
---

# Tissue Price Compare

## Baseline

Use User's current best-buy baseline unless the user explicitly updates it:

- ¥29.34 per box
- 24 packs
- 3 layers
- 110 sheets/draws per pack
- Baseline pack price: `29.34 / 24 = ¥1.2225/包`
- Baseline draw price: `29.34 / 24 / 110 = ¥0.0111136/抽`

Treat layer count, sheet/draw count, pack count, sheet size, and brand as important quality dimensions. Do not ignore layer count.

## Quick Workflow

1. Parse the offer:
   - layers = `N层`
   - draws per pack = `N抽`
   - pack count = `N包`; if `24包*3`, total packs is usually `72包`, but verify whether the price is total price or per-box price when ambiguous.
   - price = final paid price after coupons/subsidies.
2. Calculate:
   - `单包价 = price / total_packs`
   - `单抽价 = price / total_packs / draws_per_pack`
   - `合理价 = baseline_draw_price * total_packs * draws_per_pack` for same-layer comparison.
   - `差异百分比 = (offer_draw_price / baseline_draw_price - 1) * 100`
3. Decide:
   - `<= baseline`: 划算 / 可以买.
   - `0% to +3%`: 小幅偏贵；只有尺寸/品牌更好才买.
   - `> +3%`: 不划算，跳过.
   - `< -5%`: 明显划算.
   - `< -15%`: 非常划算，优先买, but still warn about size/brand缩水.
4. If layers differ from the 3-layer baseline:
   - Mention the mismatch clearly.
   - Prefer comparing only against same layer count.
   - If forced, give a rough normalized estimate but mark it as rough, not a clean verdict.
5. If dimensions/brand are unknown:
   - Give the price verdict first.
   - Add: “只要尺寸/品牌没缩水”.

## Response Style

Reply in concise Chinese. For Discord, do not use markdown tables.

Recommended format:

```text
不划算/划算。

这款：价格 ÷ 包数 ÷ 抽数 = ¥X/抽
基准：¥0.01111/抽

贵/便宜约 Y%。按基准折算，合理价约 ¥Z；除非尺寸/品牌更好，否则跳过。
```

When the user gives a bundle with ambiguous multiplication/pricing, stop and ask one clarification, or show both scenarios if easy:

```text
这里有歧义：39.98 是 3箱合计价，还是每箱单价？
如果是合计价：...
如果是单箱价：...
```

## Deterministic Calculator

Use `scripts/compare_tissue.py` when there are multiple items, ambiguous arithmetic, or you want to avoid mental math errors.

Examples:

```bash
python3 skills/tissue-price-compare/scripts/compare_tissue.py --layers 3 --draws 150 --packs 40 --price 69.91
python3 skills/tissue-price-compare/scripts/compare_tissue.py --item "3,110,40,48.16" --item "3,150,40,69.91"
```
