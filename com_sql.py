import pyodbc


def conectarBD():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=DESKTOP-VVHFIP4;"
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


def criarPlaylist(codPlay, nome, dt_criacao, tempo):
    return executarAcao(
        "INSERT INTO PLAYLIST (cod_play, nome, dt_criacao, tempo) VALUES (?,?,?,?)",
        (codPlay, nome, dt_criacao, tempo)
    )


def deletaPlaylist(cod_play):
    return executarAcao(
        "DELETE FROM Playlist WHERE cod_play = ?",
        (cod_play,)
    )


def listarPlaylist():
    return fazerConsulta("SELECT * FROM Playlist")

def gerarNovoCodigoPlaylist():
    resultado = fazerConsulta("SELECT COUNT(*) FROM playlist")

    # Se não conseguiu consultar (erro de conexão)
    if not resultado:
        return "0001"

    quantidade = resultado[0][0] + 1
    return f"{quantidade:04d}"
