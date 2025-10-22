"""
Streamlit dashboard for Quebec Market Trends visualization.
Interactive dashboard for analyzing furniture, appliances, mattresses, and flooring trends.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from pathlib import Path
import yaml
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.data_collection.database import TrendsDatabase
from src.data_collection.trends_collector import QuebecTrendsCollector


# Page configuration
st.set_page_config(
    page_title="Analyse de Tendances - Marché Québécois",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_config():
    """Load configuration file."""
    config_path = Path("config/config.yaml")
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


@st.cache_resource
def get_database():
    """Get database instance."""
    config = load_config()
    return TrendsDatabase(config['database']['path'])


@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_trends_data(keywords=None, category=None, days_back=365):
    """Load trends data from database."""
    db = get_database()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)

    data = db.get_trends_data(
        keywords=keywords,
        category=category,
        start_date=start_date.strftime('%Y-%m-%d'),
        end_date=end_date.strftime('%Y-%m-%d')
    )
    return data


def main():
    """Main dashboard application."""

    # Header
    st.markdown('<div class="main-header">📊 Analyse de Tendances - Marché Québécois</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Meubles • Électroménagers • Matelas • Couvre-planchers</div>', unsafe_allow_html=True)

    # Load configuration and database
    config = load_config()
    db = get_database()

    # Sidebar
    st.sidebar.title("⚙️ Contrôles")

    # Data collection section
    st.sidebar.header("📥 Collecte de données")

    if st.sidebar.button("🔄 Collecter nouvelles données", help="Lance une collecte complète"):
        with st.spinner("Collection en cours... Cela peut prendre quelques minutes."):
            try:
                collector = QuebecTrendsCollector()
                stats = collector.collect_all_categories()

                st.sidebar.success(f"✅ Collection terminée!")
                st.sidebar.info(f"📊 {stats['total_records']} enregistrements ajoutés")
                st.sidebar.info(f"⏱️ Durée: {stats['duration_seconds']:.1f}s")

                # Clear cache to reload data
                st.cache_data.clear()

            except Exception as e:
                st.sidebar.error(f"❌ Erreur: {e}")

    # Database statistics
    st.sidebar.header("📈 Statistiques")
    stats = db.get_summary_stats()

    st.sidebar.metric("Total d'enregistrements", f"{stats['total_records']:,}")
    st.sidebar.metric("Mots-clés uniques", stats['unique_keywords'])

    if stats['last_successful_collection']:
        last_coll = datetime.fromisoformat(stats['last_successful_collection'])
        st.sidebar.metric("Dernière collecte", last_coll.strftime('%Y-%m-%d %H:%M'))

    # Filters
    st.sidebar.header("🔍 Filtres")

    # Category filter
    categories = list(config['keywords'].keys())
    category_labels = {
        'meubles': '🛋️ Meubles',
        'electromenagers': '🔌 Électroménagers',
        'matelas': '🛏️ Matelas',
        'couvre_planchers': '🏠 Couvre-planchers'
    }

    selected_categories = st.sidebar.multiselect(
        "Catégories",
        options=categories,
        default=categories,
        format_func=lambda x: category_labels.get(x, x)
    )

    # Time range filter
    time_ranges = {
        "7 derniers jours": 7,
        "30 derniers jours": 30,
        "3 derniers mois": 90,
        "6 derniers mois": 180,
        "1 an": 365
    }

    selected_range = st.sidebar.selectbox(
        "Période",
        options=list(time_ranges.keys()),
        index=4  # Default to 1 year
    )

    days_back = time_ranges[selected_range]

    # Main content area
    if stats['total_records'] == 0:
        st.warning("⚠️ Aucune donnée dans la base. Cliquez sur 'Collecter nouvelles données' dans la barre latérale.")
        st.info("💡 La première collecte prendra quelques minutes pour récupérer 12 mois de données.")
        return

    # Load data for selected categories
    data_frames = []
    for category in selected_categories:
        df = load_trends_data(category=category, days_back=days_back)
        if not df.empty:
            data_frames.append(df)

    if not data_frames:
        st.warning("Aucune donnée disponible pour les filtres sélectionnés.")
        return

    all_data = pd.concat(data_frames, ignore_index=True)

    # Tab layout
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Tendances", "🔥 Top Keywords", "📊 Comparaison", "📋 Données"])

    # Tab 1: Time series trends
    with tab1:
        st.header("Évolution des Tendances")

        # Category selector for detailed view
        view_category = st.selectbox(
            "Sélectionner une catégorie pour vue détaillée",
            options=selected_categories,
            format_func=lambda x: category_labels.get(x, x)
        )

        category_data = all_data[all_data['category'] == view_category]

        if not category_data.empty:
            # Line chart with all keywords in category
            fig = px.line(
                category_data,
                x='date',
                y='interest',
                color='keyword',
                title=f"Intérêt au fil du temps - {category_labels[view_category]}",
                labels={'interest': 'Intérêt relatif', 'date': 'Date', 'keyword': 'Mot-clé'},
                height=500
            )

            fig.update_layout(
                hovermode='x unified',
                legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02)
            )

            st.plotly_chart(fig, use_container_width=True)

            # Show trend summary
            col1, col2, col3 = st.columns(3)

            with col1:
                avg_interest = category_data['interest'].mean()
                st.metric("Intérêt moyen", f"{avg_interest:.1f}")

            with col2:
                max_interest = category_data['interest'].max()
                max_keyword = category_data[category_data['interest'] == max_interest]['keyword'].iloc[0]
                st.metric("Pic d'intérêt", f"{max_interest} ({max_keyword})")

            with col3:
                unique_keywords = category_data['keyword'].nunique()
                st.metric("Mots-clés suivis", unique_keywords)

    # Tab 2: Top keywords
    with tab2:
        st.header("Top Mots-clés par Catégorie")

        # Calculate average interest per keyword over the period
        for category in selected_categories:
            category_data = all_data[all_data['category'] == category]

            if not category_data.empty:
                st.subheader(category_labels.get(category, category))

                # Calculate average and max interest
                keyword_stats = category_data.groupby('keyword').agg({
                    'interest': ['mean', 'max']
                }).round(1)

                keyword_stats.columns = ['Intérêt moyen', 'Intérêt max']
                keyword_stats = keyword_stats.sort_values('Intérêt moyen', ascending=False)

                # Bar chart
                fig = go.Figure()

                fig.add_trace(go.Bar(
                    x=keyword_stats.index,
                    y=keyword_stats['Intérêt moyen'],
                    name='Moyenne',
                    marker_color='lightblue'
                ))

                fig.add_trace(go.Bar(
                    x=keyword_stats.index,
                    y=keyword_stats['Intérêt max'],
                    name='Maximum',
                    marker_color='darkblue'
                ))

                fig.update_layout(
                    barmode='group',
                    height=400,
                    xaxis_tickangle=-45,
                    showlegend=True
                )

                st.plotly_chart(fig, use_container_width=True)

                # Show table
                with st.expander("📋 Voir les détails"):
                    st.dataframe(keyword_stats, use_container_width=True)

    # Tab 3: Category comparison
    with tab3:
        st.header("Comparaison entre Catégories")

        # Calculate average interest per category over time
        category_comparison = all_data.groupby(['date', 'category'])['interest'].mean().reset_index()

        fig = px.line(
            category_comparison,
            x='date',
            y='interest',
            color='category',
            title="Comparaison de l'intérêt par catégorie",
            labels={'interest': 'Intérêt moyen', 'date': 'Date', 'category': 'Catégorie'},
            height=500
        )

        fig.update_layout(hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)

        # Category statistics
        st.subheader("Statistiques par Catégorie")

        cols = st.columns(len(selected_categories))

        for idx, category in enumerate(selected_categories):
            with cols[idx]:
                cat_data = all_data[all_data['category'] == category]
                avg_interest = cat_data['interest'].mean()

                st.markdown(f"**{category_labels.get(category, category)}**")
                st.metric("Intérêt moyen", f"{avg_interest:.1f}")

                # Calculate trend (last 30 days vs previous 30 days)
                if len(cat_data) > 60:
                    recent_avg = cat_data.nlargest(30, 'date')['interest'].mean()
                    older_avg = cat_data.nlargest(60, 'date').nsmallest(30, 'date')['interest'].mean()
                    trend = ((recent_avg - older_avg) / older_avg * 100) if older_avg > 0 else 0
                    st.metric("Tendance 30j", f"{trend:+.1f}%")

    # Tab 4: Raw data
    with tab4:
        st.header("Données Brutes")

        st.dataframe(
            all_data.sort_values('date', ascending=False),
            use_container_width=True,
            height=500
        )

        # Download button
        csv = all_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Télécharger les données (CSV)",
            data=csv,
            file_name=f"trends_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

    # Footer
    st.markdown("---")
    st.markdown(
        f"<div style='text-align: center; color: #666;'>"
        f"Dernière mise à jour: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
        f"Total: {len(all_data):,} enregistrements"
        f"</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
