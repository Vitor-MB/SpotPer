CREATE VIEW [dbo].[AlbunsPlaylist]
WITH SCHEMABINDING
AS
    SELECT 
        p.cod_play, f.cod_album,
        p.nome AS nome_playlist,
        COUNT_BIG(*) AS qtd_faixas
    FROM dbo.playlist p
    JOIN dbo.playlists fp 
        ON p.cod_play = fp.cod_play
    JOIN dbo.faixa f
        ON f.cod_album = fp.cod_album
       AND f.num_disco = fp.num_disco
       AND f.num_faixa = fp.num_faixa
    GROUP BY p.cod_play, p.nome, f.cod_album;
GO

CREATE UNIQUE CLUSTERED INDEX I_AlbunsPlaylist
ON dbo.AlbunsPlaylist(cod_play, cod_album);
GO

CREATE VIEW [dbo].[vw_playlist_album_count]
WITH SCHEMABINDING
AS
SELECT 
    p.cod_play,
    p.nome_playlist AS nome_playlist,
    COUNT(*) AS qtd_albuns
FROM dbo.AlbunsPlaylist as p
GROUP BY p.cod_play, p.nome_playlist;
GO