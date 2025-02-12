# calculate Index of Coincidence (IC)
def calc_ic(text):
    freqs = {}
    for c in text:
        if c in freqs:
            freqs[c] += 1
        else:
            freqs[c] = 1

    n = len(text)
    ic = sum(f * (f - 1) for f in freqs.values()) / (n * (n - 1))
    return ic

# estimate key length using Friedman-Test
def est_key_len(text, max_key_len):
    ics = []
    for key_len in range(1, max_key_len + 1):
        subgroups = [''.join(text[i::key_len]) for i in range(key_len)]

        ic_values = [calc_ic(sub) for sub in subgroups if len(sub) > 1]
        if ic_values:
            avg_ic = sum(ic_values) / len(ic_values)
            ics.append((key_len, avg_ic))
    
    return sorted(ics, key=lambda x: -x[1])[0][0]