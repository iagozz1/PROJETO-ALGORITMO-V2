animais = {}
derivados = {}
registro = []
import datetime
import matplotlib.pyplot as plt
from funcoescliente import gastos
from funcoescliente import comentarios
from funções import usuarios

def AdicionarAnimais(usuario_logado):
        nome = input('Digite o nome do animal:').lower().strip()
        while True:
            id_existe = False
            ident = int(input('ID do animal:'))
            for ids in animais:
                if ids == ident:
                    print('Já existe um animal com o id registrado.')
                    id_existe = True
            if id_existe == True:
                continue
            else:
                estado = input('Estado do animal:').lower().strip()
                peso = int(input('Digite o peso em arroba do animal: '))

                animais[ident] = {'nome': nome, 'peso':peso, 'estado':estado}
                Registrar(f"Adicionou o animal {nome} (ID {ident})", usuarios[usuario_logado]['Nome'], tipo=usuarios[usuario_logado]['Tipo'])
                
                print('Animal adicionado!')
            break

def BuscarAnimais(usuario_logado):
    nome_busca = input('Qual animal deseja buscar?: ')
    existe = False
    for id_animal, dados in animais.items():
        if dados['nome'] == nome_busca:
            print(f"Nome: {dados['nome']} | Id: {id_animal} | Peso: {dados['peso']}@ | Estado: {dados['estado']}")
            existe = True
    if existe == False:
        print('Nenhum animal encontrado.')
    Registrar(f"Buscou pelo animal {nome_busca}", usuarios[usuario_logado]['Nome'], tipo=usuarios[usuario_logado]['Tipo'])

def VerProdutos(usuario_logado):
    print('='*60)
    print('DERIVADOS'.center(60))
    print('='*60)
    for nome, dados in derivados.items():
        print(f'Produto: {nome} | Quantidade: {dados['Quant']} | Preço: R$ {dados['Preço']}')
    Registrar("Visualizou lista de produtos derivados", usuarios[usuario_logado]['Nome'], tipo=usuarios[usuario_logado]['Tipo'])

def AtualizarAnimais(usuario_logado): 
    encontrado = False
    nome_busca = input('Qual animal deseja buscar?: ')
    for id_animal, dados in animais.items():
        if dados['nome'] == nome_busca:
            print(f"Nome: {dados['nome']} | Id: {id_animal} | Peso: {dados['peso']}@ | Estado: {dados['estado']}")
            encontrado = True
    if encontrado == True:
        atualizar = int(input('Digite o Id do animal que queira atualizar: '))
        nome_novo = input('Digite o nome do animal:')
        estado_novo = input('Estado do animal:')
        animais[atualizar] = {'nome': nome_novo,'estado':estado_novo}
        print('Animal Atualizado com Sucesso.')
        Registrar(f"Atualizou animal ID {atualizar} para {nome_novo}", usuarios[usuario_logado]['Nome'], tipo=usuarios[usuario_logado]['Tipo'])
    else:
        print('Nenhum Animal desse tipo foi encontrado.')
        
def AdicionarDerivados(usuario_logado):
        while True:
            existe = False
            nome = input('Digite o nome do produto:').lower().strip()
            for nomes in derivados:
                if nomes == nome:
                    existe = True
                    break
            if existe == True:
                print('Esse Produto já existe.')
                op = input('Você deseja atualizar o produto?(s/n)').lower().strip()
                if op == 's' or 'sim' or 'ss':
                    existe = False
                else:
                    continue
            if existe == False: 
                quant = int(input('Digite a quantidade do produto:'))
                valor = float(input('Digite o valor do produto:'))

                derivados[nome] = {'Quant': quant,'Preço':valor}
                gastos[nome] = {'Quant':quant, 'Preço':valor}
                Registrar(f"Adicionou produto {nome} (Qtd: {quant}, Preço: {valor})", usuarios[usuario_logado]['Nome'], tipo=usuarios[usuario_logado]['Tipo'])
                print('O Produto foi adicionado!') 

            continuar = input('Deseja continuar adicionando? (s/n):').lower().strip()
            if continuar == 's':
                continuar
            else:
                break

def RemoverAnimal(usuario_logado):
    nome_busca = input('Qual animal deseja buscar?: ')
    for id_animal, dados in animais.items():
        if dados['nome'] == nome_busca:
            print(f"Nome: {dados['nome']} | Id: {id_animal} | Peso: {dados['peso']}@ | Estado: {dados['estado']}")

    esc = int(input('Qual animal deseja remover?(ID):'))

    removido = animais.pop(esc)
    Registrar(f"Removeu animal {removido['nome']} (ID {esc})", usuarios[usuario_logado]['Nome'], tipo=usuarios[usuario_logado]['Tipo'])

    print('Animal removido com sucesso!')

def GraficoDeVendas():
    if not gastos:
        print("Nenhum dado de vendas encontrado.")
        return

    produtos = list(gastos.keys())
    quantidades = [dados['Quant'] for dados in gastos.values()]
    valores = [dados['Preço'] for dados in gastos.values()]

    if sum(valores) == 0 or sum(quantidades) == 0:
        print("Não há vendas registradas para gerar o gráfico.")
        return

    
    plt.figure(figsize=(8,5))
    plt.bar(produtos, valores, color="green")
    plt.title("Vendas por Produto/Animal")
    plt.xlabel("Produtos/Animais")
    plt.ylabel("Valor total vendido (R$)")
    plt.xticks(rotation=45)
    plt.show()
    plt.close()

    
    plt.figure(figsize=(6,6))
    plt.pie(quantidades, labels=produtos, autopct='%1.1f%%', startangle=90)
    plt.title("Participação nas Vendas (Quantidade)")
    plt.show()
    plt.savefig("grafico_vendas.png")
    plt.close()  

def PdfComentarios(usuario_logado):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    import datetime


    
    nome_arquivo = "Comentarios_Fazenda.pdf"
    pdf = SimpleDocTemplate(nome_arquivo, pagesize=A4)

    
    estilos = getSampleStyleSheet()
    titulo = Paragraph("📊 Relatório de Comentários da Fazenda", estilos['Title'])
    subtitulo = Paragraph("Usuários, Comentários e Datas", estilos['Heading2'])
    espacamento = Spacer(1, 20)

    
    dados = [["Usuário", "Comentário", "Data"]]

    
    for usuario, info in comentarios.items():
        data_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        dados.append([usuario, info['Comentário'], data_atual])

    
    tabela = Table(dados, colWidths=[150, 250, 120])

    
    estilo_tabela = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#FF5733")), 
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 14),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#FDEDEC")), 
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ])
    tabela.setStyle(estilo_tabela)

    
    elementos = [titulo, subtitulo, espacamento, tabela]
    pdf.build(elementos)
    Registrar("Gerou PDF de comentários", usuarios[usuario_logado]['Nome'], tipo=usuarios[usuario_logado]['Tipo'])
    print(f"PDF '{nome_arquivo}' gerado com sucesso!")

def VerRegistro():
    print("="*80)
    print("📜 REGISTRO GERAL DA FAZENDA".center(80))
    print("="*80)
    for log in registro:
        print(f"[{log['data']}] ({log['tipo']}){log['usuario']} -> {log['acao']}")

def Registrar(acao, usuario="Sistema", tipo='Adm'):
    data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    registro.append({'tipo':tipo, "usuario": usuario, "acao": acao, "data": data_hora})

