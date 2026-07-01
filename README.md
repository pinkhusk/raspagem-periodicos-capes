# Raspagem de Dados no Portal de Periódicos da CAPES

Script em Python para extração de dados do Portal de Periódicos da CAPES, com suporte a coleta direta via requisição HTTP e processamento alternativo de páginas HTML salvas localmente. Os dados extraídos são armazenados em banco SQLite.

## Objetivo

Este projeto automatiza a busca por termos específicos no Portal de Periódicos da CAPES, extrai os dados dos artigos retornados e armazena as informações em um banco de dados local.

## Funcionalidades

- Realiza buscas no Portal de Periódicos da CAPES.
- Extrai metadados dos resultados encontrados.
- Acessa a página de detalhes de cada artigo.
- Coleta o resumo (`abstract`) dos registros.
- Salva os dados em um banco SQLite.
- Oferece um método alternativo de extração a partir de arquivos HTML salvos localmente.

## Bibliotecas utilizadas

### Método principal

- requests
- beautifulsoup4
- demjson3
- re
- json
- sqlite3

### Método alternativo

- beautifulsoup4
- demjson3
- re
- sqlite3
- os
- unicodedata
- pathlib

## Métodos disponíveis

Este repositório oferece dois modos de extração de dados do Portal de Periódicos da CAPES:

- `raspagem_periodicos_capes.py`: realiza a coleta diretamente no portal por meio de requisições HTTP.
- `raspagem_periodicos_capes_html.py`: realiza a extração a partir de arquivos HTML previamente salvos localmente.

O segundo script pode ser útil quando o método direto não funciona, por exemplo, em casos de expiração de cookies, bloqueio da requisição ou mudanças temporárias na resposta do portal.

## Requisitos

Antes de executar, instale as dependências necessárias:

```bash
pip install requests beautifulsoup4 demjson3
```

## Método principal: coleta direta no portal

O script principal:

- define o termo de pesquisa;
- monta a URL de busca no portal;
- faz a requisição HTTP com cabeçalhos personalizados;
- extrai a lista de itens retornada no HTML;
- acessa cada registro individualmente para obter o resumo (`abstract`);
- salva os dados em uma tabela SQLite.

### Como executar

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
pesquisa = "tcc"
termo = "direitos crianças adolescentes"
```

O valor definido em `pesquisa` será usado para nomear o arquivo `.db`. Assim, ao executar o script com diferentes termos de busca e o mesmo nome de pesquisa, novas tabelas poderão ser adicionadas ao mesmo banco de dados.

### Configuração dos cookies

Antes de executar o script, pode ser necessário atualizar manualmente o valor do campo `"Cookie"` no dicionário `headers`, já que cookies de sessão podem expirar com o tempo. Ferramentas de desenvolvedor do navegador permitem visualizar os cabeçalhos HTTP das requisições feitas pela página, incluindo o campo `Cookie`.

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

Execute o script Python:

```bash
python raspagem_periodicos_capes.py
```

### Saída gerada

Ao final da execução, será criado um arquivo `.db` com o nome definido em `pesquisa`, contendo os registros coletados.

Exemplo:

```bash
tcc.db
```

## Método alternativo: processamento de HTML local

O script `raspagem_periodicos_capes_html.py` foi desenvolvido como alternativa para situações em que a raspagem direta pelo portal não seja possível.

Nesse caso, o processo funciona a partir de arquivos HTML já salvos no computador, contendo páginas de resultados da busca realizada no Portal de Periódicos da CAPES.

### Como funciona

O script alternativo:

- procura arquivos HTML em uma pasta local;
- identifica páginas no padrão `{termo}_pagina1.html`, `{termo}_pagina2.html`, `{termo}_pagina3.html` etc.;
- extrai os itens presentes no bloco JavaScript `const itens = [...]`;
- extrai os resumos presentes nos elementos `<p class="mb-0 small">`;
- remove registros duplicados com base no campo `id`;
- salva os dados em uma tabela SQLite.

### Estrutura esperada dos arquivos

Os arquivos HTML devem estar em uma pasta definida no script, por padrão:

```python
PASTA_HTML = SCRIPT_DIR / "html"
```

O nome dos arquivos deve seguir este padrão:

```text
termo_pagina1.html
termo_pagina2.html
termo_pagina3.html
```

Por exemplo:

```text
direitos_criança_adolescente_pagina1.html
direitos_criança_adolescente_pagina2.html
```

O nome-base dos arquivos é gerado automaticamente a partir do valor definido em `termo`, substituindo os espaços por `_`.

### Como executar o método alternativo

Edite o script `raspagem_periodicos_capes_html.py` com os valores desejados:

```python
pesquisa = "nome da base de dados"
termo = "termos de busca"
```

Verifique se os arquivos HTML estão salvos na pasta correta e com o nome esperado.

Depois, execute:

```bash
python raspagem_periodicos_capes_html.py
```

### Saída gerada pelo método alternativo

Assim como no método principal, será criado ou atualizado um arquivo `.db` com o nome definido em `pesquisa`.

Exemplo:

```bash
pesquisa.db
```

A tabela criada no banco terá nome derivado do termo pesquisado, com caracteres normalizados para evitar problemas de compatibilidade com nomes de arquivo e identificadores no SQLite.

### Quando usar este método

Use o método alternativo quando:

- o script principal não conseguir acessar corretamente os resultados do portal;
- os cookies da sessão expirarem;
- você já tiver salvo manualmente as páginas HTML da busca;
- quiser trabalhar com uma cópia local dos resultados.

## Possíveis erros

- A busca não retorna resultados esperados.
- O HTML da página vem incompleto ou diferente do esperado.
- O script não encontra a variável `const itens`.
- O portal responde com bloqueio, redirecionamento ou erro de acesso.
- Nenhum arquivo HTML é encontrado na pasta esperada pelo método alternativo.
- O número de textos extraídos no HTML não corresponde ao número de itens encontrados.

Em muitos desses casos, pode ser necessário atualizar novamente o valor do campo `"Cookie"` no cabeçalho da requisição ou revisar a estrutura dos arquivos HTML utilizados.

## Observações

- O script foi desenvolvido para fins de pesquisa e organização de dados bibliográficos.
- A estrutura de extração pode precisar de ajustes caso o Portal de Periódicos da CAPES altere o formato da página.
- O uso do script deve respeitar as condições de acesso e uso da plataforma.
- O método alternativo foi desenvolvido com o apoio da IA Kilo Code, extensão de codificação com IA integrada ao VsCodium por meio do ecossistema de extensões compatíveis.
