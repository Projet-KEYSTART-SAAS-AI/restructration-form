import streamlit as st
import requests

def render_dirigeant_loader(society_key):
    st.subheader("Dirigeant")

    dirigeant_id = st.text_input("Identifiant dirigeant (ex : Johan-Makerly.GROCHATEAU.u3QfJn6385B)", "Johan-Makerly.GROCHATEAU.u3QfJn6385B")

    mandats = []
    if st.button("Charger les mandats"):
        if not society_key or not dirigeant_id:
            st.warning("Veuillez fournir la clé API et l'identifiant dirigeant.")
            return dirigeant_id, []

        url = f"https://api.societe.com/api/v1/mandats/{dirigeant_id}"
        headers = {
            "X-Authorization": f"socapi {society_key}",
            "Accept": "application/json"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json().get("data", {})
            mandats = data.get("mandats", [])
            st.session_state["mandats"] = mandats  # Save in session
        else:
            st.error(f"Erreur API : {response.status_code}")
            return dirigeant_id, []

    # Load from session if available
    mandats = st.session_state.get("mandats", [])

    selected_rows = []

    if mandats:
        st.write("### Mandats disponibles")

        # Table headers
        cols = st.columns([1, 2, 2, 3, 2, 2])
        cols[0].write("Sélect.")
        cols[1].write("Dénomination")
        cols[2].write("Ville")
        cols[3].write("Activité")
        cols[4].write("Fonction")
        cols[5].write("SIREN")

        # Render each row with a checkbox
        for i, mandat in enumerate(mandats):
            checkbox_key = f"mandat_select_{i}"
            if checkbox_key not in st.session_state:
                st.session_state[checkbox_key] = False

            cols = st.columns([1, 2, 2, 3, 2, 2])
            selected = cols[0].checkbox("", key=checkbox_key)
            cols[1].write(mandat.get("denomination", ""))
            cols[2].write(mandat.get("ville", ""))
            cols[3].write(mandat.get("activitelibelle", ""))
            cols[4].write(mandat.get("fonctionlibelle", ""))
            cols[5].write(mandat.get("siren", ""))

            if selected:
                selected_rows.append(mandat)

    return dirigeant_id, selected_rows
