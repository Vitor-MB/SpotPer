USE SpotPer
GO

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
	