import pyodbc

def conectarBD():
    server = 'DESKTOP-VVHFIP4;'
    database = 'SpotPer;'

    return pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};' \
    'SERVER='+server+';DATABASE='+database+';TrustServerCertificate=yes;'+'Trusted_Connection=yes')

def fazerConsulta(consulta, param = None):
    try:
        with conectarBD() as con:
            with con.cursor() as cursor:
                if param:
                    cursor.execute(consulta, param)
                else:
                    cursor.execute(consulta)
                return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao consultar: {e}")
        return[]

def executarAcao(comando, param = None):
    try:
        with conectarBD() as con:
            with con.cursor() as cursor:
                if param:
                    cursor.execute(comando, param)
                else:
                    cursor.execute(comando)
                
                con.commit()
                return True
    except Exception as e:
        print(f"Erro ao exercutar acao: {e}")
        return False   
    

def modificarPlaylist(codPlay, nome, dt_criacao, tempo):
    return executarAcao('INSERT INTO PLAYLIST (cod_play, nome, dt_criacao, tempo) VALUES (?,?,?,?)',
                     (codPlay, nome, dt_criacao, tempo)
                    )

def removerFaixasPlaylist(num_faixa, cod_album, num_disco, cod_play):
    return executarAcao('DELETE FROM playlists WHERE num_faixa = ? AND cod_album = ? AND num_disco = ? AND cod_play = ?', (num_faixa, cod_album, num_disco, cod_play))

def adicionarFaixasPlaylist(num_faixa, cod_album, num_disco, cod_play):
    return executarAcao('INSERT into playlists (num_faixa, cod_album, num_disco, cod_play, vezes_tocada, ultima_vez_tocada) VALUES (?, ?, ?, ?, ?, ?)', 
                 (num_faixa, cod_album, num_disco, cod_play, 0, None))

def criarPlaylist(codPlay, nome, dt_criacao, tempo):
     return executarAcao('INSERT INTO PLAYLIST (cod_play, nome, dt_criacao, tempo) VALUES (?,?,?,?)',
                    (codPlay, nome, dt_criacao, tempo)
                 )
    
def deletaPlaylist(cod_play):
    return executarAcao('DELETE FROM Playlist where cod_play = ?', (cod_play))

def listarPlaylist():
    return fazerConsulta('SELECT * FROM playlist')

def listarMusicasPlaylist(cod_play):
    return fazerConsulta('SELECT f.cod_album, f.num_disco, f.num_faixa, f.descricao, a.decricao from playlists p join faixa f on p.cod_album = f.cod_album AND p.num_disco = f.num_disco AND p.num_faixa = f.num_faixa join album a on a.cod_album = f.cod_album WHERE p.cod_play = ? ', (cod_play))

def listarAlbuns():
    return fazerConsulta('SELECT cod_album, decricao, g.nome from album a join gravadora g on a.gravadora = g.cod_gra')

def listarMusicaAlbum(cod_album):
    return fazerConsulta('SELECT cod_album, num_disco, num_faixa from faixa f WHERE f.cod_album = ? ', (cod_album))


