import streamlit as st

# Subheading
st.markdown("## 📌 Key Features")

# Horizontal list (Markdown + HTML)
st.markdown("""
**Modules:**
<ul style='display: flex; list-style-type: none; padding-left: 0;'>
    <li style='margin-right: 20px;'>🔍 Search</li>
    <li style='margin-right: 20px;'>📊 Analytics</li>
    <li style='margin-right: 20px;'>⚙️ Settings</li>
</ul>
""", unsafe_allow_html=True)

# Collapsed bullet points (HTML details/summary)
st.markdown("""
<details>
<summary>📁 Expand for more options</summary>

- 📄 Reports
- 🔔 Notifications
- 🧩 Plugins
- 🛠️ Developer Tools

</details>
""", unsafe_allow_html=True)
