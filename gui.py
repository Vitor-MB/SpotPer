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

        com_sql.criarPlaylist(cod_play, nome, data, 200)

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

def abrir_janela_editar_playlist():
    janela = ctk.CTkToplevel()
    janela.title("Editar Playlist")
    janela.geometry("900x600")
    janela.resizable(False, False)

    playlist_selecionada = {"cod": None}

    frame_playlists = ctk.CTkFrame(janela)
    frame_playlists.pack(side="left", fill="y", padx=10, pady=10)

    frame_musicas = ctk.CTkFrame(janela)
    frame_musicas.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    # ================= PLAYLISTS =================
    ctk.CTkLabel(frame_playlists, text="Playlists").pack(pady=5)

    listbox_playlists = tk.Listbox(
        frame_playlists,
        height=25,
        bg="#1e1e1e",
        fg="white",
        exportselection=False
    )
    listbox_playlists.pack(padx=10, pady=10)

    playlists = com_sql.listarPlaylist()
    for p in playlists:
        listbox_playlists.insert(tk.END, f"{p[0]} - {p[1]}")

    # ================= MUSICAS DA PLAYLIST =================
    ctk.CTkLabel(frame_musicas, text="Músicas da Playlist").pack()

    listbox_playlist = tk.Listbox(
        frame_musicas,
        bg="#1e1e1e",
        fg="white",
        height=10,
        exportselection=False
    )
    listbox_playlist.pack(fill="x", padx=10)

    btn_remover = ctk.CTkButton(
        frame_musicas,
        text="Remover música da playlist",
        state="disabled"
    )
    btn_remover.pack(pady=5)

    # ================= TODAS MUSICAS =================
    ctk.CTkLabel(frame_musicas, text="Todas as músicas").pack(pady=5)

    listbox_todas = tk.Listbox(
        frame_musicas,
        bg="#1e1e1e",
        fg="white",
        height=10,
        exportselection=False
    )
    listbox_todas.pack(fill="x", padx=10)

    btn_adicionar = ctk.CTkButton(
        frame_musicas,
        text="Adicionar música à playlist",
        state="disabled"
    )
    btn_adicionar.pack(pady=5)

    todas_musicas = com_sql.listarTodasMusicas()
    for m in todas_musicas:
        listbox_todas.insert(
            tk.END,
            f"Álbum {m[0]} | Disco {m[1]} | Faixa {m[2]} - {m[3]}"
        )

    # ================= FUNÇÕES =================
    def carregar_musicas_playlist(event):
        listbox_playlist.delete(0, tk.END)
        btn_remover.configure(state="disabled")
        btn_adicionar.configure(state="disabled")

        sel = listbox_playlists.curselection()
        if not sel:
            return

        cod = int(listbox_playlists.get(sel).split(" - ")[0])
        playlist_selecionada["cod"] = cod

        musicas = com_sql.listarMusicasDaPlaylist(cod)
        for m in musicas:
            listbox_playlist.insert(
                tk.END,
                f"Álbum {m[0]} | Disco {m[1]} | Faixa {m[2]} - {m[3]}"
            )

    def selecionar_musica_playlist(event):
        if playlist_selecionada["cod"] is not None:
            btn_remover.configure(state="normal")

    def selecionar_musica_todas(event):
        if playlist_selecionada["cod"] is not None:
            btn_adicionar.configure(state="normal")

    def remover_musica():
        i = listbox_playlist.curselection()
        if not i:
            return

        cod_play = playlist_selecionada["cod"]
        musica = com_sql.listarMusicasDaPlaylist(cod_play)[i[0]]

        com_sql.removerFaixaDaPlaylist(
            musica[2], musica[0], musica[1], cod_play
        )

        carregar_musicas_playlist(None)

    def adicionar_musica():
        i = listbox_todas.curselection()
        if not i:
            return

        cod_play = playlist_selecionada["cod"]
        musica = todas_musicas[i[0]]

        # REGRA: não duplicar
        existentes = com_sql.listarMusicasDaPlaylist(cod_play)
        if any(
            m[0] == musica[0] and m[1] == musica[1] and m[2] == musica[2]
            for m in existentes
        ):
            messagebox.showwarning("Aviso", "Essa música já está na playlist")
            return

        com_sql.adicionarFaixasPlaylist(
            musica[2], musica[0], musica[1], cod_play
        )

        carregar_musicas_playlist(None)

    # ================= BINDS =================
    listbox_playlists.bind("<<ListboxSelect>>", carregar_musicas_playlist)
    listbox_playlist.bind("<<ListboxSelect>>", selecionar_musica_playlist)
    listbox_todas.bind("<<ListboxSelect>>", selecionar_musica_todas)

    btn_remover.configure(command=remover_musica)
    btn_adicionar.configure(command=adicionar_musica)

def iniciar_app():
    global entry_cod, lista_playlists

    app = ctk.CTk()
    app.title("SpotPer")
    app.geometry("900x600")
    app.resizable(False, False)

    imagem_logo = ctk.CTkImage(
        light_image=Image.open("logo-sFundo.png"),
        dark_image=Image.open("logo-sFundo.png"),
        size=(150, 150)
    )

    fundo = ctk.CTkLabel(app, image=imagem_logo, text="")
    fundo.place(x=-10, y=-10)
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

    ctk.CTkButton(
        frame_botoes,
        text="Editar Playlist",
        command=abrir_janela_editar_playlist
    ).grid(row=0, column=3, padx=10)


    lista_playlists = ctk.CTkTextbox(app, width=800, height=250)
    lista_playlists.pack(pady=20)

    app.mainloop()
