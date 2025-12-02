"""
Requirements Management Page

This module contains the UI for managing adventure requirements (CRUD operations).
Allows adding, editing, deleting, and importing/exporting requirements.
"""

import streamlit as st
import pandas as pd
from scout_tracker.config import LION_REQUIREMENTS, RANK_REQUIREMENTS
from scout_tracker.data import load_requirement_key, save_requirements


def page_manage_requirements():
    """Page for managing adventure requirements (CRUD operations)."""
    st.title("📚 Manage Requirements")
    st.write("Add, edit, or remove adventure requirements for your den.")

    # Load current requirements
    requirements_df = load_requirement_key()

    # Create tabs for different operations
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["View All", "Add New", "Edit Existing", "Delete", "Import/Export"])

    # TAB 1: View All Requirements
    with tab1:
        st.subheader("All Requirements")
        if not requirements_df.empty:
            # Group by required/elective first
            st.write("### Required Adventures (Must complete all)")
            required_df = requirements_df[requirements_df["Required"] == True]
            if not required_df.empty:
                adventures = required_df["Adventure"].unique()
                for adventure in sorted(adventures):
                    adventure_reqs = required_df[required_df["Adventure"] == adventure]
                    # Get URL for the adventure (from first requirement)
                    adventure_url = adventure_reqs.iloc[0].get("URL", "") if not adventure_reqs.empty else ""

                    # Show adventure name and link separately to avoid click conflicts
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        header = f"{adventure} ({len(adventure_reqs)} requirements)"
                    with col2:
                        if adventure_url:
                            st.markdown(f"[📖 View on BSA Website]({adventure_url})")

                    with st.expander(header):
                        # Show requirements without URL column in dataframe
                        display_cols = ["Req_ID", "Adventure", "Requirement_Description", "Required"]
                        st.dataframe(adventure_reqs[display_cols], width='stretch', hide_index=True)
            else:
                st.info("No required adventures found.")

            st.write("---")
            st.write("### Elective Adventures (Must complete any 2)")
            elective_df = requirements_df[requirements_df["Required"] == False]
            if not elective_df.empty:
                adventures = elective_df["Adventure"].unique()
                for adventure in sorted(adventures):
                    adventure_reqs = elective_df[elective_df["Adventure"] == adventure]
                    # Get URL for the adventure (from first requirement)
                    adventure_url = adventure_reqs.iloc[0].get("URL", "") if not adventure_reqs.empty else ""

                    # Show adventure name and link separately to avoid click conflicts
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        header = f"{adventure} ({len(adventure_reqs)} requirements)"
                    with col2:
                        if adventure_url:
                            st.markdown(f"[📖 View on BSA Website]({adventure_url})")

                    with st.expander(header):
                        # Show requirements without URL column in dataframe
                        display_cols = ["Req_ID", "Adventure", "Requirement_Description", "Required"]
                        st.dataframe(adventure_reqs[display_cols], width='stretch', hide_index=True)
            else:
                st.info("No elective adventures found.")
        else:
            st.info("No requirements found. Add some requirements to get started!")

    # TAB 2: Add New Requirement
    with tab2:
        st.subheader("Add a New Requirement")
        with st.form("add_requirement_form"):
            new_req_id = st.text_input(
                "Requirement ID",
                placeholder="e.g., Bobcat.1 or MyAdventure.1",
                help="Use format: AdventureName.Number"
            )
            new_adventure = st.text_input(
                "Adventure Name",
                placeholder="e.g., Bobcat, Fun on the Run",
                help="Name of the adventure this requirement belongs to"
            )
            new_description = st.text_area(
                "Requirement Description",
                placeholder="e.g., 1. Get to know the members of your den",
                help="Detailed description of what scouts need to do"
            )
            new_required = st.checkbox(
                "Required Adventure",
                value=False,
                help="Check if this is a required adventure (must complete all required adventures). Uncheck for elective adventures (must complete any 2)."
            )
            new_url = st.text_input(
                "Reference URL (optional)",
                placeholder="https://www.scouting.org/cub-scout-adventures/...",
                help="Link to BSA website or other reference material for this requirement"
            )

            submit_add = st.form_submit_button("Add Requirement")

            if submit_add:
                if not new_req_id.strip() or not new_adventure.strip() or not new_description.strip():
                    st.error("❌ Please fill in all fields.")
                elif new_req_id in requirements_df["Req_ID"].values:
                    st.error(f"❌ Requirement ID '{new_req_id}' already exists.")
                else:
                    # Add new requirement
                    new_row = pd.DataFrame({
                        "Req_ID": [new_req_id],
                        "Adventure": [new_adventure],
                        "Requirement_Description": [new_description],
                        "Required": [new_required],
                        "URL": [new_url.strip()]
                    })
                    requirements_df = pd.concat([requirements_df, new_row], ignore_index=True)
                    save_requirements(requirements_df)
                    st.success(f"✅ Added requirement {new_req_id}!")
                    st.rerun()

    # TAB 3: Edit Existing Requirement
    with tab3:
        st.subheader("Edit an Existing Requirement")
        if not requirements_df.empty:
            # Select requirement to edit
            req_options = [
                f"{row['Req_ID']} - {row['Requirement_Description'][:50]}..."
                for _, row in requirements_df.iterrows()
            ]
            selected_req = st.selectbox(
                "Select a requirement to edit:",
                options=req_options,
                key="edit_req_select"
            )

            if selected_req:
                # Extract Req_ID from selection
                selected_req_id = selected_req.split(" - ")[0]
                current_req = requirements_df[requirements_df["Req_ID"] == selected_req_id].iloc[0]

                with st.form("edit_requirement_form"):
                    st.write(f"Editing: **{selected_req_id}**")

                    edit_adventure = st.text_input(
                        "Adventure Name",
                        value=current_req["Adventure"]
                    )
                    edit_description = st.text_area(
                        "Requirement Description",
                        value=current_req["Requirement_Description"],
                        height=100
                    )
                    edit_required = st.checkbox(
                        "Required Adventure",
                        value=bool(current_req["Required"]),
                        help="Check if this is a required adventure (must complete all required adventures). Uncheck for elective adventures (must complete any 2)."
                    )
                    edit_url = st.text_input(
                        "Reference URL (optional)",
                        value=current_req.get("URL", ""),
                        placeholder="https://www.scouting.org/cub-scout-adventures/...",
                        help="Link to BSA website or other reference material for this requirement"
                    )

                    submit_edit = st.form_submit_button("Save Changes")

                    if submit_edit:
                        # Update the requirement
                        requirements_df.loc[
                            requirements_df["Req_ID"] == selected_req_id,
                            ["Adventure", "Requirement_Description", "Required", "URL"]
                        ] = [edit_adventure, edit_description, edit_required, edit_url.strip()]
                        save_requirements(requirements_df)
                        st.success(f"✅ Updated requirement {selected_req_id}!")
                        st.rerun()
        else:
            st.info("No requirements available to edit.")

    # TAB 4: Delete Requirement
    with tab4:
        st.subheader("Delete a Requirement")
        if not requirements_df.empty:
            req_to_delete = st.selectbox(
                "Select a requirement to delete:",
                options=requirements_df["Req_ID"].tolist(),
                key="delete_req_select"
            )

            if req_to_delete:
                req_details = requirements_df[requirements_df["Req_ID"] == req_to_delete].iloc[0]
                st.warning(f"**Warning:** You are about to delete:")
                st.write(f"- **ID:** {req_details['Req_ID']}")
                st.write(f"- **Adventure:** {req_details['Adventure']}")
                st.write(f"- **Description:** {req_details['Requirement_Description']}")

                if st.button("⚠️ Confirm Delete", type="primary"):
                    requirements_df = requirements_df[requirements_df["Req_ID"] != req_to_delete]
                    save_requirements(requirements_df)
                    st.success(f"✅ Deleted requirement {req_to_delete}!")
                    st.rerun()
        else:
            st.info("No requirements available to delete.")

    # TAB 5: Import/Export
    with tab5:
        st.subheader("Import/Export Requirements")
        st.write("Share requirements with other dens or back up your customizations.")

        col1, col2 = st.columns(2)

        with col1:
            st.write("### 📥 Import Requirements")
            st.write("Upload a CSV file with requirements to replace or add to your current set.")

            uploaded_file = st.file_uploader(
                "Choose a CSV file",
                type="csv",
                key="import_requirements",
                help="CSV must have columns: Req_ID, Adventure, Requirement_Description, Required"
            )

            import_mode = st.radio(
                "Import Mode:",
                ["Replace All (clear existing)", "Add New (keep existing)"],
                key="import_mode"
            )

            if uploaded_file is not None:
                try:
                    imported_df = pd.read_csv(uploaded_file)

                    # Validate required columns
                    required_cols = ["Req_ID", "Adventure", "Requirement_Description", "Required"]
                    if not all(col in imported_df.columns for col in required_cols):
                        st.error(f"❌ CSV must contain columns: {', '.join(required_cols)}")
                    else:
                        st.write(f"**Preview:** {len(imported_df)} requirements found")
                        st.dataframe(imported_df.head(), width='stretch')

                        if st.button("✅ Import Requirements", type="primary"):
                            if import_mode == "Replace All (clear existing)":
                                save_requirements(imported_df)
                                st.success(f"✅ Replaced all requirements with {len(imported_df)} imported requirements!")
                            else:
                                # Add new, skip duplicates
                                existing_ids = set(requirements_df["Req_ID"].values)
                                new_reqs = imported_df[~imported_df["Req_ID"].isin(existing_ids)]
                                if not new_reqs.empty:
                                    combined_df = pd.concat([requirements_df, new_reqs], ignore_index=True)
                                    save_requirements(combined_df)
                                    st.success(f"✅ Added {len(new_reqs)} new requirements!")
                                else:
                                    st.warning("⚠️ No new requirements to add (all IDs already exist)")
                            st.rerun()

                except Exception as e:
                    st.error(f"❌ Error reading CSV: {str(e)}")

        with col2:
            st.write("### 📤 Export Requirements")
            st.write("Download your current requirements as a CSV file to share or back up.")

            if not requirements_df.empty:
                # Convert DataFrame to CSV
                csv = requirements_df.to_csv(index=False)

                st.download_button(
                    label="⬇️ Download Requirements CSV",
                    data=csv,
                    file_name="scout_requirements.csv",
                    mime="text/csv",
                    width='stretch'
                )

                st.info(f"📊 {len(requirements_df)} requirements ready to export")
            else:
                st.warning("No requirements to export")

        st.write("---")

        # Load Pre-Packaged Requirements
        st.write("### 📦 Load Pre-Packaged Requirements")
        st.write("Quickly switch to a different Cub Scout rank with official BSA adventure structure.")

        selected_rank = st.selectbox(
            "Select Rank:",
            options=list(RANK_REQUIREMENTS.keys()),
            key="rank_selector",
            help="Choose a rank to load its pre-packaged requirements"
        )

        if selected_rank:
            rank_reqs = RANK_REQUIREMENTS[selected_rank]
            required_count = sum(1 for r in rank_reqs if r["Required"])
            elective_count = sum(1 for r in rank_reqs if not r["Required"])

            st.info(f"**{selected_rank}** has {required_count} required adventures and {elective_count} elective adventures")

            if st.button(f"📥 Load {selected_rank} Requirements", type="primary", width='stretch'):
                if st.session_state.get("confirm_load_rank", False):
                    df = pd.DataFrame(rank_reqs)
                    save_requirements(df)
                    st.session_state["confirm_load_rank"] = False
                    st.success(f"✅ Loaded {selected_rank} requirements!")
                    st.rerun()
                else:
                    st.session_state["confirm_load_rank"] = True
                    st.warning(f"⚠️ Click again to confirm. This will replace ALL current requirements with {selected_rank} requirements!")

        st.write("---")

        # Quick Actions
        st.write("### ⚙️ Quick Actions")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔄 Reset to Lion Scout Defaults", width='stretch'):
                if st.session_state.get("confirm_reset", False):
                    # Reload the default Lion requirements
                    df = pd.DataFrame(LION_REQUIREMENTS)
                    save_requirements(df)
                    st.session_state["confirm_reset"] = False
                    st.success("✅ Reset to Lion Scout defaults!")
                    st.rerun()
                else:
                    st.session_state["confirm_reset"] = True
                    st.warning("⚠️ Click again to confirm reset. This will replace ALL current requirements!")

        with col2:
            if st.button("🗑️ Clear All Requirements", width='stretch'):
                if st.session_state.get("confirm_clear", False):
                    empty_df = pd.DataFrame(columns=["Req_ID", "Adventure", "Requirement_Description", "Required"])
                    save_requirements(empty_df)
                    st.session_state["confirm_clear"] = False
                    st.success("✅ All requirements cleared!")
                    st.rerun()
                else:
                    st.session_state["confirm_clear"] = True
                    st.warning("⚠️ Click again to confirm clear. This cannot be undone!")
