import streamlit as st

def render_form_section():
    col_left, col_right = st.columns(2)

    with col_left:
        st.header("Objectifs de Structuration")

        objectifs_dividendes = st.text_area(
            "Maximiser les dividendes vs salaire",
            placeholder="Ex : Préférence pour les dividendes afin de réduire les charges sociales..."
        )

        objectifs_fiscaux = st.text_area(
            "Réduction des charges sociales et fiscales",
            placeholder="Ex : Passage de l'IR à l'IS, déductions fiscales, etc."
        )

        objectifs_holding = st.text_area(
            "Création d’une holding, filiales",
            placeholder="Ex : Centraliser les participations, levée de fonds, transmission facilitée..."
        )

        objectifs_transmission = st.text_area(
            "Optimisation de la transmission / succession",
            placeholder="Ex : Démembrement de propriété, préservation du patrimoine familial..."
        )

        objectifs_croissance = st.text_area(
            "Structuration pour croissance / investissement",
            placeholder="Ex : Entrée d'investisseurs, levée de fonds, création de société..."
        )

        objectifs_finance = st.text_area(
            "Optimisation de la gestion financière",
            placeholder="Ex : Réduction des coûts de financement, rentabilité opérationnelle..."
        )

    with col_right:
        st.header("Contraintes Spécifiques et Préférences")

        contraintes_temps = st.text_area(
            "Contraintes temporelles",
            placeholder="Ex : Recommandations mensuelles, entreprise récente..."
        )

        contraintes_secteur = st.text_area(
            "Contraintes sectorielles",
            placeholder="Ex : Secteur innovation, régime JEI, exonérations ZFU..."
        )

        contraintes_distribution = st.text_area(
            "Distribution & Financement",
            placeholder="Ex : Besoin de liquidités immédiates, préférence dividendes..."
        )

        contraintes_gouvernance = st.text_area(
            "Gouvernance & Transmission",
            placeholder="Ex : Holding familiale pour faciliter la succession..."
        )

        contraintes_geo = st.text_area(
            "Contraintes géographiques & juridiques",
            placeholder="Ex : Activités internationales, implantation en ZFU..."
        )

    return {
        "objectifs": {
            "dividendes": objectifs_dividendes,
            "fiscaux": objectifs_fiscaux,
            "holding": objectifs_holding,
            "transmission": objectifs_transmission,
            "croissance": objectifs_croissance,
            "finance": objectifs_finance,
        },
        "contraintes": {
            "temps": contraintes_temps,
            "secteur": contraintes_secteur,
            "distribution": contraintes_distribution,
            "gouvernance": contraintes_gouvernance,
            "geo": contraintes_geo,
        }
    }
