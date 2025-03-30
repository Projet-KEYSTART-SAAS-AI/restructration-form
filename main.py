import streamlit as st
from setup_section import render_setup_section
from form_section import render_form_section
from dirigeant_loader import render_dirigeant_loader

st.set_page_config(page_title="Formulaire Structuration", layout="wide")
st.title("Formulaire de Structuration d'Entreprise")

# Step 1: Setup keys
openai_key, society_key = render_setup_section()

st.markdown("---")

# Step 2: Dirigeant loader with checkbox selection
dirigeant_id, selected_mandats = render_dirigeant_loader(society_key)

st.markdown("---")

# Step 3: Main form
form_data = render_form_section()

st.markdown("---")

# Final submit
if st.button("Soumettre le formulaire"):
    st.success("Formulaire soumis ! (Voir les logs ci-dessous)")

    st.write("## Résumé")

    st.write("### OpenAI Key")
    st.code(openai_key or "Non fourni", language='text')

    st.write("### Society.com Key")
    st.code(society_key or "Non fourni", language='text')

    st.write("### Dirigeant ID")
    st.code(dirigeant_id or "Non fourni", language='text')

    st.write("### Mandats sélectionnés")
    st.json(selected_mandats)

    st.write("### Objectifs")
    st.json(form_data["objectifs"])

    st.write("### Contraintes")
    st.json(form_data["contraintes"])
