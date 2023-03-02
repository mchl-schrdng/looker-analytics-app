# My Looker Micro Front
<img width="781" alt="image" src="https://user-images.githubusercontent.com/73759636/221237370-5d9245bd-058d-479d-86b5-c6705fca684d.png">

This is a Streamlit application that provides an interface to manage users and datagroups in Looker. The objective of this micro front-end is to enable end-users to perform admin actions without requiring admin permissions. This particular implementation provides three actions - adding users to groups, deleting users from groups, and viewing datagroups. However, you can easily add as many micro actions as needed.

## Installation
To run this app, you will need to install the following packages:

```python
pip install streamlit
pip install looker-sdk
pip install pandas
```
Additionally, you will need to set the following environment variables to your Looker API credentials:

```python
LOOKERSDK_BASE_URL
LOOKERSDK_CLIENT_ID
LOOKERSDK_CLIENT_SECRET
```

## Usage
To run the app, navigate to the directory where the code is saved and run the following command:

```python
streamlit run main.py
```

The app will open in your browser, and you can use the various sections to manage users and datagroups in Looker.

## User Management
The "User Management" section allows you to add users to groups and remove users from groups. To use this section, you will need to authenticate with Looker using the Looker SDK.

You can add users to groups by selecting users from a table and groups from a table, and then clicking the "Add Users to Selected Groups" button.

You can remove users from a group by selecting a group from a table, selecting users from a table, and then clicking the "Remove Users from Selected Group" button.

## Datagroups
The "Datagroups" section allows you to view information about all datagroups in Looker. To use this section, you will need to authenticate with Looker using the Looker SDK.

## License
This app is licensed under the MIT License. See the LICENSE file for more information.
