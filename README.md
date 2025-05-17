# SIGAACollector

**SIGAACollector** é uma ferramenta automatizada para coleta, organização e visualização de horários acadêmicos extraídos diretamente do sistema SIGAA. Usando Python, Selenium e Streamlit, o projeto permite:

- Raspagem de disciplinas e horários da tela de matrícula
- Geração automática de um arquivo CSV estruturado
- Visualização com filtros via painel web com Streamlit

---

## 🚀 Tecnologias utilizadas

- Python 3.11+
- Selenium 4+
- Pandas 1.3+
- Streamlit 1.24+

---

## 🔧 Requisitos

1. Google Chrome instalado
2. ChromeDriver compatível com sua versão do navegador (instalado automaticamente com selenium >= 4.6)
3. Sistema operacional com suporte ao ChromeDriver (Windows, Linux ou macOS)

---

## 📂 Estrutura do projeto

SIGAACollector/

├── output/                  # Arquivos CSV gerados automaticamente

├── schedule_dashboard.py    # Painel de visualização com Streamlit

├── sigaa_collector.py       # Script de raspagem com Selenium

├── requirements.txt         # Dependências do projeto

└── .gitignore               # Arquivos ignorados no Git

## 📅 Etapas de Execução

1. Clone o repositório

```
git clone https://github.com/gustavo-f0ntz/SIGAACollector
cd SIGAACollector
```

2. Crie e ative o ambiente virtual (opcional, mas recomendado)

```
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
```

3. Instale as dependências

```
pip install -r requirements.txt
```

## 🧰 Parte 1: Coletar dados do SIGAA

Passos:

1. Acesse o SIGAA normalmente com seu login

2. Navegue até a tela de matrícula com os horários visíveis

3. No terminal, execute:
```
python sigaa_collector.py
```

4. Aguarde o prompt:

```
🔵 Abra o SIGAA, faça login e acesse a tela de matrícula com disciplinas + horários.
🔧 Pressione ENTER aqui quando estiver na tela certa...
```

5. Volte para o terminal e pressione ```ENTER```

6. O script extrairá as disciplinas, locais, dias e horários e gerará:

```
output/subjects_schedule.csv
```

## 📊 Parte 2: Visualizar com painel interativo

Execute o dashboard com:

```
streamlit run schedule_dashboard.py
```

Acesse em seu navegador:

```
http://localhost:8501
```

Recursos do painel:

📅 Filtro por dia da semana

🕒 Filtro por turno (MANHÃ, TARDE, NOITE)

📄 Tabela interativa com os dados filtrados

```text
Versão simples: apenas a tabela com filtros.
Versão com grade estilo SIGAA (disponível no histórico): apresenta as disciplinas em formato de agenda por faixa horária.
```

## 📊 Formato do CSV gerado

<pre>
| DISCIPLINA                       | LOCAL DE AULA   | DIA   | TURNO  | HORÁRIO INICIAL  | HORÁRIO FINAL  |
|----------------------------------|---------------- |-------|--------|------------------|----------------|
| PROGRAMAÇÃO ORIENTADA A OBJETOS  | Lab. inf. 02    | Terça | TARDE  | 13:55            | 15:45          |
| BANCO DE DADOS                   | Lab. inf. 02    | Terça | TARDE  | 15:55            | 17:45          |
</pre>


## 🚫 Aviso legal

Este projeto não quebra autenticação, não coleta dados sensíveis nem acessa APIs privadas do SIGAA.
A raspagem é feita apenas após login manual, a partir de informações já exibidas na tela.

## 📄 Licença

Este repositório está licenciado sob a MIT License. Você pode usar, modificar e distribuir com atribuição.

## 🙌 Autor

Desenvolvido por Gustavo Kesley de Fontes Nunes

Projeto criado com foco em produtividade acadêmica, automação de tarefas e visualização clara de horários curriculares.



