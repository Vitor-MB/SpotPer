import customtkinter as ctk
from datetime import date
from PIL import Image
import com_sql
import tkinter as tk

# =========================
# CONFIGURAÇÃO GLOBAL
# =========================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


# =========================
# FUNÇÕES DE AÇÃO
# =========================

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


def criar_playlist():
    try:
        cod = int(entry_cod.get())
        nome = entry_nome.get()
        data_criacao = date.today()
        tempo = 0

        sucesso = com_sql.criarPlaylist(cod, nome, data_criacao, tempo)

        if sucesso:
            lista_playlists.insert("end", f"\nPlaylist '{nome}' criada com sucesso!\n")
        else:
            lista_playlists.insert("end", "\nErro ao criar playlist.\n")

    except ValueError:
        lista_playlists.insert("end", "\nCódigo deve ser numérico.\n")
    except Exception as e:
        lista_playlists.insert("end", f"\nErro: {e}\n")


def deletar_playlist():
    try:
        cod = int(entry_cod.get())
        sucesso = com_sql.deletaPlaylist(cod)

        if sucesso:
            lista_playlists.insert("end", f"\nPlaylist {cod} removida.\n")
        else:
            lista_playlists.insert("end", "\nErro ao remover playlist.\n")

    except ValueError:
        lista_playlists.insert("end", "\nInforme um código válido.\n")


# =========================
# INTERFACE GRÁFICA
# =========================

def iniciar_app():
    global entry_cod, entry_nome, lista_playlists

    app = ctk.CTk()
    app.title("SpotPer 🎵")
    app.geometry("900x600")
    app.resizable(False, False)

    imagem_fundo = ctk.CTkImage(
        light_image=Image.open("fundo.jpg"),
        dark_image=Image.open("fundo.jpg"),
        size=(900, 600)
    )

    fundo = ctk.CTkLabel(
        app,
        image=imagem_fundo,
        text=""
    )
    fundo.place(x=0, y=0)
    fundo.lower()

    # -------------------------
    # TÍTULO
    # -------------------------
    titulo = ctk.CTkLabel(
        app,
        text="SpotPer",
        font=("Arial", 28, "bold")
    )
    titulo.pack(pady=20)

    # -------------------------
    # FRAME DE FORMULÁRIO
    # -------------------------
    frame_form = ctk.CTkFrame(app)
    frame_form.pack(pady=10)

    lbl_cod = ctk.CTkLabel(frame_form, text="Código da Playlist:")
    lbl_cod.grid(row=0, column=0, padx=10, pady=10, sticky="e")

    entry_cod = ctk.CTkEntry(frame_form, width=200)
    entry_cod.grid(row=0, column=1, padx=10, pady=10)

    lbl_nome = ctk.CTkLabel(frame_form, text="Nome da Playlist:")
    lbl_nome.grid(row=1, column=0, padx=10, pady=10, sticky="e")

    entry_nome = ctk.CTkEntry(frame_form, width=200)
    entry_nome.grid(row=1, column=1, padx=10, pady=10)

    # -------------------------
    # BOTÕES
    # -------------------------
    frame_botoes = ctk.CTkFrame(app)
    frame_botoes.pack(pady=10)

    def abrir_janela_criar_playlist():
        janela = ctk.CTkToplevel()
        janela.title("Criar Playlist")
        janela.geometry("800x600")
        janela.resizable(False, False)
        frame_dados = ctk.CTkFrame(janela, fg_color="#1e1e1e")
        frame_dados.pack(pady=15, fill="x", padx=20)

        ctk.CTkLabel(frame_dados, text="Código da Playlist").grid(row=0, column=0, padx=10, pady=5)
        entry_cod = ctk.CTkEntry(frame_dados)
        entry_cod.grid(row=0, column=1)

        ctk.CTkLabel(frame_dados, text="Nome da Playlist").grid(row=1, column=0, padx=10, pady=5)
        entry_nome = ctk.CTkEntry(frame_dados)
        entry_nome.grid(row=1, column=1)

        ctk.CTkLabel(frame_dados, text="Data de Criação (YYYY-MM-DD)").grid(row=2, column=0, padx=10, pady=5)
        entry_data = ctk.CTkEntry(frame_dados)
        entry_data.grid(row=2, column=1)

        frame_musicas = ctk.CTkFrame(janela, fg_color="#2a2a2a")
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

        musicas = com_sql.fazerConsulta("""
            SELECT cod_album, num_disco, num_faixa, descricao
            FROM faixa
        """)
        for m in musicas:
            texto = f"Álbum {m[0]} | Disco {m[1]} | Faixa {m[2]} - {m[3]}"
            listbox.insert(tk.END, texto)

        def salvar_playlist():
            cod = entry_cod.get()
            nome = entry_nome.get()
            data = entry_data.get()

            if not cod or not nome or not data:
                return

            com_sql.criarPlaylist(cod, nome, data, 0)

            selecionadas = listbox.curselection()
            for i in selecionadas:
                cod_album, num_disco, num_faixa, _ = musicas[i]
                com_sql.adicionarFaixasPlaylist(
                    num_faixa, cod_album, num_disco, cod
                )

            janela.destroy()

        btn_salvar = ctk.CTkButton(
            janela,
            text="Salvar Playlist",
            command=salvar_playlist
        )
        btn_salvar.pack(pady=15)


        btn_deletar = ctk.CTkButton(
            frame_botoes,
            text="Deletar Playlist",
            command=deletar_playlist,
            fg_color="#3a3a3a",
            hover_color="#5a5a5a"
        )
        btn_deletar.grid(row=0, column=1, padx=10)

        btn_listar = ctk.CTkButton(
            frame_botoes,
            text="Listar Playlists",
            command=carregar_playlists,
            fg_color="#2f2f2f",
            hover_color="#4f4f4f"
        )
        btn_listar.grid(row=0, column=2, padx=10)

        btn_criar = ctk.CTkButton(
            frame_botoes,
            text="Criar Playlist",
            command=abrir_janela_criar_playlist
        )
        btn_criar.pack(side="left", padx=10)

        # -------------------------
        # ÁREA DE RESULTADO
        # -------------------------
        lista_playlists = ctk.CTkTextbox(
            app,
            width=800,
            height=250
        )
        lista_playlists.pack(pady=20)

        lista_playlists.insert("end", "Bem-vindo ao SpotPer!\n")

        app.mainloop()
