-- Albuns com valor maior que a média de todos os albuns
SELECT a.decricao
from(
	SELECT avg(a1.preco) as Media
	from album a1
	) m, album a
WHERE a.preco > m.Media

GO

-- Listar nome da gravadora com maior número de playlists que possuem pelo uma faixa composta pelo compositor Dvorack.

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

GO

--Compositor com mais faixas nas playlists
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