## 🎮 Pacman DBZ

O jogo **Pac-Man de Dragon Ball** está sendo desenvolvido com a biblioteca **Pygame**, uma ferramenta do **Python** voltada para o desenvolvimento de jogos 2D.

### 🧩 O que é a Pygame
A **Pygame** é uma biblioteca livre e multiplataforma que oferece recursos para:
- **Renderização gráfica 2D** (criação de cenários, personagens e animações);
- **Controle de eventos** (como teclado, mouse e colisões);
- **Execução de sons e músicas**;
- **Gerenciamento de tempo**, essencial para o movimento fluido dos personagens.

Essas funções permitem criar toda a estrutura do jogo — desde as **telas iniciais** até o **nível jogável**, controlando tudo de forma integrada e eficiente.

---

## ✨ Por que escolhemos a Pygame
A escolha da Pygame se deve à sua **facilidade de uso** e à **semelhança com os jogos retrô**, como o Pac-Man original.  
Ela permite que a equipe se concentre na criatividade e nas mecânicas, sem precisar lidar com detalhes complexos de engine gráfica.

Além disso, a Pygame é amplamente utilizada em projetos educacionais e protótipos, sendo ideal para o aprendizado de **lógica de programação, física simples e design de jogos**.

---

## 🖼️ Como a Pygame será usada no projeto
No **Pac-Man de Dragon Ball**, a Pygame será responsável por:

- **Desenhar o mapa** do jogo (paredes, corredores e fundo);
- **Exibir os sprites** do Goku e dos vilões;
- **Controlar o movimento** dos personagens e a detecção de colisões;
- **Gerenciar as telas iniciais** (menu, instruções e créditos);
- **Tocar os sons** de coleta das esferas e efeitos especiais (como o “Kamehameha”).

## 📋 Pré-requisitos

Para executar este projeto, você precisará ter o Python e a biblioteca Pygame instalados.

* **Python 3.12
* **Pygame**

Instalar o Pygame usando o `pip` no seu terminal (CMD, PowerShell ou Bash):

```bash
pip install pygame
```
## 🚀 Como Executar o Projeto

**IMPORTANTE:** O script `menu.py` utiliza caminhos relativos (ex: `client/assets/...`). Por causa disso, ele **precisa** ser executado a partir da pasta raiz do projeto, que é a `pacman_project`.

Siga estes passos para garantir que o programa encontre todos os arquivos (imagens, sons, fontes):

1.  Abra seu terminal (PowerShell, CMD, Bash, etc.).

2.  Navegue com o comando `cd` (change directory) até a pasta `pacman_project` que está dentro do diretório principal.

    *(Ajuste o caminho abaixo para o local onde você salvou a pasta do projeto)*
    ```bash
    # Exemplo de caminho:
    cd C:\Users\SeuUsuario\Downloads\pacmandbz-main\pacmandbz-main\pacman_project
    ```

3.  Uma vez que seu terminal esteja **dentro** da pasta `pacman_project`, execute o script do menu, que está na subpasta `client`:

    ```bash
    python client/menu.py
    ```
