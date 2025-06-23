import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# --- Configurações do E-mail (agora lidas do .env) ---
REMETENTE_EMAIL = os.getenv("REMETENTE_EMAIL")
REMETENTE_SENHA = os.getenv("REMETENTE_SENHA")
DESTINATARIO_EMAIL = os.getenv("DESTINATARIO_EMAIL")

ASSUNTO_EMAIL = "Registro Diário de Caixa"
CORPO_EMAIL = "Segue o registro de caixa de hoje."

# --- Diretório para salvar os arquivos de movimentação ---
DIRETORIO_MOVIMENTACOES = "movimentacoes"

# Garante que o diretório exista
if not os.path.exists(DIRETORIO_MOVIMENTACOES):
    os.makedirs(DIRETORIO_MOVIMENTACOES)

# --- Funções de Manipulação do Arquivo de Registro ---

def obter_nome_arquivo_do_dia():
    """Retorna o nome do arquivo de registro para o dia atual."""
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(DIRETORIO_MOVIMENTACOES, f"movimentacoes-{data_hoje}.txt")

def registrar_movimento(valor, tipo, descricao):
    """Registra uma nova movimentação no arquivo do dia."""
    nome_arquivo = obter_nome_arquivo_do_dia()
    with open(nome_arquivo, 'a', encoding='utf-8') as f:
        f.write(f"[{datetime.now().strftime('%H:%M:%S')}] Valor: R${valor:.2f}, Tipo: {tipo}, Descrição: {descricao}\n")
    print("Movimento registrado com sucesso!")

def listar_movimentacoes():
    """Lista todas as movimentações do arquivo do dia."""
    nome_arquivo = obter_nome_arquivo_do_dia()
    if not os.path.exists(nome_arquivo):
        print("Nenhuma movimentação registrada para hoje ainda.")
        return

    print("\n--- Movimentações do Dia ---")
    with open(nome_arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()
        if not conteudo.strip():
            print("Nenhuma movimentação registrada para hoje ainda.")
        else:
            print(conteudo)
    print("---------------------------\n")

# --- Função de Envio de E-mail ---

def enviar_email_com_anexo(remetente_email, remetente_senha, destinatario_email, assunto, corpo_email, caminho_arquivo):
    """Envia um e-mail com o arquivo de registro do dia como anexo."""
    if not remetente_email or not remetente_senha or not destinatario_email:
        print("Erro: As credenciais de e-mail (REM_EMAIL, REM_SENHA, DEST_EMAIL) não foram configuradas no .env.")
        print("Verifique seu arquivo .env e certifique-se de que as variáveis estão preenchidas.")
        return
    
    if not os.path.exists(caminho_arquivo):
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado para envio.")
        return

    try:
        msg = MIMEMultipart()
        msg['From'] = remetente_email
        msg['To'] = destinatario_email
        msg['Subject'] = assunto

        msg.attach(MIMEText(corpo_email, 'plain'))

        with open(caminho_arquivo, "rb") as f:
            attach = MIMEApplication(f.read(), _subtype="txt")
            attach.add_header('Content-Disposition', 'attachment', filename=os.path.basename(caminho_arquivo))
            msg.attach(attach)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remetente_email, remetente_senha)
        text = msg.as_string()
        server.sendmail(remetente_email, destinatario_email, text)
        server.quit()
        print(f"E-mail enviado com sucesso para {destinatario_email}!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        print("Verifique as configurações de e-mail, especialmente a 'senha de aplicativo' para o Gmail.")

# --- Lógica Principal do Console ---

def menu_principal():
    """Exibe o menu e gerencia as opções do usuário."""
    while True:
        print("\n--- Sistema de Registro de Caixa ---")
        print("1. Registrar nova movimentação")
        print("2. Listar movimentações do dia")
        print("3. Enviar registro do dia por e-mail")
        print("4. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            try:
                valor = float(input("Digite o valor (ex: 150.75): R$"))
                
                # Loop para garantir entrada válida para o tipo
                while True:
                    tipo_input = input("Digite o tipo (E para Entrada / S para Saída): ").strip().lower()
                    if tipo_input == 'e':
                        tipo = "Entrada"
                        break
                    elif tipo_input == 's':
                        tipo = "Saída"
                        break
                    else:
                        print("Opção inválida. Por favor, digite 'E' para Entrada ou 'S' para Saída.")

                descricao = input("Digite uma pequena descrição: ").strip()
                if not descricao:
                    print("Descrição não pode ser vazia. Operação cancelada.")
                    continue # Volta para o menu principal se a descrição for vazia

                registrar_movimento(valor, tipo, descricao)
            except ValueError:
                print("Valor inválido. Por favor, digite um número.")
                # Se o valor for inválido, ele volta para o menu principal
        elif opcao == '2':
            listar_movimentacoes()
        elif opcao == '3':
            caminho_arquivo_do_dia = obter_nome_arquivo_do_dia()
            enviar_email_com_anexo(
                REMETENTE_EMAIL, REMETENTE_SENHA, DESTINATARIO_EMAIL,
                ASSUNTO_EMAIL, CORPO_EMAIL, caminho_arquivo_do_dia
            )
        elif opcao == '4':
            print("Saindo do sistema. Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")

# --- Início do Programa ---
if __name__ == "__main__":
    menu_principal()