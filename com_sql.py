import pyodbc


def conectarBD():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=SpotPer;"
        "TrustServerCertificate=yes;"
        "Trusted_Connection=yes;"
    )


def fazerConsulta(consulta, param=None):
    try:
        with conectarBD() as con:
            cursor = con.cursor()
            if param:
                cursor.execute(consulta, param)
            else:
                cursor.execute(consulta)
            return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao consultar: {e}")
        return []


def executarAcao(comando, param=None):
    try:
        with conectarBD() as con:
            cursor = con.cursor()
            if param:
                cursor.execute(comando, param)
            else:
                cursor.execute(comando)
            con.commit()
            return True
    except Exception as e:
        print(f"Erro ao executar ação: {e}")
        return False


def adicionarFaixasPlaylist(num_faixa, cod_album, num_disco, cod_play):
    return executarAcao(
        "INSERT INTO playlists "
        "(num_faixa, cod_album, num_disco, cod_play, vezes_tocada, ultima_vez_tocada) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (num_faixa, cod_album, num_disco, cod_play, 0, None)
    )


def criarPlaylist(codPlay, nome, dt_criacao):
    return executarAcao(
        "INSERT INTO PLAYLIST (cod_play, nome, dt_criacao) VALUES (?,?,?)",
        (codPlay, nome, dt_criacao)
    )


def deletaPlaylist(cod_play):
    return executarAcao(
        "DELETE FROM Playlist WHERE cod_play = ?",
        (cod_play,)
    )


def listarPlaylist():
    return fazerConsulta("""
                         select p.cod_play, pl.nome , pl.dt_criacao, sum(f.tempo) as 'Tempo_playlist'
                        from faixa f join playlists p on f.cod_album = p.cod_album AND f.num_disco = p.num_disco AND f.num_faixa = p.num_faixa join playlist pl on p.cod_play = pl.cod_play 
                        group by p.cod_play, pl.nome, pl.dt_criacao
                         """)

def gerarNovoCodigoPlaylist():
    resultado = fazerConsulta("SELECT COUNT(*) FROM playlist")

    # Se não conseguiu consultar (erro de conexão)
    if not resultado:
        return "0001"

    quantidade = resultado[0][0] + 1
    return f"{quantidade:04d}"

def listarMusicasDaPlaylist(cod_play):
    return fazerConsulta(
        """
        SELECT f.cod_album, f.num_disco, f.num_faixa, f.descricao
        FROM playlists p
        JOIN faixa f
            ON p.cod_album = f.cod_album
           AND p.num_disco = f.num_disco
           AND p.num_faixa = f.num_faixa
        WHERE p.cod_play = ?
        ORDER BY f.cod_album, f.num_disco, f.num_faixa
        """,
        (cod_play,)
    )


def removerFaixaDaPlaylist(num_faixa, cod_album, num_disco, cod_play):
    return executarAcao(
        """
        DELETE FROM playlists
        WHERE num_faixa = ?
          AND cod_album = ?
          AND num_disco = ?
          AND cod_play = ?
        """,
        (num_faixa, cod_album, num_disco, cod_play)
    )


def listarTodasMusicas():
    return fazerConsulta(
        """
        SELECT cod_album, num_disco, num_faixa, descricao
        FROM faixa
        ORDER BY cod_album, num_disco, num_faixa
        """
    )
