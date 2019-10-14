# %%
import pandas as pd
import os
import sys
import subprocess


# %% functions
def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])


def episode_randomizer(path='.', save_df=True, open_ep=False):
    # create empty DataFrame
    df = pd.DataFrame(columns=['season', 'episode_number', 'episode_name',
        'rel_path'])
    # Walk selected path
    for root, _, files in os.walk(path):
        for name in files:
            df = df.append({'season': root, 'episode_number': name,
                'episode_name': name, 'rel_path': root + '/' + name},
                ignore_index=True)
    # Populate DataFrame
    df = df[df['season'] != '.']  # borro este archivo del df
    df.season = df.season.str.extract(r'(\d+)').astype(int)
    df.episode_number = df.episode_number.str.extract(r'x(\d+)').astype(int)
    df.episode_name = df.episode_name.str.extract(r'x\d+\s?_?(.+)')
    df.episode_name = df.episode_name.str.strip().str.replace(r'\..+', '')
    df = df.sort_values(['season', 'episode_number'])
    df.index = df.season.astype(str) + 'X' + df.episode_number.astype(str)
    # Write DF to folder
    if save_df:
        df.to_csv(f'{path}/episodes.csv', sep='|')
    if open_ep:
        open_file(df.sample(1).rel_path[0])
    return df.sample(1)
