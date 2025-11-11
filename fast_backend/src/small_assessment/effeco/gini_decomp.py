import pandas as pd
import numpy as np

def gini(x, w=None):
    if w is None:
        w = np.ones_like(x)
    
    # Remove missing values
    valid = ~(np.isnan(x) | np.isnan(w))
    x, w = x[valid], w[valid]
    
    if np.any(w < 0):
        raise ValueError("At least one weight is negative")
    if np.all(w == 0):
        raise ValueError("All weights are zero")
    
    # Normalize weights
    w = w / np.sum(w)
    
    # Sort values and weights
    order = np.argsort(x)
    x, w = x[order], w[order]
    
    # Cumulative sums
    p = np.cumsum(w)
    nu = np.cumsum(w * x)
    nu /= nu[-1]
    
    # Gini calculation
    gini = np.sum(nu[1:] * p[:-1]) - np.sum(nu[:-1] * p[1:])
    return float(gini)

def gini_decomp(x, z, w=None):
    """

    Args:
        x:
        z:
        w:

    Returns:

    """
    if w is None:
        w = np.ones_like(x)
    
    z = pd.factorize(z)[0]
    df = pd.DataFrame({'x': np.array(x, dtype=float), 'z': z, 'w': np.array(w, dtype=float)})
    df = df.dropna()
    
    # Group splitting
    df_split = {key: df[df['z'] == key] for key in df['z'].unique()}
    n_group = df.groupby('z')['w'].sum()
    
    # Means
    x_mean = float(np.average(df['x'], weights=df['w']))
    x_mean_group = {int(key): float(np.average(df_split[key]['x'], weights=df_split[key]['w'])) for key in df_split}
    share_group = {int(key): float(df_split[key]['w'].sum() / df['w'].sum()) for key in df_split}
    share_group_income = {int(key): float(share_group[key] * x_mean_group[key] / x_mean) for key in df_split}
    
    # Gini calculations
    gini_total = gini(df['x'].values, df['w'].values)
    gini_group = {int(key): gini(df_split[key]['x'].values, df_split[key]['w'].values) for key in df_split}
    gini_group_contribution = {int(key): gini_group[key] * share_group[key] * share_group_income[key] for key in df_split}
    gini_within = sum(gini_group_contribution.values())
    gini_between = gini(np.array(list(x_mean_group.values())), n_group.values)
    gini_overlap = gini_total - gini_within - gini_between
    
    return {
        'gini_decomp': {
            'gini_total': float(gini_total),
            'gini_within': float(gini_within),
            'gini_between': float(gini_between),
            'gini_overlap': float(gini_overlap)
        },
        'gini_group': {
            'gini_group': gini_group,
            'gini_group_contribution': gini_group_contribution
        },
        'mean': {
            'mean_total': x_mean,
            'mean_group': x_mean_group
        },
        'share_groups': share_group,
        'share_income_groups': share_group_income,
        'number_cases': {
            'n_weighted': float(df['w'].sum()),
            'n_group_weighted': list(n_group)
        }
    }
