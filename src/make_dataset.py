import argparse 
import pandas as pd
import os

def main():
    parser = argparse.ArgumentParser(description="Build labeled dataset from normal + replay features")
    parser.add_argument("--normal", required=True, help="Path to features_normal.csv")
    parser.add_argument("--replay", required=True, help="Path to features_replay.csv")
    parser.add_argument("--out", default="outputs/dataset.csv", help="Output dataset CSV path")
    args = parser.parse_args()

    normal_df = pd.read_csv(args.normal)
    replay_df = pd.read_csv(args.replay)

    normal_df["label"] = 0
    replay_df["label"] = 1

    # ensure same feature columns (except label)
    common_cols = sorted(list(set(normal_df.columns) & set(replay_df.columns)))
    # keep all feature cols + label
    normal_df = normal_df[common_cols]
    replay_df = replay_df[common_cols]

    dataset = pd.concat([normal_df, replay_df], ignore_index=True)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    dataset.to_csv(args.out, index=False)

    print("Saved:", args.out)
    print("Rows:", len(dataset), "Normal:", (dataset["label"] == 0).sum(), "Replay:", (dataset["label"] == 1).sum())
    print("Columns:", list(dataset.columns))

if __name__ == "__main__":
    main()