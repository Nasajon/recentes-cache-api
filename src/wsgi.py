# Importando arquivos de configuração
from src.settings import DEBUG, SERVER_PORT, application

# TODO Importar todos os controllers (se não, as rotas não existirão)

import src.controller.recents_controller

if __name__ == '__main__':
    # application.run(port=SERVER_PORT, host="0.0.0.0", debug=DEBUG)
    application.run(port=SERVER_PORT)

