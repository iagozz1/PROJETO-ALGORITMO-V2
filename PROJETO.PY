import funções
import funcoes2
import funcoescliente
while True:
    if len(funções.usuarios) > 0:
        cadastro = True
    else:
        cadastro = False 
    if cadastro == False:
        print('='*60)
        print('MENU PARA CADASTROS'.center(60))
        print('='*60)
        print('[1] - Registrar ')
        print('-'*60)
        escolha = str(input('Digite a opção: '))
        if escolha != '1':
            print('Resposta Inválida')
            continue
        if escolha == '1':
            funções.Cadastro()
    
    if cadastro == True:
        print('='*60)
        print('MENU Principal'.center(60))
        print('='*60)
        print('[1] - Registrar\n[2] - Login ')
        print('-'*60)
        escolha = str(input('Digite a opção: '))
        if escolha != '1' and escolha != '2':
            print('Resposta Inválida')
            continue
        
        if escolha == '1':
            funções.Cadastro()
        
        
        elif escolha == '2':
            log,nome = funções.Login()
            usuario_logado = nome
            if log == True and funções.usuarios[nome]['Tipo'] == 'adm':
                while True:
                    print('='*60)
                    print('MENU PRINCIPAL  -  ADMINISTRADOR'.center(60))
                    print('='*60)
                    print('\n[1] - Adicionar Animais \n[2] - Buscar animais\n[3] - Buscar derivados \n[4] - Atualizar animal\n[5] - Remover animal\n[6] - Adicionar Derivados\n[7] - Menu de Estatísticas\n[8] - Vizualizar comentários\n[9] - Histórico de Movimentação\n[0] - Deslogar a conta')
                    print('-'*60)
                    
                    escolha = str(input('Digite a opção: '))
                    
                    
                    if escolha != '1' and escolha != '2' and escolha != '3' and escolha != '4' and escolha != '5' and escolha != '6' and escolha != '7' and escolha != '8' and escolha != '9' and escolha != '0':
                        print('Escolha Inválida')

                    if escolha == '0':
                        print("Deslogado")
                        break
                    
                    if escolha == '1':
                        funcoes2.AdicionarAnimais(usuario_logado)

                    if escolha == '2':
                        funcoes2.BuscarAnimais(usuario_logado)

                    if escolha == '3':
                        funcoes2.VerProdutos(usuario_logado)
                    
                    if escolha == '4':
                        funcoes2.AtualizarAnimais(usuario_logado)

                    if escolha == '5':
                        funcoes2.RemoverAnimal(usuario_logado)

                    if escolha == '6':
                        funcoes2.AdicionarDerivados(usuario_logado)

                    if escolha == '7':
                        funcoes2.GraficoDeVendas()

                    if escolha == '8':
                        funcoes2.PdfComentarios(usuario_logado)

                    if escolha == '9':
                        funcoes2.VerRegistro()

            
            elif log == True and funções.usuarios[nome]['Tipo'] == 'cliente':
                while True:
                    print('='*60)
                    print('MENU PRINCIPAL  -  CLIENTE'.center(60))
                    print('='*60)
                    print('\n[1] - Visualizar estoque \n[2] - Comprar Derivados\n[3] - Comprar animais\n[4] - Reclamações\n[0] - Deslogar a conta')
                    print('-'*60)
                    escolha = str(input('Digite a opção: '))
                    if escolha != '1' and escolha != '2' and escolha != '3' and escolha != '4' and escolha != '0':
                        print('Escolha Inválida')
                    
                    if escolha == '1':
                        funcoescliente.VizualizarEstoque(usuario_logado)

                    if escolha == '2':
                        funcoescliente.ComprasdeDerivados(usuario_logado)
                    
                    if escolha == '3':
                        funcoescliente.ComprasDeAnimais(usuario_logado)
                        
                    if escolha == '4':
                        funcoescliente.FazerComentarios(nome)

                    if escolha == '0':
                        print('deslogado')
                        break
        
    

    
        

        