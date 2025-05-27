# Produtiv

Produtiv: Assessing Microbial Impact on Garlic Yield via Weighted Abundance Metrics

The produtiv software is a Python-based tool designed to identify microbial taxa whose abundance changes are most strongly associated with garlic yield across multiple farms. It integrates relative abundance data of soil bacteria collected before and after cultivation with crop yield data from four farms with varying soil types and management practices.

The algorithm operates in three primary steps:

Compute Abundance Variation: For each bacterial species, the program calculates the relative abundance change (Δ_ij) between post- and pre-cultivation samples at each farm i.

Normalize Productivity: Each farm's yield Y_i is normalized by the mean yield Ȳ across all farms, producing a productivity factor P_i:

  P_i = Y_i / Ȳ

Calculate Productivity-Weighted Score (PWS): For each species j, the productivity-weighted score is computed by aggregating its abundance changes across all farms where it was detected, weighted by the respective productivity factors:

  PWS_j = (Σ_i Δ_ij × P_i) / Σ_i P_i

  Where Δ_ij is the relative abundance variation of species j in farm i, and P_i is the productivity factor of farm i.

Species with high positive scores are considered potentially beneficial to garlic productivity, whereas negative scores suggest taxa associated with yield declines. This approach enables the identification of microbial indicators or drivers of productivity under real-world agricultural conditions.

The tool outputs a ranked table of species with their corresponding PWS, classification of impact (high/medium/low positive or negative), and full metadata. It also generates a statistical summary highlighting the most impactful taxa and trends across farms.

## How to Use
