insert into gravadora values
(1, 'BS audio', 'Rua A', 'Bairro 1', 'Caucaia','CE', null),
(2, 'Audio Maker','Rua B', 'Bairro 2', 'Fortaleza','CE', 'www.AuMaker.com'),
(4, 'Best gravacoes','Rua C', 'Bairro 3', 'Sao Paulo','RJ', 'www.Bestgra.com.br')

insert into telefones_gravadora values
(123456, 1),
(2345, 1),
(1223, 2)

insert into album values
(1, 'Barroco Vol.1', 59.90, '2000-05-12', '2006-01-10', 'CD', 1),
(2, 'Classicas', 74.50, '2010-03-22', '2011-07-18', 'VINIL', 2),
(3, 'MPB Colecao', 95.90, '2008-08-14', '2009-09-25', 'CD', 4)

insert into periodo values
(1, 'Barroco',1600, 1750),
(2, 'Classico',1750, 1820),
(3, 'MPB', 1990, 2010)

insert into compositor values
(1, 'Johann Sebastian Bach', 'Concerto', 'Eisenach, Alemanha', '1685-03-31', '1750-07-28', 2),
(4, 'Ludwig van Beethoven', 'Sinfonia', 'Bonn, Alemanha', '1770-12-17', '1827-03-26', 3),
(5, 'Aluizio Almendra', 'MPB', 'Coreau - CE', '1980-01-25', null, 1),
(6, 'Djavan', 'MPB', 'Maceió - AL', '1949-01-27', NULL, 1)

insert into tipo_comp values
(1, 'MPB'),
(2, 'Barroca'),
(3, 'Clássica');

insert into interprete values
(1, 'Chico Buarque', 'MPB'),
(2, 'Djavan', 'MPB'),
(3, 'Caetano Veloso', 'MPB'),
(4, 'J. S. Bach', 'Barroca'),
(5, 'G. F. Handel', 'Barroca'),
(6, 'L. v. Beethoven', 'Clássica'),
(7, 'W. A. Mozart', 'Clássica');

insert into faixa values
(1, 1, 'Samba da Aurora', 210, 'DDD', 1),
(1, 2, 'Noite de Verão',   185, 'DDD', 1),
(1, 3, 'Mar de Janeiro',   225, 'ADD', 2),

(2, 1, 'Lembranças',       260, 'DDD', 1),
(2, 2, 'Vento do Norte',   200, 'ADD', 2),

(3, 1, 'Balada do Tempo',  230, 'DDD', 3),
(3, 2, 'Estrelas',         195, 'DDD', 3),
(3, 3, 'Caminhos',         245, 'ADD', 1);