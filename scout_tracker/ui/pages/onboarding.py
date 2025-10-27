"""
Onboarding Flow Page

This module contains the UI for the onboarding flow for first-time users.
"""

import streamlit as st
import pandas as pd
from scout_tracker.config import (
    LION_REQUIREMENTS,
    TIGER_REQUIREMENTS,
    WOLF_REQUIREMENTS,
    BEAR_REQUIREMENTS,
    WEBELOS_REQUIREMENTS
)
from scout_tracker.data import load_roster, load_requirement_key, save_roster, save_requirements


def is_first_run():
    """Check if this is the first time the app is being used."""
    # Check if roster is empty and requirements are still default Lion requirements
    roster_df = load_roster()
    requirement_key = load_requirement_key()

    # First run if roster is empty AND using default requirements (Lion)
    is_first = roster_df.empty and len(requirement_key) == len(LION_REQUIREMENTS)

    return is_first


def page_onboarding():
    """Onboarding flow for first-time users."""

    # Initialize session state for onboarding
    if 'onboarding_step' not in st.session_state:
        st.session_state.onboarding_step = 1
    if 'onboarding_complete' not in st.session_state:
        st.session_state.onboarding_complete = False
    if 'selected_rank' not in st.session_state:
        st.session_state.selected_rank = None

    # Step 1: Welcome and Rank Selection
    if st.session_state.onboarding_step == 1:
        st.title("🏕️ Welcome to Scout Tracker!")
        st.write("### Let's get you started in just a few steps")

        st.write("---")
        st.subheader("Step 1: Select Your Den's Rank")
        st.write("Choose the rank level for your den. You can change this later if needed.")

        col1, col2 = st.columns([2, 1])

        with col1:
            rank_option = st.selectbox(
                "Which rank is your den?",
                options=["Lion (Kindergarten)", "Tiger (1st Grade)", "Wolf (2nd Grade)",
                        "Bear (3rd Grade)", "Webelos (4th-5th Grade)"],
                key="rank_selection"
            )

            # Show info about the selected rank
            rank_info = {
                "Lion (Kindergarten)": "Lion Scouts work on 6 required adventures and 2+ elective adventures with detailed requirements.",
                "Tiger (1st Grade)": "Tiger Scouts complete 6 required adventures and 2+ elective adventures.",
                "Wolf (2nd Grade)": "Wolf Scouts complete 6 required adventures and 2+ elective adventures.",
                "Bear (3rd Grade)": "Bear Scouts complete 6 required adventures and 2+ elective adventures.",
                "Webelos (4th-5th Grade)": "Webelos Scouts earn required and elective adventure pins toward their Arrow of Light."
            }

            st.info(rank_info[rank_option])

            if st.button("✅ Continue with " + rank_option.split()[0], type="primary", width='stretch'):
                st.session_state.selected_rank = rank_option.split()[0]
                st.session_state.onboarding_step = 2
                st.rerun()

        with col2:
            st.write("**Why this matters:**")
            st.write("Scout Tracker will load the appropriate requirements for your selected rank.")
            st.write("")
            st.write("**Can I change this later?**")
            st.write("Yes! You can load different rank requirements at any time from the Manage Requirements page.")

    # Step 2: Loading Requirements
    elif st.session_state.onboarding_step == 2:
        st.title("🏕️ Setting Up Your Den")
        st.write("### Step 2: Loading Requirements")

        rank = st.session_state.selected_rank
        st.info(f"📥 Loading {rank} Scout requirements...")

        # Load the appropriate requirements based on rank
        rank_requirements_map = {
            "Lion": LION_REQUIREMENTS,
            "Tiger": TIGER_REQUIREMENTS,
            "Wolf": WOLF_REQUIREMENTS,
            "Bear": BEAR_REQUIREMENTS,
            "Webelos": WEBELOS_REQUIREMENTS
        }

        requirements_data = rank_requirements_map.get(rank, LION_REQUIREMENTS)
        df = pd.DataFrame(requirements_data)
        save_requirements(df)

        st.success(f"✅ Successfully loaded {len(df)} {rank} Scout requirements!")
        st.write(f"- **Required adventures:** {len(df[df['Required'] == True]['Adventure'].unique())}")
        st.write(f"- **Elective adventures:** {len(df[df['Required'] == False]['Adventure'].unique())}")

        if st.button("Continue to Roster Setup →", type="primary"):
            st.session_state.onboarding_step = 3
            st.rerun()

    # Step 3: Roster Setup
    elif st.session_state.onboarding_step == 3:
        st.title("🏕️ Setting Up Your Den")
        st.write("### Step 3: Add Your Scouts")

        st.write("Let's add the scouts in your den. You can add more scouts later from the Manage Roster page.")

        roster_df = load_roster()

        # Show current scouts if any
        if not roster_df.empty:
            st.write(f"**Current roster:** {len(roster_df)} scout(s)")
            for scout_name in roster_df["Scout Name"]:
                st.write(f"✓ {scout_name}")
            st.write("---")

        # Add scout form
        with st.form("onboarding_add_scout"):
            scout_name = st.text_input("Scout Name", placeholder="Enter scout's name")
            col1, col2 = st.columns(2)
            with col1:
                add_scout = st.form_submit_button("➕ Add Scout", width='stretch')
            with col2:
                done = st.form_submit_button("✅ Done - Start Using Scout Tracker", type="primary", width='stretch')

            if add_scout and scout_name.strip():
                if scout_name not in roster_df["Scout Name"].values:
                    new_scout = pd.DataFrame({"Scout Name": [scout_name]})
                    roster_df = pd.concat([roster_df, new_scout], ignore_index=True)
                    save_roster(roster_df)
                    st.success(f"Added {scout_name} to the roster!")
                    st.rerun()
                else:
                    st.warning(f"{scout_name} is already in the roster.")

            if done:
                if roster_df.empty:
                    st.warning("⚠️ Please add at least one scout before continuing.")
                else:
                    st.session_state.onboarding_complete = True
                    st.session_state.onboarding_step = 4
                    st.rerun()

    # Step 4: Completion
    elif st.session_state.onboarding_step == 4:
        st.balloons()
        st.title("🎉 Setup Complete!")
        st.write("### Your den is ready to track advancement!")

        rank = st.session_state.selected_rank
        roster_df = load_roster()

        st.success(f"""
        **What you've set up:**
        - ✅ {rank} Scout requirements loaded
        - ✅ {len(roster_df)} scout(s) in your roster

        **Next steps:**
        1. **Plan Meetings** - Create meetings and select which requirements you'll cover
        2. **Log Attendance** - After meetings, mark which scouts attended
        3. **Track Progress** - View the dashboard to see each scout's advancement
        """)

        if st.button("🚀 Go to Dashboard", type="primary"):
            st.session_state.onboarding_complete = True
            st.rerun()
