import customtkinter as ctk
from datetime import date
from PIL import Image
import com_sql
import tkinter as tk
from tkinter import messagebox as mb

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

def centralizar_janela(janela, largura, altura):
    janela.update_idletasks()
    x = (janela.winfo_screenwidth() // 2) - (largura // 2)
    y = (janela.winfo_screenheight() // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")


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
            mb.showinfo("Deletado", "Playlist deletada com sucesso")
            carregar_playlists()
        else:
            mb.showerror("Erro", "Erro ao deletar playlist")
    except ValueError:
        mb.showwarning("Aviso", "Código inválido")


def abrir_janela_consultas(app):
    janela = ctk.CTkToplevel()
    janela.transient(app)
    janela.grab_set()
    janela.focus_force()
    janela.title("Consulta")
    largura, altura = 1000, 600
    centralizar_janela(janela, largura, altura)
    janela.resizable(False, False)

    # ===========================
    # Consultas
    # ===========================

    def realizarconsulta1(consulta, listbox):
        listbox.delete(0, tk.END)
        resultado = com_sql.fazerConsulta(consulta)

        if not resultado:
            listbox.insert(tk.END, "⚠️ Banco indisponível ou sem músicas cadastradas")
        for m in resultado:
            texto = f"Álbum {m[0]}"
            listbox.insert(tk.END, texto)

    def realizarconsulta2(consulta, listbox):
        listbox.delete(0, tk.END)
        resultado = com_sql.fazerConsulta(consulta)

        if not resultado:
            listbox.insert(tk.END, "⚠️ Banco indisponível ou sem músicas cadastradas")
        for m in resultado:
            texto = f"Código da gravadora = {m[0]} | nome da gravadora = {m[1]} | qtd = {m[2]}"
            listbox.insert(tk.END, texto)

    def realizarconsulta3(consulta, listbox):
        listbox.delete(0, tk.END)
        resultado = com_sql.fazerConsulta(consulta)

        if not resultado:
            listbox.insert(tk.END, "⚠️ Banco indisponível ou sem músicas cadastradas")
        for m in resultado:
            texto = f"Nome do Compositor = {m[0]} | total_faixas = {m[1]}"
            listbox.insert(tk.END, texto)
    
    def realizarconsulta3(consulta, listbox):
        listbox.delete(0, tk.END)
        resultado = com_sql.fazerConsulta(consulta)

        if not resultado:
            listbox.insert(tk.END, "⚠️ Banco indisponível ou sem músicas cadastradas")
        for m in resultado:
            texto = f"Nome da Playlist = {m[0]}"
            listbox.insert(tk.END, texto)



    frame_dados1 = ctk.CTkFrame(janela)
    frame_dados1.columnconfigure(1, weight=1)
    frame_dados1.pack(pady=10, fill="x", padx=20)
    ctk.CTkLabel(frame_dados1, text="Albuns com valor maior que a média de todos os albuns").grid(row=0, column=0, padx=10, pady=5)

    listbox1 = tk.Listbox(
        frame_dados1,
        selectmode=tk.MULTIPLE,
        height=4,
        bg="#1e1e1e",
        fg="white"
    )

    listbox1.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    resultado1 = """
        SELECT a.decricao
        from(
            SELECT avg(a1.preco) as Media
            from album a1
            ) m, album a
        WHERE a.preco > m.Media
    """

    btn_realizarconsulta1 = ctk.CTkButton(
        frame_dados1,
        text="Realizar consulta",
        command=lambda: realizarconsulta1(resultado1, listbox1)
    )
    btn_realizarconsulta1.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")


    ################################

    frame_dados2 = ctk.CTkFrame(janela)
    frame_dados2.pack(pady=10, fill="x", padx=20)
    frame_dados2.columnconfigure(1, weight=1)
    ctk.CTkLabel(frame_dados2, text="Nome da gravadora com maior número de playlists que possuem pelo uma faixa composta pelo compositor Dvorack.").grid(row=0, column=0, padx=10, pady=5)

    listbox2 = tk.Listbox(
        frame_dados2,
        selectmode=tk.MULTIPLE,
        height=4,
        bg="#1e1e1e",
        fg="white"
    )

    listbox2.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    resultado2 = """
    SELECT q.cod_gra, g.nome, q.Qtd_faixas_na_playlist
    FROM (
        SELECT g.cod_gra, count(*) as 'Qtd_faixas_na_playlist'
        FROM gravadora g 
        join album a on g.cod_gra =a.gravadora 
        join faixa f on a.cod_album = f.cod_album 
        join playlists p on p.cod_album = f.cod_album AND p.num_disco = f.num_disco AND p.num_faixa = f.num_faixa
        join compositores co on co.cod_album = f.cod_album AND co.num_disco = f.num_disco AND co.num_faixa = f.num_faixa
        join compositor c on co.cod_comp = c.cod_comp
        WHERE c.nome = 'Antonin Dvorak'
        group by g.cod_gra
        ) q join gravadora g on q.cod_gra = g.cod_gra

    WHERE q.Qtd_faixas_na_playlist >= ALL (
                                    SELECT count(*) as 'Qtd_faixas_na_playlist'
                                    FROM gravadora g2 
                                    join album a2 on g2.cod_gra =a2.gravadora 
                                    join faixa f2 on a2.cod_album = f2.cod_album 
                                    join playlists p2 on p2.cod_album = f2.cod_album AND p2.num_disco = f2.num_disco AND p2.num_faixa = f2.num_faixa
                                    join compositores co2 on co2.cod_album = f2.cod_album AND co2.num_disco = f2.num_disco AND co2.num_faixa = f2.num_faixa
                                    join compositor c2 on co2.cod_comp = c2.cod_comp
                                    WHERE c2.nome = 'Antonin Dvorak'
                                    group by g2.cod_gra
                                    )
    """

    btn_realizarconsulta2 = ctk.CTkButton(
        frame_dados2,
        text="Realizar consulta",
        command=lambda: realizarconsulta2(resultado2, listbox2)
    )
    btn_realizarconsulta2.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")

    ####################################

    frame_dados3 = ctk.CTkFrame(janela)
    frame_dados3.pack(pady=10, fill="x", padx=20)
    ctk.CTkLabel(frame_dados3, text="Compositor com mais faixas nas playlists").grid(row=0, column=0, padx=10, pady=5)

    frame_dados3.columnconfigure(1, weight=1)

    listbox3 = tk.Listbox(
        frame_dados3,
        selectmode=tk.MULTIPLE,
        height=4,
        bg="#1e1e1e",
        fg="white"
    )
    listbox3.configure(width=60)
    listbox3.grid(row=1, column=0, padx=10, pady=10)

    resultado3 = """
    SELECT c.nome as nome_compositor, COUNT(*) as total_faixas
    FROM compositor c
        JOIN compositores cf ON cf.cod_comp = c.cod_comp
        JOIN playlists fp ON fp.num_faixa= cf.num_faixa
        AND fp.cod_album = cf.cod_album
        AND fp.num_disco = cf.num_disco
    GROUP BY c.cod_comp, c.nome
    HAVING COUNT(*) >= ALL (SELECT MAX(qtd_faixas)
                            FROM (	SELECT COUNT(*) as qtd_faixas
                                    FROM compositores cf2
                                        JOIN playlists fp2 ON fp2.num_faixa = cf2.num_faixa
                                        AND fp2.cod_album    = cf2.cod_album
                                        AND fp2.num_disco = cf2.num_disco
                                    GROUP BY cf2.cod_comp) s)

    """

    btn_realizarconsulta3 = ctk.CTkButton(
        frame_dados3,
        text="Realizar consulta",
        command=lambda: realizarconsulta3(resultado3, listbox3)
    )

    btn_realizarconsulta3.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")

    ###############################

    frame_dados4 = ctk.CTkFrame(janela)
    frame_dados4.pack(pady=10, fill="x", padx=20)
    frame_dados4.columnconfigure(1, weight=1)
    ctk.CTkLabel(frame_dados4, text="Todas playlist que todas as faixas sao do periodo Barroco e tipo de composicao Concerto").grid(row=0, column=0, padx=10, pady=5)

    listbox4 = tk.Listbox(
        frame_dados4,
        selectmode=tk.MULTIPLE,
        height=4,
        bg="#1e1e1e",
        fg="white"
    )

    listbox4.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    resultado4 = """
    SELECT play.nome
    FROM playlist play
    WHERE NOT EXISTS(
        SELECT *
        FROM playlists p join playlist pl on pl.cod_play = p.cod_play join faixa f on f.cod_album = p.cod_album AND f.num_disco = p.num_disco AND f.num_faixa = p.num_faixa join tipo_comp tc on f.tipo_composicao = tc.cod_tipo
            join compositores co on co.cod_album = f.cod_album AND co.num_disco = f.num_disco AND co.num_faixa = f.num_faixa join compositor c on co.cod_comp = c.cod_comp join periodo per on c.periodo = per.cod_per

        WHERE play.cod_play = pl.cod_play AND (per.descricao <> 'Barroco' OR tc.descricao <> 'Concerto')
    )
    """

    btn_realizarconsulta4 = ctk.CTkButton(
        frame_dados4,
        text="Realizar consulta",
        command=lambda: realizarconsulta3(resultado4, listbox4)
    )

    btn_realizarconsulta4.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")




def abrir_janela_criar_playlist(app):
    janela = ctk.CTkToplevel()
    janela.transient(app)
    janela.grab_set()
    janela.focus_force()
    janela.title("Criar Playlist")
    largura, altura = 800, 600
    centralizar_janela(janela, largura, altura)
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
            mb.showerror("Erro", "Dê um nome a sua playlist.")
            return

        cod_play = entry_cod.get()
        if not cod_play.isdigit():
            return
        cod_play = int(cod_play)

        data = date.today()

        criou = com_sql.criarPlaylist(cod_play, nome, data)

        if criou:
            selecionadas = listbox.curselection()
            for i in selecionadas:
                cod_album, num_disco, num_faixa, _ = musicas[i]
                com_sql.adicionarFaixasPlaylist(
                    num_faixa, cod_album, num_disco, cod_play
                )

            carregar_playlists()
            mb.showinfo("Sucesso", "Playlist criada com sucesso")
            janela.destroy()
        else:
            mb.showerror("Erro", "Erro na criacao da playlist!")
            return

    btn_salvar = ctk.CTkButton(
        janela,
        text="Salvar Playlist",
        command=salvar_playlist
    )
    btn_salvar.pack(pady=10)

def abrir_janela_editar_playlist(app):
    janela = ctk.CTkToplevel()
    janela.transient(app)
    janela.grab_set()
    janela.focus_force()
    janela.title("Editar Playlist")
    largura, altura = 900, 600
    centralizar_janela(janela, largura, altura)
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

        carregar_playlists()
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
            mb.showwarning("Aviso", "Essa música já está na playlist")
            return

        com_sql.adicionarFaixasPlaylist(
            musica[2], musica[0], musica[1], cod_play
        )

        carregar_playlists()
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
    largura, altura = 900, 600
    centralizar_janela(app, largura, altura)
    app.resizable(False, False)

    imagem_logo = ctk.CTkImage(
        light_image=Image.open("imgs/logo-sFundo.png"),
        dark_image=Image.open("imgs/logo-sFundo.png"),
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
        command=lambda: abrir_janela_criar_playlist(app)
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
        command=lambda: abrir_janela_editar_playlist(app)
    ).grid(row=0, column=3, padx=10)

    ctk.CTkButton(
        frame_botoes,
        text ='Consultas',
        command=lambda: abrir_janela_consultas(app)
    ).grid(row=0, column=4, padx=10)

    lista_playlists = ctk.CTkTextbox(app, width=800, height=250)
    lista_playlists.pack(pady=20)

    app.mainloop()
