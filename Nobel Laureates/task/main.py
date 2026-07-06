import numpy as np
import pandas as pd
import re


def extract_country(series):
    if series is np.nan or "," not in series:
        return None
    if series:
        return series.split(',')[-1].strip()


def extract_year(series):
    template_1 = r"\d{1,2} [A-z]+ \d{4}"
    template_2 = r"\d{4}-\d{1,2}-\d{1,2}"
    template_3 = r"[A-z]+ \d{1,2}, \d{4}"
    template_4 = r"\d{4}"
    if re.match(template_1, series) or re.match(template_3, series):
        return series[-4:]
    elif re.match(template_2, series):
        return series[:4]
    elif re.match(template_4, series):
        return series
    return None


def generate_pie_chart(df):
    """
        Plot the exact pie chart as depicted below, using the country of birth information.

        Re-code the countries. If the number of the Nobel Laureates born in the country is
        less than 25, re-code it to the Other countries group;

        Use the following colors: blue, orange, red, yellow, green, pink, brown, cyan, purple;

        Set figure size to (12, 12);

        For countries whose slices are exploded, set the explode parameter to 0.08.

        Tip: Use autopct parameter to calculate and format the values. The format of the
        text displayed on the slices is {:.2f}%\n({:.0f}).
        """

    colors = ['blue', 'orange', 'red', 'yellow', 'green', 'pink', 'brown', 'cyan', 'purple']

    counts = df['born_in'].value_counts()
    threshold = 25
    df['born_in'] = df['born_in'].map(lambda x: x if counts[x] >= threshold else 'Other countries')

    labels = df['born_in'].value_counts().index.tolist()
    explode = [0, 0, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08]
    plt.figure(figsize=(12, 12))

    # Preciso criar uma função para passar para autopct
    data_values = df['born_in'].value_counts()
    total = sum(data_values)
    custom_calc = lambda p: '{:.2f}%\n({:.0f})'.format(p, p * total / 100)
    plt.pie(df['born_in'].value_counts()
            , colors=colors
            , explode=explode
            , labels=labels
            , autopct=custom_calc)

    plt.show()


def generate_bar_plot(df):
    """
    Drop all the rows where the category column does not contain any values.

    Set figure size to (10, 10);

    The bar centers are moved by 0.2 from the tick center, the width of bars is 0.4;

    The bars corresponding to males and females are of "blue" and "crimson" colours respectively;

    The axis font size is 14, the plot font size is 20.
    """

    df['category'] = np.where(df["category"] == "", None, df["category"])
    df = df.dropna(subset=['category'])

    categories = df['category'].value_counts().sort_index().index
    height_male = (df['category'][df['gender'] == 'male']).value_counts().sort_index()
    height_female = (df['category'][df['gender'] == 'female']).value_counts().sort_index()

    x_axis = np.arange(len(categories))

    plt.figure(figsize=(10, 6))
    plt.xticks(x_axis, categories)

    plt.bar(x=x_axis - 0.2, height=height_male, width=0.4, label='Males', color='blue')
    plt.bar(x=x_axis + 0.2, height=height_female, width=0.4, label='Females', color='crimson')

    plt.xlabel('Category', fontsize=14)
    plt.ylabel('Nobel Laureates Count', fontsize=14)
    plt.title("The total count of male and female Nobel Prize winners by categories", fontsize=20)

    plt.legend()
    plt.show()


def generate_box_plot(df):
    """
    Generate a box plot for ages of getting the Nobel Prize for each category:

    Set figure size to (10, 10);

    Set the font size of the axis labels to 14 and the font size of the plot label is 20;

    Display the mean age of obtaining the Nobel Prize in each category (green triangle in the image below).
    """

    df['category'] = np.where(df["category"] == "", None, df["category"])
    df = df.dropna(subset=['category'])

    categories = sorted(df['category'].unique())
    # print(categories)

    dados_por_categoria = [df[df['category'] == cat]['age'].values for cat in categories]
    dados_por_categoria.append(df['age'].values.tolist())

    boxprops = {'facecolor': 'white'}
    meanprops = {'color': 'g', 'marker': '^', 'markerfacecolor': 'g'}
    categories.append("All categories")

    plt.figure(figsize=(14, 10))
    plt.boxplot(dados_por_categoria, patch_artist=True, boxprops=boxprops,
                tick_labels=categories, showmeans=True, meanprops=meanprops)

    plt.title('Distribution of Ages by Category', fontsize=20)
    plt.ylabel('Age Of Obtaining the Nobel Prize', fontsize=14)

    plt.show()


if __name__ == "__main__":
    df = pd.read_json('data/nobel_laureates.json')

    df.dropna(subset=['gender'], inplace=True)
    df.reset_index(inplace=True, drop=True)

    df['place_of_birth'] = df['place_of_birth'].apply(extract_country)
    df['born_in'] = np.where(df["born_in"] == "", df["place_of_birth"], df["born_in"])

    df[['born_in', 'place_of_birth']] = df[['born_in', 'place_of_birth']].replace(['US', 'United States', 'U.S.'],
                                                                                  'USA')
    df[['born_in', 'place_of_birth']] = df[['born_in', 'place_of_birth']].replace('United Kingdom', 'UK')
    df.dropna(subset=['born_in'], inplace=True)
    # print(df['born_in'].tolist())

    """
    The dates of birth are present in 4 formats: 26 April 1932, 1951-3-26, December 13, 1923,
    and, 1950. Generate a new column, representing the year each Nobel Laureate was born.

    Create a new column, representing the age of winning the prize. It is the year of
     winning the prize minus the year of birth."""

    df['year_of_birth'] = df['date_of_birth'].apply(extract_year)
    df.dropna(subset=['year_of_birth'], inplace=True)
    df['age'] = df['year'].astype(int) - df['year_of_birth'].astype(int)
    # print(df['year_of_birth'].astype(int).tolist())
    # print(df['age'].tolist())

    import matplotlib.pyplot as plt

    generate_pie_chart(df)
    generate_bar_plot(df)
    generate_box_plot(df)
