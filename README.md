# stock-news

O projeto visa desenvolver um crawler capaz de buscar dados de sites de notícias sobre empresas listadas na bolsa de valores, com o objetivo de coletar informações relevantes para análise da movimentação das ações dessas empresas. Com a análise de sentimentos das notícias coletadas, será possível avaliar se uma determinada notícia tem potencial para gerar uma alta ou queda na ação daquela empresa. 

# Lista de links
```
https://www.infomoney.com.br/mercados
https://www.infomoney.com.br/economia
https://www.infomoney.com.br/negocios
https://www.infomoney.com.br/politica
https://www.infomoney.com.br/onde-investir
https://www.infomoney.com.br/minhas-financas
```

# Esquema de dados
```json
{
  "tag": "String",
  "category": "String",
  "title": "String",
  "link": "String",
  "content": "String",
  "category": "String"
}
```
# Exemplo extraido

```json
"news": [
  {
    "tag": "Ao vivo",
    "category": "mercados",
    "title": "Ibovespa hoje avança e dólar recua, com crise bancária e regra fiscal no radar; Petrobras (PETR4) oscila e Vale (VALE3) cai 10 minutos atrás.",
    "link": "https://www.infomoney.com.br/mercados/ibovespa-hoje-bolsa-de-valores-ao-vivo-16032023/"
    "content": "EM_DESENVOLVIMENTO"
  }
]
```

### Atenção
Este crawler é um projeto educativo, desenvolvido com o objetivo de aprender sobre coleta e análise de dados. As notícias aqui presentes são coletadas de diversos sites de notícias sobre empresas da bolsa brasileira. gostaria de enfatizar que todo o crédito pelas notícias aqui apresentadas são dos respectivos sites de origem. Obrigado pela compreensão!
