# Sistema de Gerenciamento de Livros

Este é um sistema simples de gerenciamento de livros em uma livraria, utilizando SQLite para o armazenamento de dados. O sistema permite a criação, visualização, atualização e remoção de livros, além de funcionalidades de backup e exportação/importação de dados em formato CSV.

## Funcionalidades

- **Adicionar novo livro:** Insere um novo livro no banco de dados com título, autor, ano de publicação e preço.
- **Exibir todos os livros:** Lista todos os livros presentes no banco de dados.
- **Atualizar preço de um livro:** Permite atualizar o preço de um livro já cadastrado.
- **Remover um livro:** Remove um livro específico do banco de dados.
- **Buscar por autor:** Busca e lista todos os livros de um autor específico.
- **Exportar para CSV:** Exporta os livros cadastrados para um arquivo CSV.
- **Importar de CSV:** Importa livros de um arquivo CSV.
- **Backup e limpeza de backups antigos:** Cria backups do banco de dados e mantém apenas os cinco backups mais recentes.

## Estrutura de Diretórios

O programa organiza os dados em três diretórios principais:
- `meu_sistema_livraria/backups`: Armazena os backups do banco de dados.
- `meu_sistema_livraria/data`: Contém o arquivo de banco de dados SQLite.
- `meu_sistema_livraria/exports`: Diretório para exportação e importação de arquivos CSV.
