import streamlit as st
import os
import json
from dotenv import load_dotenv
from api.societe_api import fetch_infos_legales, fetch_latest_bilan, fetch_mandats
from api.openai_api import call_openai

# Load environment variables
load_dotenv()

# ---------- Utils ----------

def load_prompt_template(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def format_company_data(companies):
    output = ""
    for i, comp in enumerate(companies, 1):
        output += f"\nEntreprise {i} :\n"
        output += f"- Dénomination : {comp['denomination']}\n"
        output += "- Infos légales :\n" + json.dumps(comp['infos_legales'], indent=2, ensure_ascii=False) + "\n"
        output += "- Dernier bilan :\n" + json.dumps(comp['latest_bilan'], indent=2, ensure_ascii=False) + "\n"
    return output

# ---------- Init State ----------

def init_state():
    defaults = {
        "mandats": [],
        "selected_rows": [],
        "company_data": [],
        "fs_result": "",
        "fs_prompt": "",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

# ---------- Main App ----------

def main():
    st.set_page_config("FS Score Generator", layout="wide")
    st.title("📊 Générateur FS Score avec OpenAI")

    init_state()

    dirigeant_id = st.text_input("Identifiant dirigeant", value="Johan-Makerly.GROCHATEAU.u3QfJn6385B")

    if st.button("🔍 Charger les entreprises"):
        with st.spinner("Chargement des mandats..."):
            mandats = fetch_mandats(dirigeant_id)
            if mandats:
                st.session_state["mandats"] = mandats
                st.success(f"{len(mandats)} entreprise(s) trouvée(s).")
            else:
                st.error("Aucune entreprise trouvée ou erreur API.")

    if st.session_state["mandats"]:
        st.subheader("Étape 1 : Sélectionner les entreprises à analyser")
        selected = []
        with st.form("form_selection"):
            for mandat in st.session_state["mandats"]:
                siren = mandat.get("siren")
                denom = mandat.get("denomination", "")
                checkbox_key = f"checkbox_{siren}"
                if st.checkbox(f"{denom} ({siren})", key=checkbox_key):
                    selected.append(mandat)
            submitted = st.form_submit_button("Analyser")
        if submitted:
            st.session_state["selected_rows"] = selected
            st.session_state["company_data"] = []
            st.session_state["fs_result"] = ""
            st.session_state["fs_prompt"] = ""

    if st.session_state["selected_rows"] and not st.session_state["company_data"]:
        st.subheader("Étape 2 : Récupération des données")
        company_data = []
        for mandat in st.session_state["selected_rows"]:
            siren = mandat["siren"]
            denomination = mandat.get("denomination", "Entreprise")
            with st.spinner(f"Chargement : {denomination} ({siren})"):
                infos = fetch_infos_legales(siren)
                bilan = fetch_latest_bilan(siren)
                if infos:
                    company_data.append({
                        "denomination": denomination,
                        "siren": siren,
                        "infos_legales": infos,
                        "latest_bilan": bilan
                    })
                else:
                    st.warning(f"⚠️ Pas d'infos pour {denomination}")
        st.session_state["company_data"] = company_data

    if st.session_state["company_data"]:
        st.subheader("Étape 3 : Générer le prompt FS Score")

        if not st.session_state["fs_prompt"]:
            fs_template = load_prompt_template("prompts/fs_score_prompt.txt")
            entreprise_data = format_company_data(st.session_state["company_data"])
            final_prompt = fs_template.format(entreprise_data=entreprise_data)
            st.session_state["fs_prompt"] = final_prompt

        st.text_area("📋 Prompt FS généré", st.session_state["fs_prompt"], height=500)

        if st.button("⚡ Générer FS Score via OpenAI"):
            with st.spinner("Appel OpenAI..."):
                fs_response = call_openai(st.session_state["fs_prompt"])
                st.session_state["fs_result"] = fs_response
                st.success("✅ FS Score généré avec succès")

    if st.session_state["fs_result"]:
        st.subheader("📊 Résultat FS Score")
        st.text_area("Résultat OpenAI", st.session_state["fs_result"], height=600)

        restructuring_template = load_prompt_template("prompts/restructuring_prompt.txt")
        restructure_prompt = restructuring_template.format(fs_result=st.session_state["fs_result"])
        st.text_area("📋 Prompt Recommandations", restructure_prompt, height=500)

        if st.button("🧠 Générer Plan Fiscal via OpenAI"):
            with st.spinner("Appel OpenAI..."):
                plan_result = call_openai(restructure_prompt)
                st.success("✅ Plan généré")
                st.text_area("📘 Plan de restructuration", plan_result, height=700)

    # Debug session state
    with st.expander("🧪 Debug"):
        st.json({k: v for k, v in st.session_state.items() if k != "mandats"})

if __name__ == "__main__":
    main()
