--SCRIPT DE CRIACAO DO BANCO DE DADOS

CREATE DATABASE SpotPer

ON PRIMARY(
	NAME = SpotPer_Primary,
	FILENAME = 'C:\SpotPer\SpotPer_Primary.mdf',
	SIZE = 30 MB,
	FILEGROWTH = 10 MB
),

FILEGROUP FG_DADOS(
	NAME = SpotPer_Dados1,
	FILENAME = 'C:\SpotPer\SpotPer_Dados1.ndf',
	SIZE = 20MB,
	FILEGROWTH = 10MB
),
(
	NAME = SpotPer_Dados2,
	FILENAME = 'C:\SpotPer\SpotPer_Dados2.ndf',
	SIZE = 20MB,
	FILEGROWTH = 10MB
),

FILEGROUP FG_PLAYLIST(
	NAME = SpotPer_Playlists,
	FILENAME = 'C:\SpotPer\SpotPer_Playlists.ndf',
	SIZE = 30MB,
	FILEGROWTH = 10MB
)

LOG ON (
	NAME = SpotPer_Log,
	FILENAME = 'C:\SpotPer\SpotPer_Log.ldf',
	SIZE = 15MB,
	FILEGROWTH = 15MB
)

GO

USE SpotPer

GO

--CRIACAO DAS TABELAS

Create table periodo(
	cod_per tinyint not null,
	descricao varchar(20) not null,
	ano_inicio smallint not null,
	ano_fim smallint not null,

	constraint Pk_cod_per primary key(cod_per),

	constraint Check_anos CHECK(ano_inicio<ano_fim)
)on FG_DADOS

CREATE TABLE tipo_comp(
	cod_tipo tinyint not null,
	descricao varchar(20)not null,

	constraint  Fk_tipo_comp primary key(cod_tipo)
)on FG_DADOS

Create table gravadora(
	cod_gra smallint not null,
	nome varchar(40) not null,
	rua_end varchar(30) not null,
	bairro_end varchar(30) not null,
	cidade_end varchar(30) not null,
	estado_end varchar(2) not null,
	url_site varchar(70),

	constraint Pk_cod_gra PRIMARY KEY(cod_gra)

)on FG_DADOS

Create table telefones_gravadora(
	telefone varchar(15) not null,
	cod_gra smallint not null,

	constraint Pk_tel_gravadora primary key(cod_gra, telefone),

	constraint Fk_telefone foreign key(cod_gra) references gravadora(cod_gra)
)on FG_DADOS

Create table interprete(
	cod_int smallint not null,
	nome varchar(30) not null,
	tipo varchar(30) not null,

	constraint Pk_cod_inter PRIMARY KEY(cod_int)

)on FG_DADOS

Create table compositor(
	cod_comp smallint not null,
	nome varchar(50) not null,
	tipo_composicao varchar(20),
	local_nasc varchar(40),
	dt_nasc DATE not null,
	dt_morte DATE,
	periodo tinyint not null,

	constraint Pk_cod_comp PRIMARY KEY(cod_comp),
	constraint Fk_comp foreign key(periodo) references periodo(cod_per),

	constraint Check_datas CHECK(dt_morte is null or dt_nasc<dt_morte)

)on FG_DADOS

Create table album(
	cod_album SMALLINT not null,
	decricao VARCHAR(50) not null,
	preco DEC(10,2),
	dt_gravacao DATE not null,
	dt_compra DATE not null,
	meio_fisico varchar(10) not null,
	gravadora smallint not null,

	constraint Pk_album PRIMARY KEY(cod_album),
	constraint Fk_gravadora foreign key(gravadora) references gravadora(cod_gra),

	constraint Check_data CHECK(dt_gravacao >= '2000-01-01'),
	constraint Check_meio_fisico CHECK(meio_fisico in ('CD','VINIL', 'DOWNLOAD'))
)on FG_DADOS


CREATE TABLE faixa(
	cod_album SMALLINT not null,
	num_disco TINYINT not null,
	num_faixa SMALLINT not null,
	descricao VARCHAR(50) not null,
	tempo SMALLINT not null,
	tipo_gravacao VARCHAR(3),
	tipo_composicao TINYINT not null,

	CONSTRAINT Pk_faixa PRIMARY KEY(cod_album, num_disco, num_faixa),

	CONSTRAINT Fk_faixa_tipo_comp foreign key(tipo_composicao) references tipo_comp(cod_tipo),
	
	CONSTRAINT Check_tipo_grav CHECK( tipo_gravacao in ('ADD', 'DDD')),

	CONSTRAINT FK_faixa_album FOREIGN KEY (cod_album) references album(cod_album) ON DELETE CASCADE


)on FG_DADOS

Create table playlist(

	cod_play smallint not null,
	nome varchar(20) not null,
	dt_criacao date not null,
	tempo smallint,

	constraint Pk_playlist primary key(cod_play),

	constraint Check_tempo CHECK(tempo>0)

)on FG_PLAYLIST

--Tabelas N:N

Create table playlists(
	num_faixa smallint NOT NULL,
    cod_album SMALLINT NOT NULL,
	num_disco tinyint not null,
    cod_play SMALLINT NOT NULL,
    vezes_tocada SMALLINT,
    ultima_vez_tocada DATE,

	constraint Pk_play_mus primary key(cod_album, num_faixa, num_disco, cod_play),

	constraint Fk_faixa_play_faixa foreign key (cod_album, num_disco, num_faixa) REFERENCES faixa(cod_album, num_disco, num_faixa) ON DELETE CASCADE,

	constraint Fk_faixa_play_play foreign key (cod_play) references playlist(cod_play) ON DELETE CASCADE
)on FG_PLAYLIST

CREATE TABLE compositores(

	num_faixa smallint not null,
	cod_album smallint not null,
	num_disco tinyint not null,
	cod_comp smallint not null,

	constraint Pk_compositores primary key(cod_album, num_faixa, num_disco, cod_comp),

	constraint Fk_compositores_faixa foreign key(cod_album, num_disco, num_faixa ) references faixa(cod_album, num_disco, num_faixa ) ON DELETE  CASCADE,

	constraint Fk_compositores_compositor foreign key(cod_comp) references compositor(cod_comp)
)on FG_DADOS

CREATE TABLE interpretes(
	
	num_faixa smallint not null,
	cod_album smallint not null,
	num_disco tinyint not null,
	cod_inter smallint not null,

	constraint Pk_interpretes PRIMARY KEY(cod_album, num_faixa, num_disco, cod_inter),

	constraint Fk_interpretes_faixa foreign key(cod_album, num_disco, num_faixa) references faixa(cod_album, num_disco, num_faixa) ON DELETE CASCADE,

	constraint Fk_interpretes_interprete foreign key(cod_inter) references interprete(cod_int)
)on FG_DADOS

GO

--CRIACAO DOS TRIGGERS

--´CD TEM QUE SER ADD OU DDD E OS OUUTROS NUULOS
CREATE TRIGGER tipo_gravacao
on faixa
for INSERT, UPDATE
as
Begin
	if exists(
		select *
		from album a join inserted f on a.cod_album = f.cod_album
		where (meio_fisico = 'CD' and tipo_gravacao is null) or (meio_fisico in ('VINIL', 'DOWNLOAD') and tipo_gravacao is not null))
		Begin
			raiserror('Tipo de gravação incompátivel com o meio fisico', 16, 1);
			rollback transaction;
	END
END;
GO


--MAXIMO DE MUSICAS É 64 POR ALBUM
CREATE TRIGGER maximo_musicas
on faixa
for insert
as
begin
	 IF EXISTS (
        SELECT *
        FROM ( 
			SELECT count(*) as QTD
            FROM Faixa
            WHERE cod_album IN (SELECT DISTINCT cod_album FROM inserted)
            GROUP BY cod_album
			) t
		WHERE t.QTD > 64
      
    )
		begin
			raiserror( 'A quantidade maxima de faixas para esse album atingida(64 faixas)', 16, 1);
			rollback transaction;
		end
end;
GO


--Barroco so DDD
CREATE TRIGGER Barroco_DDD
on compositores
for update, insert
as
BEGIN
	IF exists(
		select *
		from inserted i join faixa f on i.num_faixa = f.num_faixa and i.cod_album = f.cod_album and f.num_disco = i.num_disco join compositor c on i.cod_comp = c.cod_comp join periodo p on p.cod_per = c.periodo
		where p.descricao like '_arroco' and f.tipo_gravacao <> 'DDD'
		)
		BEGIN
			raiserror('Faixas do periodo Barroco devem ter o tipo de gravacao DDD', 16, 1);
			rollback transaction;
	END
END;
GO


CREATE TRIGGER limite_preco
ON album
for insert, update
as
BEGIN
	if exists(
		select *
		from inserted i
		where i.preco >  3 * 
			( 
			--Nenhuma faixa tem a gravacao DDD
				select avg(a.preco)
				from album a
				where not exists(
					select *
					from faixa f
					where f.cod_album = a.cod_album and f.tipo_gravacao <> 'DDD'
					)
			)
			and
			(
				select count(*)
				from album a
				where not exists (
					select *
					from faixa f
					where f.cod_album = a.cod_album and f.tipo_gravacao > 'DDD'
					)
			) > 0
			
			)

			begin
			raiserror('O preco inserido deve ser até 3 vezes menor que a media de toddos os albuns DDD', 16, 1);
			rollback transaction;
			end
	end;


GO

--CRIACAO DA FUNCAO

create function Albuns_do_Compositor (@nome_compositor_ent varchar(50))
returns  @tab_resultado table (descricao_album varchar(30), cod_album smallint)
as
begin
declare @nome_compositor varchar(50)
set @nome_compositor = '%'+@nome_compositor_ent+'%'
insert into @tab_resultado
select a.decricao, a.cod_album
from album a join faixa f on a.cod_album = f.cod_album join compositores co on f.cod_album = co.cod_album and f.num_faixa = co.num_faixa and co.num_disco = f.num_disco join compositor c on co.cod_comp = c.cod_comp
where c.nome like @nome_compositor
return
end