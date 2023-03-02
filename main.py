import os
import streamlit as st
import pandas as pd
import looker_sdk
from looker_sdk import models40

# Set Looker SDK environment variables using GitHub secrets
os.environ["LOOKERSDK_BASE_URL"] = "https://mylookerinstance.eu.looker.com/"
os.environ["LOOKERSDK_API_VERSION"] = "4.0"
os.environ["LOOKERSDK_VERIFY_SSL"] = "true"
os.environ["LOOKERSDK_TIMEOUT"] = "120"
os.environ["LOOKERSDK_CLIENT_ID"] = "client_id"
os.environ["LOOKERSDK_CLIENT_SECRET"] = "client_secret"

def main():
    st.header("My Looker Micro Front")
    st.markdown("---")

    st.title("User Management")

    # Authenticate with Looker SDK
    sdk = looker_sdk.init31()

    # Define a collapsible section for adding users to groups
    user_management_expander = st.expander("Add Users to Groups", expanded=False)
    with user_management_expander:
        # Call Looker SDK to get all users
        all_users = sdk.all_users()
        user_info = []
        for user in all_users:
            user_info.append({
                "ID": user.id,
                "Email": user.email,
                "First Name": user.first_name,
                "Last Name": user.last_name,
                "Disabled": user.is_disabled
            })

        # Display all users in a table with checkboxes to select users
        user_info_df = pd.DataFrame(user_info)
        user_info_df['Option'] = user_info_df['ID'].astype(str) + ' - ' + user_info_df['First Name'] + ' ' + user_info_df['Last Name'] + ' (' + user_info_df['Email'] + ')'
        selected_user_options = user_info_df.set_index('ID')['Option'].to_dict()
        selected_user_ids = st.multiselect("Select users to add to groups", options=list(selected_user_options.keys()), format_func=lambda x: selected_user_options[x])
        selected_users_df = user_info_df[user_info_df['ID'].isin(selected_user_ids)]
        st.dataframe(selected_users_df)


        # Call Looker SDK to get all groups
        all_groups = sdk.all_groups()
        group_info = []
        for group in all_groups:
            group_info.append({
                "ID": group.id,
                "Name": group.name,
                "User Count": group.user_count
        })

        # Display all groups in a table with checkboxes to select groups
        group_info_df = pd.DataFrame(group_info)
        group_info_df['Option'] = group_info_df['ID'].astype(str) + ' - ' + group_info_df['Name']
        selected_group_options = group_info_df.set_index('ID')['Option'].to_dict()
        selected_group_ids = st.multiselect("Select groups to add users to", options=list(selected_group_options.keys()), format_func=lambda x: selected_group_options[x])
        selected_groups_df = group_info_df[group_info_df['ID'].isin(selected_group_ids)]
        st.dataframe(selected_groups_df)

        # Add a button to add selected users to selected groups
        if st.button("Add Users to Selected Groups"):
            if len(selected_user_ids) == 0 or len(selected_group_ids) == 0:
                st.warning("Please select at least one user and one group.")
            else:
                # Call Looker SDK to add users to groups
                for group_id in selected_group_ids:
                    for user_id in selected_user_ids:
                        sdk.add_group_user(group_id=group_id, body=models40.GroupIdForGroupUserInclusion(user_id=user_id))

                st.success(f"Selected users ({len(selected_user_ids)}) added to selected groups ({len(selected_group_ids)}).")

    # Define a collapsible section for removing users from groups
    user_removal_expander = st.expander("Remove Users from Group", expanded=False)
    with user_removal_expander:
        # Call Looker SDK to get all groups
        all_groups = sdk.all_groups()
        group_info = []
        for group in all_groups:
            group_info.append({
                "ID": group.id,
                "Name": group.name,
                "User Count": group.user_count
         })

        # Display all groups in a table with checkboxes to select a group to remove users from
        group_info_df = pd.DataFrame(group_info)
        group_info_df['Option'] = group_info_df['ID'].astype(str) + ' - ' + group_info_df['Name']
        selected_group_options = group_info_df.set_index('ID')['Option'].to_dict()
        selected_group_id = st.selectbox("Select a group to remove users from", options=selected_group_options, format_func=lambda x: selected_group_options[x])
        selected_group_df = group_info_df[group_info_df['ID'] == selected_group_id]
        st.dataframe(selected_group_df)

        # Call Looker SDK to get all users in the selected group
        response = sdk.all_group_users(group_id=selected_group_id)
        user_info = []
        for user in response:
            user_info.append({
                "ID": user.id,
                "Email": user.email,
                "First Name": user.first_name,
                "Last Name": user.last_name,
                "Disabled": user.is_disabled
            })

        # Display all users in the selected group in a table with checkboxes to select users to remove
        user_info_df = pd.DataFrame(user_info)
        user_info_df['Option'] = user_info_df['ID'].astype(str) + ' - ' + user_info_df['First Name'] + ' ' + user_info_df['Last Name'] + ' (' + user_info_df['Email'] + ')'
        selected_user_options = user_info_df.set_index('ID')['Option'].to_dict()
        selected_user_ids = st.multiselect("Select users to remove from the group", options=list(selected_user_options.keys()), format_func=lambda x: selected_user_options[x])
        selected_users_df = user_info_df[user_info_df['ID'].isin(selected_user_ids)]
        st.dataframe(selected_users_df)

        # Add a button to remove selected users from the selected group
        if st.button("Remove Users from Selected Group"):
            if len(selected_user_ids) == 0:
                st.warning("Please select at least one user to remove.")
            else:
                # Call Looker SDK to remove users from the selected group
                for user_id in selected_user_ids:
                    sdk.delete_group_user(
                        group_id=selected_group_id,
                        user_id=user_id
                    )

                st.success(f"Selected users ({len(selected_user_ids)}) removed from group ({selected_group_id}).")
 
    st.title("Datagroups")

    # Define a collapsible section for datagroups
    datagroups_expander = st.expander("Datagroups status", expanded=False)
    with datagroups_expander:
        # Call Looker SDK to get all datagroups
        all_datagroups = sdk.all_datagroups()
        datagroup_info = []
        for datagroup in all_datagroups:
            datagroup_info.append({
                "ID": datagroup.id,
                "Model Name": datagroup.model_name,
                "Name": datagroup.name,
                "Trigger Check At": datagroup.trigger_check_at,
                "Trigger Error": datagroup.trigger_error,
                "Trigger Value": datagroup.trigger_value
            })

        # Display all datagroups in a table
        datagroup_info_df = pd.DataFrame(datagroup_info, columns=["ID", "Model Name", "Name", "Trigger Check At", "Trigger Error", "Trigger Value"])
        st.dataframe(datagroup_info_df)

if __name__ == "__main__":
    main()
