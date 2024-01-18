import pandas as pd
import spotipy
import spotipy.util as util
from datetime import datetime
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

# Insira aqui as informações de autenticação da API do Spotify
username = "Six"
client_id = "959a10a59f78481f922c2822d3e90f46"
client_secret = "98724b1f464f4a46a819308f2f09dfdb"

#username = input("Insira seu username: ")
#client_id = input("Insira seu client ID: ")
#client_secret = input("Insira seu client secret: ")

redirect_uri = "http://localhost:8080/"

scope = "user-library-read"
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
sp = spotipy.Spotify(auth=token)

root = tk.Tk()
width = 400  # Width
height = 300  # Height

screen_width = root.winfo_screenwidth()  # Width of the screen
screen_height = root.winfo_screenheight()  # Height of the screen

# Calculate Starting X and Y coordinates for Window
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)

root.geometry('%dx%d+%d+%d' % (width, height, x, y))
root.configure(bg='white')

df = None
df2 = None

# Adicione o número total de álbuns escutados à label
total_label = tk.Label(root, text="Álbuns escutados: ", font=("Roboto", 14))
total_label.grid(row=0, column=1, padx=10, pady=20)

def escanearalbuns():
    global df
    global df2

    # Obtenha a lista de álbuns curtidos
    albums = sp.current_user_saved_albums(limit=50)
    album_list = albums["items"]

    root = tk.Tk()
    width = 300  # Width
    height = 100  # Height
    screen_width = root.winfo_screenwidth()  # Width of the screen
    screen_height = root.winfo_screenheight()  # Height of the screen

    # Calculate Starting X and Y coordinates for Window
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)

    root.geometry('%dx%d+%d+%d' % (width, height, x, y))
    root.configure(bg='white')
    root.title("Escaneando álbuns")
    progress = ttk.Progressbar(root, orient="horizontal", length=200, mode='determinate')
    progress.pack()
    progress.start()
    while albums["next"]:
        albums = sp.next(albums)
        album_list.extend(albums["items"])
        root.update()
    progress.stop()
    root.destroy()

    # Crie um dicionário para armazenar os álbuns separados por ano de lançamento
    albums_by_year = {}
    albums_by_year2 = {}

    root = tk.Tk()
    width = 300  # Width
    height = 100  # Height
    screen_width = root.winfo_screenwidth()  # Width of the screen
    screen_height = root.winfo_screenheight()  # Height of the screen

    # Calculate Starting X and Y coordinates for Window
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)

    root.geometry('%dx%d+%d+%d' % (width, height, x, y))
    root.configure(bg='white')
    root.title("Finalizando")
    progress = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
    progress.pack()

    # Atualize a barra de progresso enquanto o loop é executado
    progress["value"] = 0
    progress["maximum"] = len(album_list)
    for i, album in enumerate(album_list):
        release_date = album["album"]["release_date"]
        year = int(release_date[:4])
        if year not in albums_by_year:
            albums_by_year[year] = []
        albums_by_year[year].append(album["album"]["name"])
        progress["value"] = i + 1
        root.update()

    # Para cada álbum na lista, adicione 1 ao ano correspondente na contagem do dicionário
    for album in album_list:
        release_date = album["album"]["release_date"]
        year = int(release_date[:4])
        if year not in albums_by_year2:
            albums_by_year2[year] = 0
        albums_by_year2[year] += 1

    # Atualize a label com o número total de álbuns escutados
    total_label["text"] = "Álbuns escutados: " + str(len(album_list))

    root.destroy()

    # Imprima a lista de álbuns separados por ano de lançamento em ordem cronológica
    for year in sorted(albums_by_year.keys()):
        print(f"Álbuns de {year}:")
        for album in albums_by_year[year]:
            print(f" - {album}")

    # Crie um DataFrame com os dados
    df = pd.DataFrame({
        "Ano": list(albums_by_year.keys()),
        "Álbuns": list(albums_by_year.values())
    })

    # Crie um DataFrame com os dados
    df2 = pd.DataFrame({
        "Ano": list(albums_by_year2.keys()),
        "Quantidade": list(albums_by_year2.values())
    })

    # Ordene o DataFrame pelo ano
    df = df.sort_values("Ano")
    df2 = df2.sort_values("Ano")


current_date = datetime.now().strftime("%d-%m-%Y")
file_name = "Álbuns por ano " + current_date + ".xlsx"


# Salve o DataFrame como uma planilha no Excel
def criaraquivoexcel():
    from tkinter import filedialog, messagebox
    import pandas as pd

    global df
    if df is None:
        messagebox.showerror("Erro", "Lista de álbuns não foi escaneada.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", initialfile=file_name)
    writer = pd.ExcelWriter(file_path, engine='openpyxl')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.save()


def graficocriar():
    from tkinter import messagebox

    global df2

    if df2 is None:
        messagebox.showerror("Erro", "Lista de álbuns não foi escaneada.")
        return

    # Crie um gráfico de barras exibindo o número de álbuns escutados por ano
    df2.plot(kind='bar', x='Ano', y='Quantidade', color='purple', figsize=(10, 5))

    # Adicione título e rótulos ao gráfico
    plt.title("Número de Albuns Escutados por Ano")
    plt.xlabel("Ano")
    plt.ylabel("Numero de Álbuns")

    # Exiba o gráfico
    plt.show()


root.title("Escaneador de álbuns")

escanear_botao = tk.Button(root, text="Escanear", height=3, width=10, command=lambda: escanearalbuns())

gerar_botao = tk.Button(root, text="Gerar", height=3, width=10, command=lambda: criaraquivoexcel(), bg='red')

grafico_botao = tk.Button(root, text="Gráfico", height=3, width=10, command=lambda: graficocriar(), bg='red')

escanear_botao.grid(row=0, column=0, padx=10, pady=20)
gerar_botao.grid(row=1, column=0, padx=10, pady=20)
grafico_botao.grid(row=3, column=0, padx=10, pady=20)

def change_button_color():
    if df is not None:
        gerar_botao.config(bg='light green')
        grafico_botao.config(bg='light green')
    root.after(1000, change_button_color)

root.after(1000, change_button_color)

root.mainloop()
