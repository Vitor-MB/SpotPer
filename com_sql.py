import pyodbc

server = 'DESKTOP-VVHFIP4;'
database = 'SpotPer;'

conexao = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};' \
'SERVER='+server+';DATABASE='+database+';TrustServerCertificate=yes;'+'Trusted_Connection=yes')

cursor = conexao.cursor()
cursor.execute("SELECT * from faixa;")
row = cursor.fetchone()

while row:
    print(row[0])
    row = cursor.fetchone()