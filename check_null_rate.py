from load_clean import load_clean

markets = load_clean()
n_valid = sum(1 for m in markets if m.get('bn_delta_final') is not None)
print(f'bn_delta_final populated: {n_valid}/{len(markets)} ({100*n_valid/len(markets):.1f}%)')
