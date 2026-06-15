comentarios = {}
gastos = {}
import requests
import datetime
from funcoes2 import derivados
from funcoes2 import animais
from funcoes2 import registro
from funções import usuarios

def FazerComentarios(nome):
    comentario = input("Digite seu Comentário: ")
    comentarios[nome] = {'Comentário': comentario}
    
    print("Comentário registrado com sucesso!")

def VizualizarEstoque(usuario_logado):
    print('='*60)
    print('DERIVADOS'.center(60))
    print('='*60)
    for nome, dados in derivados.items():
        print(f'Produto: {nome} | Quantidade: {dados['Quant']} | Preço: R$ {dados['Preço']}')
    
    nome_busca = input('Qual animal deseja buscar?(digite n para cancelar a busca por animais): ').lower()
    existe = False
    if nome_busca == 'n' or nome_busca == 'não' or nome_busca == 'nao':
        print('Busca Cancelada')
    else:
        for id_animal, dados in animais.items():
                if dados['nome'] == nome_busca:
                    print(f"Nome: {dados['nome']} | Id: {id_animal} | Estado: {dados['estado']}")
                    existe = True
        if existe == False:
            print('Nenhum animal encontrado.')
    Registrar(f"Buscou a lista dos produtos derivados e Buscou pelo animal {nome_busca}", usuarios[usuario_logado]['Nome'], tipo=usuarios[usuario_logado]['Tipo'])

def ComprasdeDerivados(usuario_logado):
    carrinho = []
    while True:
        buscar = input('Qual produto deseja comprar? (ou "finalizar" para encerrar): ')
        if buscar.lower() == "finalizar":
            break

        if buscar not in derivados:
            print('Nenhum produto encontrado.')
            continue
        
        dados = derivados[buscar]
        print(f"Produto: {buscar} | Quantidade: {dados['Quant']} | Preço: R$ {dados['Preço']}")
        while True:
            quanti = int(input('Digite a quantidade que deseja comprar?: '))
            if quanti <= 0 or quanti > dados['Quant']:
                print('Quantidade inválida ou estoque insuficiente.')
                continue

        
            dados['Quant'] -= quanti
            carrinho.append({'Produto': buscar, 'Quant': quanti, 'Preço': dados['Preço']})
            print(f"{quanti} unidade(s) de {buscar} adicionadas ao carrinho!")


            if len(carrinho) <= 0:
                print("Carrinho vazio. Nenhuma compra realizada.")
                continue

            data_entrega = input("Digite a data da entrega (DD-MM-AAAA): ").strip()
            hora_entrega = input("Digite a hora da entrega (HH:MM): ").strip()
            print(f"Entrega agendada para {data_entrega} às {hora_entrega}h.")

            agendamento = {"Cliente": usuarios[usuario_logado]['Nome'], "Produto": buscar,"Data": data_entrega,"Hora": hora_entrega}
            print(f"Agendamento registrado: Cliente: {agendamento['Cliente']} | Produto: {agendamento['Produto']} | Data: {agendamento['Data']} | Hora: {agendamento['Hora']}")
            
            while True:
                cep = input('Digite o CEP para entrega: ')
                cep = cep.replace('-', '').replace('.', '').strip()

                if len(cep) != 8 or not cep.isdigit():
                    print("CEP inválido. Digite apenas números com 8 dígitos.")
                    continue

                response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
                endereco = response.json()

                if "erro" in endereco:
                    print("CEP não encontrado. Tente novamente.")
                    continue

                cidade = endereco.get('localidade', 'Cidade não encontrada')
                estado = endereco.get('uf', 'UF não encontrada')
                bairro = endereco.get('bairro', 'Bairro não encontrado')

                print(f"\nLocal de entrega: {cidade}/{estado}, Bairro: {bairro}")
                break

            total = 0
            print("\nResumo do carrinho:")
            for item in carrinho:
                subtotal = item['Quant'] * item['Preço']
                total += subtotal
                print(f"{item['Produto']} - {item['Quant']} x R${item['Preço']:.2f} = R${subtotal:.2f}")

            
            if estado in ["PB", "RN"]:
                transporte = "Transporte rápido (Nordeste)"
            elif estado in ["AM", "PA"]:
                transporte = "Transporte fluvial"
            else:
                transporte = "Transporte padrão"
            print(f"\nTransporte escolhido: {transporte}")

            
            if total >= 200:
                frete = 0.0
            elif estado in ["PB", "RN", "PE", "CE", "BA", "AL", "SE", "MA", "PI"]:
                frete = 20.0
            elif estado in ["SP", "RJ", "MG", "ES"]:
                frete = 30.0
            elif estado in ["AM", "PA", "RR", "RO", "AC", "AP", "TO"]:
                frete = 40.0
            else:
                frete = 25.0

            print(f"\nValor total dos produtos: R${total:.2f}")
            print(f"Frete: R${frete:.2f}")
            print(f"Valor final com frete: R${total + frete:.2f}")
            Registrar(f"Realizou a seguinte compra {carrinho}", usuarios[usuario_logado]['Nome'], tipo=usuarios[usuario_logado]['Tipo'])
            break
        break

def ComprasDeAnimais(usuario_logado):
    carrinho_animais = []
    while True:
        nome_busca = input('Qual animal deseja buscar? (ou "finalizar" para cancelar): ').lower().strip()
        if nome_busca.lower() == "finalizar":
            break

        existe = False
        for id_animal, dados in animais.items():
            if dados['nome'] == nome_busca:
                print(f"Nome: {dados['nome']} | Id: {id_animal} | Peso: {dados['peso']}@ | Estado: {dados['estado']}")
                existe = True
        if not existe:
            print('Nenhum animal encontrado.')
            continue
        while True:    
            comprar = int(input('Digite o Id do animal que você deseja comprar: '))
            if comprar not in animais:
                print("Id inválido.")
                continue

            animal = animais[comprar]
            if animal['estado'] != "disponível" and animal['estado'] != 'disponivel':
                print(f"O animal {animal['nome']} já não está disponível.")
                continue

            
            preco_arroba = 353.40  
            peso = animal['peso']
            valor = preco_arroba * peso

            
            carrinho_animais.append({'Animal': animal['nome'], 'Id': comprar, 'Peso': peso, 'Preço': valor})
            print(f"Animal {animal['nome']} adicionado ao carrinho por R${valor:.2f}!")
            
            del animais[comprar]
            
            if len(carrinho_animais) <= 0:
                print("Carrinho vazio. Nenhuma compra realizada.")
                continue
            
            if len(animais) > 0:
                confirmar = input('Deseja comprar outro animal? (s / sim | n / não)').lower().strip()
                if confirmar == 's' or confirmar == 'sim':
                    continue
            
            data_entrega = input("Digite a data da entrega (DD-MM-AAAA): ").strip()
            hora_entrega = input("Digite a hora da entrega (HH:MM): ").strip()
            print(f"Entrega agendada para {data_entrega} às {hora_entrega}h.")

            agendamento = {"Cliente": usuarios[usuario_logado]['Nome'], "Animal": animal['nome'],"Data": data_entrega,"Hora": hora_entrega}
            
            print(f"Agendamento registrado: Cliente: {agendamento['Cliente']} | Animal: {agendamento['Animal']} | Data: {agendamento['Data']} | Hora: {agendamento['Hora']}")

            while True:
                cep = input('Digite o CEP para entrega: ')
                cep = cep.replace('-', '').replace('.', '').strip()

                if len(cep) != 8 or not cep.isdigit():
                    print("CEP inválido. Digite apenas números com 8 dígitos.")
                    continue

                response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
                endereco = response.json()

                if "erro" in endereco:
                    print("CEP não encontrado. Tente novamente.")
                    continue

                cidade = endereco.get('localidade', 'Cidade não encontrada')
                estado = endereco.get('uf', 'UF não encontrada')
                bairro = endereco.get('bairro', 'Bairro não encontrado')

                print(f"Local de entrega: {cidade}/{estado}, Bairro: {bairro}")
                break

            total = 0
            print("\nResumo do carrinho de animais:")
            for item in carrinho_animais:
                subtotal = item['Preço']
                total += subtotal
                print(f"{item['Animal']} ({item['Peso']}@) - R${subtotal:.2f}")

                
                if item['Animal'] not in gastos:
                    gastos[item['Animal']] = {'Quant': 1, 'Preço': item['Preço']}
                else:
                    gastos[item['Animal']]['Quant'] += 1
                    gastos[item['Animal']]['Preço'] += item['Preço']

            
            if estado in ["PB", "RN"]:
                transporte = "Transporte rápido (Nordeste)"
            elif estado in ["AM", "PA"]:
                transporte = "Transporte fluvial"
            else:
                transporte = "Transporte padrão"
            print(f"\nTransporte escolhido: {transporte}")

            
            if total >= 20000:
                frete = 0.0
            elif estado in ["PB", "RN", "PE", "CE", "BA", "AL", "SE", "MA", "PI"]:
                frete = 500.0
            elif estado in ["SP", "RJ", "MG", "ES"]:
                frete = 800.0
            elif estado in ["AM", "PA", "RR", "RO", "AC", "AP", "TO"]:
                frete = 1000.0
            else:
                frete = 600.0

            print(f"\nValor total dos animais: R${total:.2f}")
            print(f"Frete: R${frete:.2f}")
            print(f"Valor final com frete: R${total + frete:.2f}")
            Registrar(f"Realizou a seguinte compra {carrinho_animais}", usuarios[usuario_logado]['Nome'], tipo=usuarios[usuario_logado]['Tipo'])
            break
        break

def Registrar(acao, usuario="Sistema", tipo='Adm'):
    data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    registro.append({'tipo':tipo, "usuario": usuario, "acao": acao, "data": data_hora})