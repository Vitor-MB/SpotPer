import customtkinter as ctk
from datetime import date
from PIL import Image
import com_sql
import tkinter as tk
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


def carregar_playlists():
    lista_playlists.delete("0.0", "end")
    try:
        playlists = com_sql.listarPlaylist()
        if not playlists:
            lista_playlists.insert("end", "Nenhuma playlist cadastrada.\n")
            return

        for p in playlists:
            lista_playlists.insert(
                "end",
                f"Código: {p[0]} | Nome: {p[1]} | Criada em: {p[2]} | Tempo: {p[3]}\n"
            )
    except Exception as e:
        lista_playlists.insert("end", f"Erro ao carregar playlists:\n{e}")


def deletar_playlist():
    try:
        cod = int(entry_cod.get())
        if com_sql.deletaPlaylist(cod):
            carregar_playlists()
        else:
            messagebox.showerror("Erro", "Erro ao deletar playlist")
    except ValueError:
        messagebox.showwarning("Aviso", "Código inválido")


def abrir_janela_criar_playlist():
    janela = ctk.CTkToplevel()
    janela.title("Criar Playlist")
    janela.geometry("800x600")
    janela.resizable(False, False)

    # =========================
    # DADOS DA PLAYLIST
    # =========================
    frame_dados = ctk.CTkFrame(janela)
    frame_dados.pack(pady=10, fill="x", padx=20)

    ctk.CTkLabel(frame_dados, text="Código da Playlist").grid(row=0, column=0, padx=10, pady=5)

    entry_cod = ctk.CTkEntry(frame_dados)
    entry_cod.grid(row=0, column=1)

    # Código automático
    codigo_auto = com_sql.gerarNovoCodigoPlaylist()
    entry_cod.insert(0, codigo_auto)
    entry_cod.configure(state="disabled")

    ctk.CTkLabel(frame_dados, text="Nome da Playlist").grid(row=1, column=0, padx=10, pady=5)
    entry_nome = ctk.CTkEntry(frame_dados)
    entry_nome.grid(row=1, column=1)

    # =========================
    # LISTA DE MÚSICAS
    # =========================
    frame_musicas = ctk.CTkFrame(janela)
    frame_musicas.pack(fill="both", expand=True, padx=20, pady=10)

    ctk.CTkLabel(frame_musicas, text="Selecione as músicas").pack(pady=5)

    listbox = tk.Listbox(
        frame_musicas,
        selectmode=tk.MULTIPLE,
        height=15,
        bg="#1e1e1e",
        fg="white"
    )
    listbox.pack(fill="both", expand=True, padx=10, pady=10)

    # Buscar músicas no banco
    musicas = com_sql.fazerConsulta("""
        SELECT cod_album, num_disco, num_faixa, descricao
        FROM faixa
        ORDER BY cod_album, num_disco, num_faixa
    """)

    if not musicas:
        listbox.insert(tk.END, "⚠️ Banco indisponível ou sem músicas cadastradas")
        return

    for m in musicas:
        texto = f"Álbum {m[0]} | Disco {m[1]} | Faixa {m[2]} - {m[3]}"
        listbox.insert(tk.END, texto)

    # =========================
    # SALVAR PLAYLIST
    # =========================
    def salvar_playlist():
        nome = entry_nome.get()
        if not nome:
            return

        cod_play = entry_cod.get()
        if not cod_play.isdigit():
            return
        cod_play = int(cod_play)

        data = date.today()

        com_sql.criarPlaylist(cod_play, nome, data, 0)

        selecionadas = listbox.curselection()
        for i in selecionadas:
            cod_album, num_disco, num_faixa, _ = musicas[i]
            com_sql.adicionarFaixasPlaylist(
                num_faixa, cod_album, num_disco, cod_play
            )

        carregar_playlists()
        janela.destroy()

    btn_salvar = ctk.CTkButton(
        janela,
        text="Salvar Playlist",
        command=salvar_playlist
    )
    btn_salvar.pack(pady=10)


def iniciar_app():
    global entry_cod, lista_playlists

    app = ctk.CTk()
    app.title("SpotPer")
    app.geometry("900x600")
    app.resizable(False, False)

    imagem_fundo = ctk.CTkImage(
        light_image=Image.open("fundo.jpg"),
        dark_image=Image.open("fundo.jpg"),
        size=(900, 600)
    )

    fundo = ctk.CTkLabel(app, image=imagem_fundo, text="")
    fundo.place(x=0, y=0)
    fundo.lower()

    ctk.CTkLabel(app, text="SpotPer", font=("Arial", 28, "bold")).pack(pady=20)

    frame_form = ctk.CTkFrame(app)
    frame_form.pack(pady=10)

    ctk.CTkLabel(frame_form, text="Código da Playlist").grid(row=0, column=0, padx=10)
    entry_cod = ctk.CTkEntry(frame_form, width=200)
    entry_cod.grid(row=0, column=1, padx=10)

    frame_botoes = ctk.CTkFrame(app)
    frame_botoes.pack(pady=10)

    ctk.CTkButton(
        frame_botoes,
        text="Criar Playlist",
        command=abrir_janela_criar_playlist
    ).grid(row=0, column=0, padx=10)

    ctk.CTkButton(
        frame_botoes,
        text="Deletar Playlist",
        command=deletar_playlist
    ).grid(row=0, column=1, padx=10)

    ctk.CTkButton(
        frame_botoes,
        text="Listar Playlists",
        command=carregar_playlists
    ).grid(row=0, column=2, padx=10)

    lista_playlists = ctk.CTkTextbox(app, width=800, height=250)
    lista_playlists.pack(pady=20)

    app.mainloop()
