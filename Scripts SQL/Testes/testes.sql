-- Já existem faixas 1 e 2 no álbum 1 (discos 1 e 2),
-- então vamos popular o DISCO 1 com as faixas 3..65

INSERT INTO faixa VALUES
(1, 1, 3,  'Teste', 200, 'ADD', 1),
(1, 1, 4,  'Teste', 200, 'DDD', 1),
(1, 1, 5,  'Teste', 200, 'DDD', 1),
(1, 1, 6,  'Teste', 200, 'DDD', 1),
(1, 1, 7,  'Teste', 200, 'DDD', 1),
(1, 1, 8,  'Teste', 200, 'DDD', 1),
(1, 1, 9,  'Teste', 200, 'DDD', 1),
(1, 1,10,  'Teste', 200, 'DDD', 1),
(1, 1,11,  'Teste', 200, 'DDD', 1),
(1, 1,12,  'Teste', 200, 'DDD', 1),
(1, 1,13,  'Teste', 200, 'DDD', 1),
(1, 1,14,  'Teste', 200, 'DDD', 1),
(1, 1,15,  'Teste', 200, 'DDD', 1),
(1, 1,16,  'Teste', 200, 'DDD', 1),
(1, 1,17,  'Teste', 200, 'DDD', 1),
(1, 1,18,  'Teste', 200, 'DDD', 1),
(1, 1,19,  'Teste', 200, 'DDD', 1),
(1, 1,20,  'Teste', 200, 'DDD', 1),
(1, 1,21,  'Teste', 200, 'DDD', 1),
(1, 1,22,  'Teste', 200, 'DDD', 1),
(1, 1,23,  'Teste', 200, 'DDD', 1),
(1, 1,24,  'Teste', 200, 'DDD', 1),
(1, 1,25,  'Teste', 200, 'DDD', 1),
(1, 1,26,  'Teste', 200, 'DDD', 1),
(1, 1,27,  'Teste', 200, 'DDD', 1),
(1, 1,28,  'Teste', 200, 'DDD', 1),
(1, 1,29,  'Teste', 200, 'DDD', 1),
(1, 1,30,  'Teste', 200, 'DDD', 1),
(1, 1,31,  'Teste', 200, 'DDD', 1),
(1, 1,32,  'Teste', 200, 'DDD', 1),
(1, 1,33,  'Teste', 200, 'DDD', 1),
(1, 1,34,  'Teste', 200, 'DDD', 1),
(1, 1,35,  'Teste', 200, 'DDD', 1),
(1, 1,36,  'Teste', 200, 'DDD', 1),
(1, 1,37,  'Teste', 200, 'DDD', 1),
(1, 1,38,  'Teste', 200, 'DDD', 1),
(1, 1,39,  'Teste', 200, 'DDD', 1),
(1, 1,40,  'Teste', 200, 'DDD', 1),
(1, 1,41,  'Teste', 200, 'DDD', 1),
(1, 1,42,  'Teste', 200, 'DDD', 1),
(1, 1,43,  'Teste', 200, 'DDD', 1),
(1, 1,44,  'Teste', 200, 'DDD', 1),
(1, 1,45,  'Teste', 200, 'DDD', 1),
(1, 1,46,  'Teste', 200, 'DDD', 1),
(1, 1,47,  'Teste', 200, 'DDD', 1),
(1, 1,48,  'Teste', 200, 'DDD', 1),
(1, 1,49,  'Teste', 200, 'DDD', 1),
(1, 1,50,  'Teste', 200, 'DDD', 1),
(1, 1,51,  'Teste', 200, 'DDD', 1),
(1, 1,52,  'Teste', 200, 'DDD', 1),
(1, 1,53,  'Teste', 200, 'DDD', 1),
(1, 1,54,  'Teste', 200, 'DDD', 1),
(1, 1,55,  'Teste', 200, 'DDD', 1),
(1, 1,56,  'Teste', 200, 'DDD', 1),
(1, 1,57,  'Teste', 200, 'DDD', 1),
(1, 1,58,  'Teste', 200, 'DDD', 1),
(1, 1,59,  'Teste', 200, 'DDD', 1),
(1, 1,60,  'Teste', 200, 'DDD', 1),
(1, 1,61,  'Teste', 200, 'DDD', 1),
(1, 1,62,  'Teste', 200, 'DDD', 1),
(1, 1,63,  'Teste', 200, 'DDD', 1),
(1, 1,64,  'Teste', 200, 'DDD', 1),
(1, 1,65,  'Teste', 200, 'DDD', 1);

/*
delete from faixa 
where descricao = 'Teste'
*/

--Periodo barroco DDD

INSERT INTO faixa VALUES
(2, 1, 3,  'Teste', 200, 'ADD', 1)
Insert into compositores values
(3, 2, 1, 1)

--Album até 3x o valor da media dos albuns DDD
Insert into album values
(8, 'Album_teste',150000, '2025-12-05', '2025-08-13', 'CD', 1)

/*
delete from album
where decricao = 'Album_teste'
*/

--Funçao
select * from albuns_do_compositor('alu')