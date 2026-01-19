-- Albuns com valor maior que a média de todos os albuns
SELECT a.decricao
from(
	SELECT avg(a1.preco) as Media
	from album a1
	) m, album a
WHERE a.preco > m.Media

GO

--Nome da gravadora com maior numero de faixas nas playlists
SELECT q.cod_gra, g.nome, q.Qtd_faixas_na_playlist
FROM (
	SELECT g.cod_gra, count(*) as 'Qtd_faixas_na_playlist'
	FROM gravadora g 
	join album a on g.cod_gra =a.gravadora 
	join faixa f on a.cod_album = f.cod_album 
	join playlists p on p.cod_album = f.cod_album AND p.num_disco = f.num_disco AND p.num_faixa = f.num_faixa
	join playlist pl on p.cod_play = pl.cod_play
	group by g.cod_gra
	) q join gravadora g on q.cod_gra = g.cod_gra

WHERE q.Qtd_faixas_na_playlist >= ALL (
								SELECT count(*) as 'Qtd_faixas_na_playlist'
								FROM gravadora g 
								join album a on g.cod_gra =a.gravadora 
								join faixa f on a.cod_album = f.cod_album 
								join playlists p on p.cod_album = f.cod_album AND p.num_disco = f.num_disco AND p.num_faixa = f.num_faixa
								join playlist pl on p.cod_play = pl.cod_play
								group by g.cod_gra
								)




GO

--Compositor com mais faixas nas playlists
SELECT c.nome, count(*)
FROM compositores co join compositor c on co.cod_comp = c.cod_comp join faixa f on co.cod_album = f.cod_album AND co.num_disco = f.num_disco AND co.num_faixa = f.num_faixa 
	join playlists p on f.cod_album = p.cod_album AND f.num_disco = p.num_disco AND f.num_faixa = p.num_faixa join playlist pl on p.cod_play = pl.cod_play 
group by co.cod_comp, c.nome

GO
--Todas playlist que todas as faixas sao do periodo Barroco e tipo de composicao Concerto
SELECT play.nome
FROM playlist play
WHERE NOT EXISTS(
	SELECT *
	FROM playlists p join playlist pl on pl.cod_play = p.cod_play join faixa f on f.cod_album = p.cod_album AND f.num_disco = p.num_disco AND f.num_faixa = p.num_faixa join tipo_comp tc on f.tipo_composicao = tc.cod_tipo
		join compositores co on co.cod_album = f.cod_album AND co.num_disco = f.num_disco AND co.num_faixa = f.num_faixa join compositor c on co.cod_comp = c.cod_comp join periodo per on c.periodo = per.cod_per

	WHERE play.cod_play = pl.cod_play AND (per.descricao <> 'Barroco' OR tc.descricao <> 'Concerto')
)