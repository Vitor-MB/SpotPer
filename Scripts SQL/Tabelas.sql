USE SpotPer 
GO


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