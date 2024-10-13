
## Configuração e Uso do Git <img src="https://git-scm.com/images/logos/downloads/Git-Icon-1788C.png" width="20"/> <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="20"/>

1. Adicionar o nome de usuário:
   ```bash
   git config --global user.name "seu nome de usuário"
   ```

2. Adicionar o e-mail:
   ```bash
   git config --global user.email "seu.email@example.com"
   ```

3. Verificar o status do commit:
   ```bash
   git status
   ```

4. Atualizar o repositório local:
   ```bash
   git pull
   ```

5. Executar o commit local:
   ```bash
   git commit -m "Descrição da alteração"
   ```

6. Fazer upload do commit para o GitHub:
   ```bash
   git push
   ```

> ⚠️ **Muito importante**: Caso seja adicionado algum pacote/biblioteca, é necessário executar o comando abaixo para que o container seja gerado corretamente:

   ```bash
   pip freeze > requirements.txt
   ```
