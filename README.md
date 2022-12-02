# recentes-cache-api
API para consulta e armazenamento de uma cache dos registros recentemente acessado para qualquer usuário e recurso.

#Autenticação
A autenticação da api se faz por meio da apikey então em cada requisição será necessário um header em todas as requisições com a seginte informação
```
{
    'apikey' : API_KEY_DA_APLICACAO
}
```


A api no momento possui um endpoint com dois verbos


 

[POST]
https://base_url/recents

 * Utilizado para guardar um objeto em uma chave
 * Possui um corpo obrigatório
 * Possui argumentos obrigatórios
 ```
    scope: Id do escopo do registro (id da empresa, estabelecimento, grupo empresarial, etc )
    tenant: tenant do registro que será guardado no cache
    email: email do usuario que está guardando no cache a entidade
    entity: Nome da entidade a ser guardada no cache
    primary_key: Nome do campo utiulizado como chave primaria da entidade
 ```

  ```
 {
    campos da entidade que deseja guardar 
 }
 ```

  A única regra é que a entidade precisa ter obrigatoriamente o campo passado no argumento priimary_key pois ele que definirá a a igualdade do objeto na lista

 * O retorno é um 201 created com um corpo vazio
 ```
    '', 201
 ```
 * Exemplo:
  ```
  [POST] localhost:5000/recents?scope=scope&tenant=tenant&email=email&entity=entity&primary_key=pk
  [BODY] { 	"pk" : 11, "nome" : "TESTE"}
  [RETORNO] '' 201
  ```

[GET]
https://base_url/recents

 * Utilizado para recuperar uma lista de objetos guardados em uma chave
 * Possui argumentos obrigatórios
 ```
    scope: Id do escopo do registro (id da empresa, estabelecimento, grupo empresarial, etc )
    tenant: tenant do registro que será guardado no cache
    email: email do usuario que está guardando no cache a entidade
    entity: Nome da entidade a ser guardada no cache
    primary_key: Nome do campo utiulizado como chave primaria da entidade
 ```

 * o Retorno é uma lista de objetos, ordenados pelo momento que foram tocados/guardados, e status 200 OK
 [
    {
        campos da entidade...
    }
 ],
 200
  
 * Exemplo:
  ```
  [GET] localhost:5000/recents?scope=scope&tenant=tenant&email=email&entity=entity&primary_key=pk
  [RETORNO] [{"pk": 11,"nome": "TESTE"	}],  200
  ```

 # ENVS
 * PYTHONPATH: caminho da rais de sua máquina até a pasta do projeto
 * FLASK_APP: caminho relativo do seu projeto até o arquivo sgi (src/wsgi.py)
 * SERVER_PORT: porta que o servidor ficará escutando
 * DIRETORIO_ENDPOINT: Url base do diretório
 * APIKEY_VALIDATE_URL: Url de validação de api key
 * REDIS_HOST: Host do serviço do redis
 * REDIS_PORT: Porta que o serviço do redis está ouvindo 
 * REDIS_DB: Nome/numero da database do redis 
 * EXPIRATION_SECONDS: Tempo de expiração do cache

