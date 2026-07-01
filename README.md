# Raspagem de Dados no Portal de Periódicos da CAPES
Script em Python para raspagem de dados no Portal de Periódicos da CAPES, com coleta de metadados e resumo dos resultados em banco SQLite.

## Objetivo

Este projeto automatiza a busca por termos específicos no Portal de Periódicos da CAPES, extrai os dados dos artigos retornados e armazena as informações em um banco de dados local.

## Funcionalidades

- Realiza buscas no Portal de Periódicos da CAPES.
- Extrai metadados dos resultados encontrados.
- Acessa a página de detalhes de cada artigo.
- Coleta o resumo (`abstract`) dos registros.
- Salva os dados em um banco SQLite.

## Bibliotecas utilizadas

- requests
- beautifulsoup4
- demjson3
- re
- json
- sqlite3

## Estrutura do script

O script:

- Define o termo de pesquisa.
- Monta a URL de busca no portal.
- Faz a requisição HTTP com cabeçalhos personalizados.
- Extrai a lista de itens retornada no HTML.
- Acessa cada registro individualmente para obter o resumo (`abstract`).
- Salva os dados em uma tabela SQLite.

## Requisitos

Antes de executar, instale as dependências necessárias:

```bash
pip install requests beautifulsoup4 demjson3
```

## Como executar

Clone este repositório:

```bash
git clone https://github.com/seu-usuario/raspagem-periodicos-capes.git
```

Acesse a pasta do projeto:

```bash
cd raspagem-periodicos-capes
```

Edite o script Python `raspagem_periodicos_capes.py` nas linhas que definem a pesquisa:

```python
pesquisa = "nome_da_pesquisa"
termo = "termo da pesquisa"
```

Por exemplo:

```python
pesquisa = "quilombos"
termo = "quilombo território"
```

O valor definido em `pesquisa` será usado para nomear o arquivo `.db`. Assim, ao executar o script com diferentes termos de busca e o mesmo nome de pesquisa, novas tabelas poderão ser adicionadas ao mesmo banco de dados.

Execute o script Python:

```bash
python raspagem_periodicos_capes.py
```

## Saída gerada

Ao final da execução, será criado um arquivo `.db` com o nome definido em `pesquisa`, contendo os registros coletados.

Exemplo:

```bash
quilombos.db
```
## Possíveis erros

Durante a execução, o script pode falhar caso o Portal de Periódicos da CAPES bloqueie a requisição, altere a estrutura da página ou exija cookies atualizados para permitir o acesso aos resultados.

Um erro comum acontece quando os cookies informados no cabeçalho da requisição expiram. Nesse caso, atualize manualmente o valor do campo `"Cookie"` no dicionário `headers`.

### Como atualizar os cookies da requisição

O procedimento é semelhante no Firefox, Chrome e outros navegadores baseados em Chromium:

1. Acesse o Portal de Periódicos da CAPES no navegador.
2. Pressione `F12` para abrir as Ferramentas de Desenvolvedor.
3. Abra a aba **Rede** ou **Network**.
4. Recarregue a página.
5. Clique em uma requisição feita para o domínio do portal.
6. Abra a seção **Headers**, **Cabeçalhos** ou **Request Headers**.
7. Localize o campo `Cookie`.
8. Copie o valor completo e substitua no script.

Exemplo:

```python
headers = {
    ...
    "Cookie": "COLE_AQUI_O_VALOR_ATUALIZADO",
    ...
}
```

### Sinais de que os cookies precisam ser atualizados

- A busca não retorna resultados esperados.
- O HTML da página vem incompleto ou diferente do esperado.
- O script não encontra a variável `const itens`.
- O portal responde com bloqueio, redirecionamento ou erro de acesso.

### Observação

Como cookies de sessão expiram com o tempo, pode ser necessário repetir esse procedimento periodicamente.

## Observações

- O script foi desenvolvido para fins de pesquisa e organização de dados bibliográficos.
- A estrutura de extração pode precisar de ajustes caso o Portal de Periódicos da CAPES altere o formato da página.
- O uso do script deve respeitar as condições de acesso e uso da plataforma.

## Licença

Este projeto está licenciado sob a licença Creative Commons Attribution-NonCommercial 4.0 International Public License.
