"""
Roster Management Page

This module contains the UI for managing the den roster.
Allows adding and removing scouts from the roster.
"""

import streamlit as st
import pandas as pd
from scout_tracker.config import *
from scout_tracker.data import load_roster, save_roster


def page_manage_roster():
    """Page for managing the den roster."""
    st.title("📋 Manage Roster")
    st.write("Add or remove scouts from your den's roster.")

    # Load current roster
    roster_df = load_roster()

    # Two column layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Add Scouts")

        # Create tabs for single vs bulk add
        tab1, tab2 = st.tabs(["Add One Scout", "Bulk Import"])

        # TAB 1: Single Scout Add
        with tab1:
            with st.form("add_scout_form"):
                new_scout_name = st.text_input("Scout Name", key="new_scout_name")
                submit_add = st.form_submit_button("Add Scout")

                if submit_add:
                    if not new_scout_name.strip():
                        st.error("❌ Please enter a scout name.")
                    elif new_scout_name in roster_df["Scout Name"].values:
                        st.error(f"❌ Scout '{new_scout_name}' already exists in the roster.")
                    else:
                        # Add new scout
                        new_row = pd.DataFrame({"Scout Name": [new_scout_name]})
                        roster_df = pd.concat([roster_df, new_row], ignore_index=True)
                        save_roster(roster_df)
                        st.success(f"✅ Added {new_scout_name} to the roster!")
                        st.rerun()

        # TAB 2: Bulk Import
        with tab2:
            with st.form("bulk_add_form"):
                st.write("Paste scout names below, one per line:")
                bulk_names = st.text_area(
                    "Scout Names",
                    height=200,
                    placeholder="John Smith\nJane Doe\nBob Johnson\n...",
                    key="bulk_scout_names",
                    help="Enter or paste multiple scout names, one per line"
                )
                submit_bulk = st.form_submit_button("Add All Scouts")

                if submit_bulk:
                    if not bulk_names.strip():
                        st.error("❌ Please enter at least one scout name.")
                    else:
                        # Parse the input - split by newlines and clean up
                        scout_names = [name.strip() for name in bulk_names.split('\n') if name.strip()]

                        if not scout_names:
                            st.error("❌ No valid scout names found.")
                        else:
                            # Filter out duplicates and existing scouts
                            existing_scouts = set(roster_df["Scout Name"].values)
                            new_scouts = []
                            skipped_duplicates = []
                            skipped_existing = []

                            for name in scout_names:
                                if name in existing_scouts:
                                    skipped_existing.append(name)
                                elif name in new_scouts:
                                    skipped_duplicates.append(name)
                                else:
                                    new_scouts.append(name)
                                    existing_scouts.add(name)  # Track for duplicate detection

                            # Add new scouts
                            if new_scouts:
                                new_rows = pd.DataFrame({"Scout Name": new_scouts})
                                roster_df = pd.concat([roster_df, new_rows], ignore_index=True)
                                save_roster(roster_df)
                                st.success(f"✅ Added {len(new_scouts)} scout(s) to the roster!")

                                # Show warnings if any were skipped
                                if skipped_existing:
                                    st.warning(f"⚠️ Skipped {len(skipped_existing)} scout(s) already in roster: {', '.join(skipped_existing[:5])}{'...' if len(skipped_existing) > 5 else ''}")
                                if skipped_duplicates:
                                    st.warning(f"⚠️ Removed {len(skipped_duplicates)} duplicate(s) from input: {', '.join(skipped_duplicates[:5])}{'...' if len(skipped_duplicates) > 5 else ''}")

                                st.rerun()
                            else:
                                st.error("❌ No new scouts to add. All names are already in the roster.")

    with col2:
        st.subheader("Current Den Roster")
        if not roster_df.empty:
            st.dataframe(roster_df, width='stretch', hide_index=True)

            # Remove scout section
            st.write("---")
            scout_to_remove = st.selectbox(
                "Select a scout to remove:",
                options=roster_df["Scout Name"].tolist(),
                key="scout_to_remove"
            )
            if st.button("Remove Selected Scout"):
                roster_df = roster_df[roster_df["Scout Name"] != scout_to_remove]
                save_roster(roster_df)
                st.success(f"✅ Removed {scout_to_remove} from the roster!")
                st.rerun()
        else:
            st.info("No scouts in the roster yet. Add some scouts to get started!")
