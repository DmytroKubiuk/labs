import streamlit as st
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

old_indexes = {
    1: "Черкаська", 2: "Чернігівська", 3: "Чернівецька", 4: "Республіка Крим",
    5: "Дніпропетровська", 6: "Донецька", 7: "Івано-Франківська", 8: "Харківська",
    9: "Херсонська", 10: "Хмельницька", 12: "Київська", 13: "Кіровоградська",
    14: "Луганська", 15: "Львівська", 16: "Миколаївська", 17: "Одеська", 18: "Полтавська",
    19: "Рівненська", 21: "Сумська", 22: "Тернопільська", 23: "Закарпатська",
    24: "Вінницька", 25: "Волинська", 26: "Запорізька", 27: "Житомирська"
}

def read(dir):
    headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
    files = os.listdir(dir)
    dataframe = pd.DataFrame()

    for file in files:
        path = os.path.join(dir, file)
        df = pd.read_csv(path, header=1, names=headers)
        df = df.drop(df.loc[df['VHI'] == -1].index)
        df = df.drop(columns=['empty'])
        df = df.dropna()
        df['area'] = file.split("_")[2]
        df['Year'] = df['Year'].str.replace('<tt><pre>', '').str.replace('</pre></tt>', '')
        dataframe = pd.concat([dataframe, df], ignore_index=True).drop_duplicates()
    return dataframe

df = read("downloads/")

df['area'] = df['area'].astype(int)
df = df[df['area'] != 11]
df = df[df['area'] != 20]

col1, col2 = st.columns([1, 3])

with col1:
    time_series_list = ['VCI', 'TCI', 'VHI']

    if "selected_column" not in st.session_state:
        st.session_state.selected_column = time_series_list[0]

    if "selected_area" not in st.session_state:
        st.session_state.selected_area = list(old_indexes.values())[0]

    weeks = df["Week"].unique()
    min_week, max_week = int(weeks.min()), int(weeks.max())

    if "selected_weeks" not in st.session_state:
        st.session_state.selected_weeks = (min_week, max_week)

    years = df["Year"].unique()
    min_year, max_year = int(years.min()), int(years.max())

    if "selected_years" not in st.session_state:
        st.session_state.selected_years = (min_year, max_year)

    st.session_state.selected_column = st.selectbox("Оберіть часовий ряд", options=time_series_list, index=time_series_list.index(st.session_state.selected_column))

    st.session_state.selected_area = st.selectbox("Оберіть область", options=list(old_indexes.values()), index=list(old_indexes.values()).index(st.session_state.selected_area))
    selected_area_index = [index for index, area in old_indexes.items() if area == st.session_state.selected_area][0]

    st.session_state.selected_weeks = st.slider("Оберіть діапазон тижнів", min_week, max_week, st.session_state.selected_weeks)

    st.session_state.selected_years = st.slider("Оберіть діапазон років", min_year, max_year, st.session_state.selected_years)

    filtered_df = df[(df["Week"] >= st.session_state.selected_weeks[0]) & (df["Week"] <= st.session_state.selected_weeks[1]) & 
                    (df['area'].astype(int) == selected_area_index) & 
                    (df["Year"].astype(int) >= st.session_state.selected_years[0]) & (df["Year"].astype(int) <= st.session_state.selected_years[1])]
    
    if "sort_dec" not in st.session_state:
        st.session_state.sort_dec = False
    if "sort_inc" not in st.session_state:
        st.session_state.sort_inc = False

    def update_sort_dec():
        st.session_state.sort_dec = True
        st.session_state.sort_inc = False

    def update_sort_inc():
        st.session_state.sort_inc = True
        st.session_state.sort_dec = False

    st.session_state.sort_dec = st.checkbox("Сортувати за спаданням", value=st.session_state.sort_dec, on_change=update_sort_dec)
    st.session_state.sort_inc = st.checkbox("Сортувати за зростанням", value=st.session_state.sort_inc, on_change=update_sort_inc)

    if st.session_state.sort_dec:
        filtered_df = filtered_df.sort_values(by=st.session_state.selected_column, ascending=False)
    elif st.session_state.sort_inc:
        filtered_df = filtered_df.sort_values(by=st.session_state.selected_column)

    if st.button("Reset"):
        st.session_state.selected_column = time_series_list[0]
        st.session_state.selected_area = list(old_indexes.values())[0]
        st.session_state.selected_weeks = (min_week, max_week)
        st.session_state.selected_years = (min_year, max_year)
        st.session_state.sort_inc = False
        st.session_state.sort_dec = False
        st.rerun()

with col2:
    tab1, tab2, tab3 = st.tabs(["Таблиця", "Графік", "Порівняння даних по областях"])
    with tab1:
        st.write(filtered_df[['Year', 'Week', st.session_state.selected_column]])
    with tab2:
        fig, ax = plt.subplots()
        sns.lineplot(data=filtered_df, x="Year", y=st.session_state.selected_column, ax=ax)
        ax.set_ylabel(st.session_state.selected_column)
        ax.set_xlabel("Year")
        plt.xticks(rotation=90)
        st.pyplot(fig)
    with tab3:
        filtered = df[(df["Week"] >= st.session_state.selected_weeks[0]) & (df["Week"] <= st.session_state.selected_weeks[1]) & 
                    (df["Year"].astype(int) >= st.session_state.selected_years[0]) & (df["Year"].astype(int) <= st.session_state.selected_years[1])]
        
        avg_values = filtered.groupby("area")[st.session_state.selected_column].mean().reset_index()
        avg_values['area']=avg_values['area'].astype(int)
        avg_values['area'] = avg_values['area'].map(old_indexes)

        fig, ax = plt.subplots()
        sns.barplot(data=avg_values, y="area", x=st.session_state.selected_column, ax=ax)
        ax.set_ylabel("Область")
        ax.set_xlabel(f"Середнє значення {st.session_state.selected_column}")
        st.pyplot(fig)