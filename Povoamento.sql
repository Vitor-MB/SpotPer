USE SpotPer
GO

insert into gravadora values
--(cod_gra, nome, rua, bairro, cidade, estado, url)
(1, 'BS audio', 'Rua A', 'Bairro 1', 'Caucaia','CE', null),
(2, 'Audio Maker','Rua B', 'Bairro 2', 'Fortaleza','CE', 'www.AuMaker.com'),
(4, 'Best gravacoes','Rua C', 'Bairro 3', 'Sao Paulo','RJ', 'www.Bestgra.com.br')

insert into telefones_gravadora values
--(telofone, cod_gra)
(123456, 1),
(2345, 1),
(1223, 2)

insert into album values
--(cod_album, descricao, preco, dt_gravacao, dt_compra, meio_fisico, gravadora)
(1, 'Barroco Vol.1', 59.90, '2000-05-12', '2006-01-10', 'CD', 1),
(2, 'Classicas', 74.50, '2010-03-22', '2011-07-18', 'VINIL', 2),
(3, 'MPB Colecao', 95.90, '2008-08-14', '2009-09-25', 'CD', 4)

insert into periodo values
--(cod_per, descricao, ano_inicio, ano_fim)
(1, 'Barroco',1600, 1750),
(2, 'Classico',1750, 1820),
(3, 'MPB', 1990, 2010)

insert into compositor values
--(cod_comp, nome, tipo_composicao, local_nasc, dt_nasc, dt_morte, periodo)
(1, 'Johann Sebastian Bach', 'Concerto', 'Eisenach, Alemanha', '1685-03-31', '1750-07-28', 1),
(3, 'Antonin Dvorak', 'Sinfonia', 'Nelahozeves, Tchéquia', '1841-09-08', '1904-05-01', 2),
(4, 'Ludwig van Beethoven', 'Sinfonia', 'Bonn, Alemanha', '1770-12-17', '1827-03-26', 3),
(5, 'Aluizio Almendra', 'MPB', 'Coreau - CE', '1980-01-25', null, 3),
(6, 'Djavan', 'MPB', 'Maceió - AL', '1949-01-27', NULL, 3)

insert into tipo_comp values
--(cod_tipo, descricao)
(1, 'Canção'),
(2, 'Concerto'),
(3, 'Sinfonia');


insert into interprete values
--(cod_int, nome, tipo)
(1, 'Chico Buarque', 'MPB'),
(2, 'Danny Secundino', 'MPB'),
(3, 'Tom Jobim', 'MPB'),
(4, 'J. S. Bach', 'Barroca'),
(5, 'G. F. Handel', 'Barroca'),
(6, 'L. v. Beethoven', 'Clássica'),
(7, 'W. A. Mozart', 'Clássica');

insert into faixa values
-- (cod_album, num_disco, num_faixa, descricao, tempo, tipo_gravacao, tipo_composicao)
(1, 1, 1, 'Oratório de Natal', 260, 'DDD', 1),
(1, 2, 1, 'Vento do Norte',   200, 'DDD', 2),
(1, 2, 2, 'Vento do Norte',   200, 'DDD', 2),

(1, 2, 3, 'Teste Barroco Concerto',   200, 'DDD', 2),

(2, 1, 3, 'Sinfonia de Dvorak', 360, null, 3),
(2, 1, 1, 'Sonata ao luar', 305, null, 2),
(2, 1, 2, '9° sinfonia',   930, null, 2),

(3, 1, 1, 'Mar de Janeiro',   225, 'ADD', 3),
(3, 1, 2, 'Garota de Ipanema',  230, 'DDD', 3),
(3, 2, 1, 'Estrelas',         195, 'DDD', 3),
(3, 2, 2, 'Caminhos',         245, 'ADD', 3)


insert into interpretes values
--(num_faixa, cod_album, num_disco, cod_inter)
(1, 2, 1, 6),
(2, 2, 1, 6),
(3, 2, 1, 2),

(1, 1, 2, 4),
(1, 1, 1, 7),
(3, 1, 2, 2),

(1, 3, 1, 3),
(2, 3, 1, 2),
(1, 3, 2, 1),
(2, 3, 2, 2);

insert into compositores values
-- (num_faixa, cod_album, num_disco, cod_comp)
(1, 2, 1, 6),
(2, 2, 1, 6),
(3, 2, 1, 3),

(3, 1, 2, 1),
(1, 1, 1, 1),
(1, 1, 2, 6),
(2, 1, 2, 1 ),

(1, 3, 1, 5),
(2, 3, 1, 5),
(1, 3, 2, 4),
(2, 3, 2, 6);


insert into playlist values
-- (cod_play, nome, dt_criacao, tempo)
(1, 'Favoritas', '2025-01-10'),
(2, 'Classicos Ouro', '2026-01-10'),
(3, 'MPB Relax', '2025-12-05'),
(4, 'Concertos Barrocos', '2025-12-05');



insert into playlists values
--(num_faixa, cod_album, num_disco, cod_play, vezes_tocada, ultima vez tocada)

-- Playlist 1 – Favoritas
(1, 2, 1, 1, 12, '2025-05-01'),
(2, 2, 1, 1, 8, '2025-05-01'),
(1, 3, 1, 1, 20, '2025-05-01'),

-- Playlist 2 – Classicos Ouro
(1, 1, 1, 2, 5, '2026-01-20'),
(1, 1, 2, 2, 4, '2026-01-20'),
(1, 2, 1, 2, 9, '2026-01-20'),
(3, 2, 1, 2, 1, '2026-01-20'),
-- Playlist 3 – MPB Relax
(1, 3, 1, 3, 15, '2025-12-30'),
(2, 3, 2, 3, 12, '2025-12-30'),
(2, 3, 1, 3, 10, '2025-12-30'),

-- Playlist 4 - Concertos Barrocos
(3, 1, 2, 4, 13, null);