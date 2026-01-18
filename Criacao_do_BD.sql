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