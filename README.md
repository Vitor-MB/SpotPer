# SpotPer 

Projeto desenvolvido na disciplina **Fundamentos de Banco de Dados (FBD)**  
📅 Semestre: **2025.2**  
🏫 **Universidade Federal do Ceará (UFC)** — Departamento de Computação (DC)

---

## Equipe:
- **Américo Vitor Moreira Barbosa**
- **Caio Emanuel de Oliveira Lima**

**Professor:** Ângelo Roncalli Alencar Brayner

---

## Sobre o Projeto
O **SpotPer** é um projeto acadêmico desenvolvido para a disciplina de **Fundamentos de Banco de Dados**.  Ele simula uma plataforma simples de streaming musical, com suporte a **álbuns, faixas e playlists**.

O foco principal do projeto é a **modelagem, criação e manipulação de banco de dados relacional**.

---

## Ferramentas Utilizadas
**Backend:** Python  
**Banco de Dados:** SQL Server 

---

##  Como Executar
1. Crie e inicialize o banco usando o script:
   ```
   scriptDeCriacaoDoBD.sql
   ```
2. Verifique se o banco está ativo e acessível.
3. Execute o aplicativo:
   ```
   python main.py
   ```

---

## 📂 Estrutura do Projeto (sugestão)
```
SpotPer/
 ├─ main.py
 ├─ com_sql.py (Possui as funções de comunicação, consultas e modificação das tabelas)
 ├─ scriptDeCriacaoDoBD.sql
 ├─ Povoamento.sql (Povoamento de Exemplo para testes)
 ├─ Scripts SQL/ (Scripts SQL separadamente)
 ├─ Testes/ (Arquivo com testes para gatilhos e funcoes)
 └─ README.md
```