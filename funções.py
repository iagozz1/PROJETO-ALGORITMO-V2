usuarios = {}
def Cadastro():
    cadastro = False
    caracteres_especiais = ['!', '@', '#', '$', '%', '&', '*', ',', '.']
    if len(usuarios) > 0:
        cadastro = True
    else:
        cadastro = False
    while True:
        existe = False
        nome = input('Digite seu nome de Usuário: ')
        for nomes in usuarios:
            if nomes == nome:
                existe = True
                break
        if existe == True:
            print('O nome de usuário já existe.')
        else:
            while True:
                especial = False
                senha = input('Digite sua Senha: ')
                if len(senha) < 8:
                    print('A senha deve conter pelo menos 8 caracteres.')
                    continue
                for espec in caracteres_especiais:
                    if espec in senha:
                        especial = True
                        break
                if especial == False:
                    print('A senha deve conter pelo menos um caractere especial(Exemplo ! @ # . ,).')
                    continue
                else:
                    while True:
                        tipo = input('Digite o tipo de usuario(adm / cliente): ').strip().lower()
                        if tipo != 'adm' and tipo != 'cliente':
                            print('Esse tipo é inválido')
                            continue
                        else:
                            usuarios[nome] = {'Nome':nome, 'Senha':senha, 'Tipo':tipo}
                            print('-'*10, 'Cadastro Concluido', '-'*10)
                            cadastro = True
                            break
                break
        if cadastro == True:
            break

def Login():
    log = False
    while log == False:
        nome = input('Digite seu nome:')
        usuario_encontrado = False
        
        if nome in usuarios:
            usuario_encontrado = True
                
        elif usuario_encontrado == False:
            print('Usuário não encontrado')
            continue

        if usuario_encontrado == True:
            while True:
                senha = input('Digite sua senha:')
                senha_encontrada = False
                
                if senha == (usuarios[nome]['Senha']):
                    senha_encontrada = True
                
                elif senha_encontrada == False:
                    print('Senha Incorreta.')
                    continue

                if senha_encontrada == True:
                    if (usuarios[nome]['Tipo']) == 'adm':
                        print('Logado como administrador. Bem vindo!')

                    elif (usuarios[nome]['Tipo']) == 'cliente':
                        print('Logado como cliente. Bem vindo!')
                        
                    log = True
                    return log,nome






                