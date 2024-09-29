import sqlite3
import csv
import os
import shutil
import datetime

# Configurações de diretórios
BASE_DIR = 'meu_sistema_livraria'
BACKUP_DIR = os.path.join(BASE_DIR, 'backups')
DATA_DIR = os.path.join(BASE_DIR, 'data')
EXPORT_DIR = os.path.join(BASE_DIR, 'exports')

# Criar diretórios se não existirem
os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)

# Conectar ao banco de dados ou criar se não existir
db_path = os.path.join(DATA_DIR, 'livraria.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Criar tabela livros
cursor.execute('''
    CREATE TABLE IF NOT EXISTS livros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        ano_publicacao INTEGER NOT NULL,
        preco REAL NOT NULL
    )
''')
conn.commit()

def backup_db():
    backup_file = os.path.join(BACKUP_DIR, f'backup_livraria_{datetime.date.today()}.db')
    shutil.copy(db_path, backup_file)
    print(f'Backup criado: {backup_file}')

def limpar_backups_antigos():
    backups = sorted(os.listdir(BACKUP_DIR))
    backups = [b for b in backups if b.startswith('backup_livraria_') and b.endswith('.db')]
    for backup in backups[:-5]:  # Manter apenas os últimos 5 backups
        os.remove(os.path.join(BACKUP_DIR, backup))
        print(f'Backup removido: {backup}')

def adicionar_livro(titulo, autor, ano_publicacao, preco):
    backup_db()
    cursor.execute('''
        INSERT INTO livros (titulo, autor, ano_publicacao, preco)
        VALUES (?, ?, ?, ?)
    ''', (titulo, autor, ano_publicacao, preco))
    conn.commit()
    print(f'Livro "{titulo}" adicionado com sucesso!')

def exibir_livros():
    cursor.execute('SELECT * FROM livros')
    livros = cursor.fetchall()
    if livros:
        for livro in livros:
            print(f'ID: {livro[0]}, Título: {livro[1]}, Autor: {livro[2]}, Ano: {livro[3]}, Preço: {livro[4]:.2f}')
    else:
        print('Nenhum livro cadastrado.')

def atualizar_preco(titulo, novo_preco):
    backup_db()
    cursor.execute('''
        UPDATE livros
        SET preco = ?
        WHERE titulo = ?
    ''', (novo_preco, titulo))
    conn.commit()
    print(f'Preço do livro "{titulo}" atualizado com sucesso!')

def remover_livro(titulo):
    backup_db()
    cursor.execute('DELETE FROM livros WHERE titulo = ?', (titulo,))
    conn.commit()
    print(f'Livro "{titulo}" removido com sucesso!')

def buscar_por_autor(autor):
    cursor.execute('SELECT * FROM livros WHERE autor = ?', (autor,))
    livros = cursor.fetchall()
    if livros:
        for livro in livros:
            print(f'ID: {livro[0]}, Título: {livro[1]}, Autor: {livro[2]}, Ano: {livro[3]}, Preço: {livro[4]:.2f}')
    else:
        print(f'Nenhum livro encontrado para o autor "{autor}".')

def exportar_para_csv():
    cursor.execute('SELECT * FROM livros')
    livros = cursor.fetchall()
    with open(os.path.join(EXPORT_DIR, 'livros_exportados.csv'), mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Título', 'Autor', 'Ano de Publicação', 'Preço'])
        writer.writerows(livros)
    print('Dados exportados para livros_exportados.csv.')

def importar_de_csv():
    with open(os.path.join(EXPORT_DIR, 'livros_exportados.csv'), mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Ignorar cabeçalho
        for row in reader:
            adicionar_livro(row[1], row[2], int(row[3]), float(row[4]))

def menu():
    while True:
        print('''\nMenu:
        1. Adicionar novo livro
        2. Exibir todos os livros
        3. Atualizar preço de um livro
        4. Remover um livro
        5. Buscar livro por autor
        6. Exportar dados para CSV
        7. Importar dados de CSV
        8. Limpar backups antigos
        9. Sair
        ''')
        escolha = input('Escolha uma opção: ')

        if escolha == '1':
            titulo = input('Título: ')
            autor = input('Autor: ')
            ano_publicacao = int(input('Ano de Publicação: '))
            preco = float(input('Preço: '))
            adicionar_livro(titulo, autor, ano_publicacao, preco)

        elif escolha == '2':
            exibir_livros()

        elif escolha == '3':
            titulo = input('Título do livro para atualizar o preço: ')
            novo_preco = float(input('Novo preço: '))
            atualizar_preco(titulo, novo_preco)

        elif escolha == '4':
            titulo = input('Título do livro para remover: ')
            remover_livro(titulo)

        elif escolha == '5':
            autor = input('Nome do autor: ')
            buscar_por_autor(autor)

        elif escolha == '6':
            exportar_para_csv()

        elif escolha == '7':
            importar_de_csv()

        elif escolha == '8':
            limpar_backups_antigos()

        elif escolha == '9':
            print('Saindo...')
            break

        else:
            print('Opção inválida, tente novamente.')

# Iniciar o programa
menu()

# Fechar a conexão com o banco de dados
conn.close()