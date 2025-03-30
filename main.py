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

    objectifs = form_data["objectifs"]
    contraintes = form_data["contraintes"]

    # --- Build prompt ---
    prompt_lines = []
    prompt_lines.append("A user wants a restructuration of his company.")
    
    prompt_lines.append("\nThese are his goals:")
    for key, val in objectifs.items():
        question = key.capitalize().replace("_", " ")
        prompt_lines.append(f"- {question}: {val.strip() or 'No answer provided'}")

    prompt_lines.append("\nThese are his constraints:")
    for key, val in contraintes.items():
        question = key.capitalize().replace("_", " ")
        prompt_lines.append(f"- {question}: {val.strip() or 'No answer provided'}")

    if selected_mandats:
        prompt_lines.append("\nThese are his current companies:")
        for mandat in selected_mandats:
            prompt_lines.append(
                f"- {mandat.get('denomination', 'N/A')} ({mandat.get('ville', '')}) - "
                f"{mandat.get('activitelibelle', '')} | SIREN: {mandat.get('siren', '')}"
            )
    else:
        prompt_lines.append("\nThe user has selected no current companies.")

    final_prompt = "\n".join(prompt_lines)

    # --- Log Everything ---
    st.write("### OpenAI Key (for future use)")
    st.code(openai_key or "Not provided", language="text")

    st.write("### Final Prompt to send to ChatGPT")
    st.code(final_prompt, language="markdown")