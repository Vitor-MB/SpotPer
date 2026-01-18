USE SpotPer 
GO
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