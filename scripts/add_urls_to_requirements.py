#!/usr/bin/env python3
"""
Script to add URL column to Requirement_Key.csv and populate with BSA adventure URLs.
"""
import pandas as pd
from pathlib import Path

# Adventure name to URL mapping from https://www.scouting.org/programs/cub-scouts/adventures/lion/
ADVENTURE_URLS = {
    "Bobcat": "https://www.scouting.org/cub-scout-adventures/bobcat-lion/",
    "Fun on the Run": "https://www.scouting.org/cub-scout-adventures/fun-on-the-run/",
    "Lion's Roar": "https://www.scouting.org/cub-scout-adventures/lions-roar/",
    "Lion's Pride": "https://www.scouting.org/cub-scout-adventures/lions-pride/",
    "King of the Jungle": "https://www.scouting.org/cub-scout-adventures/king-of-the-jungle/",
    "Mountain Lion": "https://www.scouting.org/cub-scout-adventures/mountain-lion/",
    "Build It Up, Knock It Down": "https://www.scouting.org/cub-scout-adventures/build-it-up-knock-it-down/",
    "Champions for Nature": "https://www.scouting.org/cub-scout-adventures/champions-for-nature-lion/",
    "Count On Me": "https://www.scouting.org/cub-scout-adventures/count-on-me/",
    "Everyday Tech": "https://www.scouting.org/cub-scout-adventures/everyday-tech/",
    "Gizmos and Gadgets": "https://www.scouting.org/cub-scout-adventures/gizmos-and-gadgets/",
    "Go Fish": "https://www.scouting.org/cub-scout-adventures/go-fish/",
    "I'll Do It Myself": "https://www.scouting.org/cub-scout-adventures/ill-do-it-myself/",
    "Let's Camp Lion": "https://www.scouting.org/cub-scout-adventures/lets-camp-lion/",
    "On a Roll": "https://www.scouting.org/cub-scout-adventures/on-a-roll/",
    "On Your Mark": "https://www.scouting.org/cub-scout-adventures/on-your-mark/",
    "Pick My Path": "https://www.scouting.org/cub-scout-adventures/pick-my-path-lion/",
    "Race Time Lion": "https://www.scouting.org/cub-scout-adventures/race-time-lion/",
    "Ready, Set, Grow": "https://www.scouting.org/cub-scout-adventures/ready-set-grow/",
    "Time to Swim": "https://www.scouting.org/cub-scout-adventures/time-to-swim/",
}

def main():
    csv_path = Path("tracker_data/Requirement_Key.csv")

    if not csv_path.exists():
        print(f"Error: {csv_path} does not exist")
        return

    # Load the CSV
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} requirements from {csv_path}")

    # Add URL column if it doesn't exist
    if "URL" not in df.columns:
        df["URL"] = ""
        print("Added URL column")

    # Populate URLs based on adventure name
    updated_count = 0
    for idx, row in df.iterrows():
        adventure = row["Adventure"]
        if adventure in ADVENTURE_URLS:
            df.at[idx, "URL"] = ADVENTURE_URLS[adventure]
            updated_count += 1

    # Save back to CSV
    df.to_csv(csv_path, index=False)
    print(f"\nUpdated {updated_count} requirements with URLs")
    print(f"Saved to {csv_path}")

    # Summary
    print("\nSummary by adventure:")
    for adventure in sorted(df["Adventure"].unique()):
        adv_df = df[df["Adventure"] == adventure]
        url = adv_df.iloc[0]["URL"] if len(adv_df) > 0 else ""
        status = "✓ URL added" if url else "✗ No URL"
        print(f"  {adventure} ({len(adv_df)} reqs): {status}")

if __name__ == "__main__":
    main()
