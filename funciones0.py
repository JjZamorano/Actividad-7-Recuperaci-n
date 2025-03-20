import pandas as pd

# cargar archivo csv o html
def cargar_archivo(nombre):
    if nombre.endswith('.csv'):
        return pd.read_csv(nombre)
    elif nombre.endswith('.html'):
        return pd.read_html(nombre)[0]
    else:
        formato = nombre.split('.')[-1]
        raise Exception(f"hola, acabas de ingresar un documento que desconozco, con extensión: .{formato}")

# verificar si es primo
def primo(n):
    if n < 2:
        return False
    for x in range(2, n):
        if n % x == 0:
            return False
    return True

# sustituir nulos
def rellenar_nulos(df):
    df2 = df.copy()
    cols = list(df2.columns)
    for i in range(len(cols)):
        c = cols[i]
        if df2[c].dtype in ['float64', 'int64']:
            if primo(i):
                df2[c] = df2[c].fillna(1111111)
            else:
                df2[c] = df2[c].fillna(1000001)
        else:
            df2[c] = df2[c].fillna('valor nulo')
    return df2

# identificar nulos
def ver_nulos(df):
    print("nulos por columna")
    print(df.isnull().sum())
    print("total de nulos:", df.isnull().sum().sum())

# función sencilla para identificar y limpiar atípicos usando Rango Intercuartílico
def limpiar_atipicos(df):
    df2 = df.copy()
    columnas = df2.select_dtypes(include=['float64', 'int64']).columns
    for col in columnas:
        q1 = df2[col].quantile(0.25)
        q3 = df2[col].quantile(0.75)
        iqr = q3 - q1
        li = q1 - 1.5 * iqr
        ls = q3 + 1.5 * iqr
        df2[col] = df2[col].apply(lambda x: 'valor atipico' if x < li or x > ls else x)
        print(f"Columna procesada: {col}")
    print("Columnas numéricas procesadas:", list(columnas))
    return df2

# ejemplo de llamado para verificar funcionamiento (para guardar en llamado_de_funciones.ipynb o un script aparte)
if __name__ == "__main__":
    df = cargar_archivo("listings1.csv")
    df2 = rellenar_nulos(df)
    ver_nulos(df2)
    df2 = limpiar_atipicos(df2)
    print("DataFrame final procesado:")
    print(df2)
    df2.to_csv("dataframe_final_procesado.csv", index=False)
