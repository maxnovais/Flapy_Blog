#Flapy_Blog
- - -

Flapy_Blog é um pequeno blog feito utilizando Python e o micro(nem tão micro)-framework Flask.

**Motivação:** Hoje temos muitos blogs feitos através de tutoriais de Python utilizando os frameworks Django e Flask, no entanto, a maioria não se encaixa no que eu digo de *página pessoal*, esse, trás consigo funcionalidades para marcação de estudo, ou seja, um padrão para escrita de artigo em Markdown, um micro bookmark e interação através de comentários.

- - -

##Versão
1.0b

- - -

##Componentes utilizados:
- Flask
- Flask-Security (e todas suas dependências)
- Flask-Pagedown
- WTForms
- Markdown
- Bootstrap
- MomentJS

- - -

##Instalação
- Clone o link disponível no GitHub
- Crie o ambiente virtual
`virtualenv *nome do ambiente* `
- Entre no ambiente virtual
`source *nome do ambiente*/bin/activate `
- Execute a instalação pip do requirements.txt
`pip install -r requirements.txt `

- - -

##Configuração
Anexo junto o arquivo **config.py** em que existem configurações necessárias como e-mail utilizado pelo Flask-Security, quantidade de itens por página, e moderação de comentários. 
**Importante:** Não utilizo o model *Roles*, devido a isso, não existem diferenças nos cadastros gerados na aplicação, para não ter problema, após o cadastro de pessoas autorizadas, prossiga com alteração da propriedade **SECURITY_REGISTERABLE** do arquivo config.py.