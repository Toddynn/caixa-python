# Sistema de Registro de Caixa - Estudo Python

---

Este é um projeto simples de estudo em Python para simular um sistema de registro de entrada e saída de caixa. Ele foi desenvolvido com o objetivo de praticar conceitos de:

* Manipulação de arquivos (`.txt`)
* Uso de módulos Python para envio de e-mails (`smtplib`, `email`)
* Trabalho com datas (`datetime`)
* Gerenciamento de variáveis de ambiente (`python-dotenv`)
* Interação via console

## Funcionalidades

* Registrar novas movimentações (entrada/saída)
* Listar movimentações do dia
* Enviar o registro do dia por e-mail (com anexo)

## Como Usar

1.  **Clone este repositório** (ou baixe os arquivos).
2.  **Instale as dependências:**
    ```bash
    pip install python-dotenv
    ```
3.  **Configure as variáveis de ambiente:**
    * Crie um arquivo chamado `.env` na mesma pasta do script principal.
    * Adicione suas credenciais de e-mail (usando **senha de aplicativo** para o Gmail):
        ```
        REMETENTE_EMAIL=seu_email@gmail.com
        REMETENTE_SENHA=sua_senha_de_app
        DESTINATARIO_EMAIL=email_do_seu_pai@exemplo.com
        ```
4.  **Execute o script:**
    ```bash
    python sistema_caixa.py
    ```

Siga as opções no console para interagir com o sistema.

---
