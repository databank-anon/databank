import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np

plt.rcParams.update({'text.usetex': True,
                     'font.family': 'serif',
                     'font.serif': 'Times',
                     'font.size': 18,
                     'savefig.dpi': 600})

LOG = "log.json"
M = 50

with open(LOG, 'r') as f:
    js = json.load(f)

n_events = [0, 25, 50, 100, 250, 500]
u_users    = [2, 10, 50, 100, 500]
p_policies = [0, 1, 2]
#modes = ['active', 'passive', 'flask']
modes = ['active', 'flask']
#mode_labels = ['D', 'P', 'F']
mode_labels = ['D', 'F']
workloads = ['insert', 'delete', 'view', 'list', 'list_paginated', 'invite']

counts = {}

columns = ['n', 'mode', 'workload', 'total', 'database', 'monitoring']
df = pd.DataFrame(columns=columns)

MODE_MAPPING = {'active': 'databank (labels on)',
#                'passive': 'databank (labels off)',
                'flask': 'Python/Flask'}

for row in js:
    k = row["n_events"], MODE_MAPPING[row["mode"]], row["workload"], row["u"], row["p"]
    if row["n_events"] == 10:
        continue
    if k not in counts:
        counts[k] = 0
    counts[k] += 1
    if 'm2' in row:
        m2 = row['m2']
    else:
        m2 = 1
    series = pd.Series({'n': row["n_events"],
                        'u': row["u"],
                        'p': row["p"],
                        'mode': MODE_MAPPING[row["mode"]],
                        'workload': row["workload"],
                        'm2': m2,
                        'total': row["total_time"] / m2})
    if 'database_time' in row:
        series['database'] = row["database_time"] / m2
    if 'monitoring_time' in row:
        series['monitoring'] = row["monitoring_time"] / m2
    df = df.append(series, ignore_index=True)

df_new = pd.DataFrame(columns=columns)

for (k, c) in counts.items():
    n, mode, workload, u, p = k
    sub_df = df[(df["n"] == n) & (df["mode"] == mode) & (df["workload"] == workload) & (df["u"] == u) & (df["p"] == p)].sort_values('total')
    print(k, c)
    s = max(0, (c-M)//2)
    sub_df = sub_df.iloc[s:s+M]
    df_new = pd.concat([sub_df, df_new], ignore_index=True)

df = df_new

df.to_csv('test.csv')

df = df.fillna(0)

df["other"] = df["total"] - df["monitoring"] - df["database"]

W = 0.2
offsets = [W/2, -W/2]#[W, 0, -W]
colors = ["lightsteelblue", "cornflowerblue", "navy"]
color_f = "black"

# Function of n

def show_costs(df_w, groupby='n'):
    df = pd.DataFrame()
    df["d"] = df_w[df_w["mode"] == "databank (labels on)"].groupby(groupby)["total"].mean()
    df["p"] = df_w[df_w["mode"] == "databank (labels off)"].groupby(groupby)["total"].mean()
    df["f"] = df_w[df_w["mode"] == "Python/Flask"].groupby(groupby)["total"].mean()
    df["d/f"] = df_w[df_w["mode"] == "databank (labels on)"].groupby(groupby)["total"].mean() / df_w[df_w["mode"] == "Python/Flask"].groupby(groupby)["total"].mean()
    df["d/p"] = df_w[df_w["mode"] == "databank (labels on)"].groupby(groupby)["total"].mean() / df_w[df_w["mode"] == "databank (labels off)"].groupby(groupby)["total"].mean()
    df["(p-f)/(d-f)"] = (df_w[df_w["mode"] == "databank (labels off)"].groupby(groupby)["total"].mean() - df_w[df_w["mode"] == "Python/Flask"].groupby(groupby)["total"].mean()) / (df_w[df_w["mode"] == "databank (labels on)"].groupby(groupby)["total"].mean() - df_w[df_w["mode"] == "Python/Flask"].groupby(groupby)["total"].mean())
    print(df)
    
for workload in workloads:
    fig, ax = plt.subplots(figsize=(10,3))
    df_w = df[(df["workload"] == workload) & (df["u"] == 10) & (df["p"] == 1)]
    legend_x, legend_y = [], []
    for offset, mode, mode_label in list(zip(*[offsets, MODE_MAPPING.values(), mode_labels]))[::-1]:
        data = df_w[df_w["mode"] == mode].groupby('n')['other', 'database', 'monitoring', 'total', 'm2'].mean()
        indices = np.arange(len(data.index))
        mm = df_w[df_w["mode"] == mode].shape[0] / len(data.index)
        o = ax.bar(indices + offset, data['other'], width=W, color=color_f if mode == "Python/Flask" else colors[0])
        d = ax.bar(indices + offset, data['database'], bottom=data['other'], width=W, color=colors[1])
        m = ax.bar(indices + offset, data['monitoring'], bottom=data['database'] + data['other'], width=W, color=colors[2])
        for j, i in enumerate(data.index):
            ax.text(j + offset, data.loc[i,'total'], mode_label, ha = 'center')
    print(workload)
    show_costs(df_w, groupby='n')
    if len(indices) < len(n_events):
        ax.set_xticks(range(0, len(n_events)-1))
        ax.set_xticklabels(n_events[1:])
    else:
        ax.set_xticks(range(len(n_events)))
        ax.set_xticklabels(n_events)
    lgd = ax.legend([m, d, o], ["monitoring", "database", "other"], bbox_to_anchor=(1,1), loc="upper left")
    ax.set_ylim(top=ax.get_ylim()[1]*1.1)
    ax.set_ylabel("Execution time in s")
    ax.set_xlabel("Number of meetings $n$")
    #ax.yaxis.set_major_formatter(FormatStrFormatter('%1.2f'))
    #txt = ax.text(1.01, 0, "F = Flask/Python\nP = Passive Databank\nD = Databank", transform=ax.transAxes)
    txt = ax.text(1.01, 0, "F = Flask/Python\nD = Databank", transform=ax.transAxes)
    fig.savefig(workload + '_n.png', bbox_extra_artists=(lgd,txt), bbox_inches='tight')

# Function of u

for workload in workloads:
    fig, ax = plt.subplots(figsize=(10,3))
    df_w = df[(df["workload"] == workload) & (df["n"] == 50) & (df["p"] == 1)]
    legend_x, legend_y = [], []
    for offset, mode, mode_label in list(zip(*[offsets, MODE_MAPPING.values(), mode_labels]))[::-1]:
        data = df_w[df_w["mode"] == mode].groupby('u')['other', 'database', 'monitoring', 'total', 'm2'].mean()
        indices = np.arange(len(data.index))
        mm = df_w[df_w["mode"] == mode].shape[0] / len(data.index)
        o = ax.bar(indices + offset, data['other'], width=W, color=color_f if mode == "Python/Flask" else colors[0])
        d = ax.bar(indices + offset, data['database'], bottom=data['other'], width=W, color=colors[1])
        m = ax.bar(indices + offset, data['monitoring'], bottom=data['database'] + data['other'], width=W, color=colors[2])
        for j, i in enumerate(data.index):
            ax.text(j + offset, data.loc[i,'total'], mode_label, ha = 'center')
    print(workload)
    show_costs(df_w, groupby='u')
    ax.set_xticks(range(len(u_users)))
    ax.set_xticklabels(u_users)
    lgd = ax.legend([m, d, o], ["monitoring", "database", "other"], bbox_to_anchor=(1,1), loc="upper left")
    ax.set_ylim(top=ax.get_ylim()[1]*1.1)
    ax.set_ylabel("Execution time in s")
    ax.set_xlabel("Number of users $u$")
    #ax.yaxis.set_major_formatter(FormatStrFormatter('%1.2f'))
    #txt = ax.text(1.01, 0, "F = Flask/Python\nP = Passive Databank\nD = Databank", transform=ax.transAxes)
    txt = ax.text(1.01, 0, "F = Flask/Python\nD = Databank", transform=ax.transAxes)
    fig.savefig(workload + '_u.png', bbox_extra_artists=(lgd,txt), bbox_inches='tight')

# Function of p

for workload in workloads:
    fig, ax = plt.subplots(figsize=(10,3))
    df_w = df[(df["workload"] == workload) & (df["n"] == 50) & (df["u"] == 10)]
    legend_x, legend_y = [], []
    for offset, mode, mode_label in list(zip(*[offsets, MODE_MAPPING.values(), mode_labels]))[::-1]:
        data = df_w[df_w["mode"] == mode].groupby('p')['other', 'database', 'monitoring', 'total', 'm2'].mean()
        indices = np.arange(len(data.index))
        mm = df_w[df_w["mode"] == mode].shape[0] / len(data.index)
        o = ax.bar(indices + offset, data['other'], width=W, color=color_f if mode == "Python/Flask" else colors[0])
        d = ax.bar(indices + offset, data['database'], bottom=data['other'], width=W, color=colors[1])
        m = ax.bar(indices + offset, data['monitoring'], bottom=data['database'] + data['other'], width=W, color=colors[2])
        for j, i in enumerate(data.index):
            ax.text(j + offset, data.loc[i,'total'], mode_label, ha = 'center')
    print(workload)
    show_costs(df_w, groupby='p')
    ax.set_xticks(range(len(p_policies)))
    ax.set_xticklabels([f"$\\varphi_u^{p}$" for p in p_policies])
    lgd = ax.legend([m, d, o], ["monitoring", "database", "other"], bbox_to_anchor=(1,1), loc="upper left")
    ax.set_ylim(top=ax.get_ylim()[1]*1.1)
    ax.set_ylabel("Execution time in s")
    ax.set_xlabel("Policy p")
    #ax.yaxis.set_major_formatter(FormatStrFormatter('%1.2f'))
    #txt = ax.text(1.01, 0, "F = Flask/Python\nP = Passive Databank\nD = Databank", transform=ax.transAxes)
    txt = ax.text(1.01, 0, "F = Flask/Python\nD = Databank", transform=ax.transAxes)
    fig.savefig(workload + '_p.png', bbox_extra_artists=(lgd,txt), bbox_inches='tight')
