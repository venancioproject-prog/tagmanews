# Tagma - Versão 1 (Static Frontend)

Esta é a **Versão 1** do novo portal Tagma (evolução do antigo TN&C). Este pacote foi preparado com extremo carinho e rigor técnico para que você possa visualizá-lo imediatamente no navegador e hospedá-lo no GitHub Pages.

## Como testar agora mesmo:
Basta dar um duplo-clique no arquivo `index.html` e ele abrirá perfeitamente no seu navegador Chrome/Edge/Safari.

## Como colocar no ar (GitHub Pages):
Como você ainda não definiu a equipe de Backend/Frontend, preparei este código para ser **100% Estático e Livre de Dependências**. Você não precisa instalar Node.js, Python ou qualquer outra coisa.

1. Crie um novo repositório público no seu GitHub (ex: `tagma-v1`).
2. Faça o upload do arquivo `index.html` que está nesta pasta diretamente para a raiz desse repositório.
3. No GitHub, vá na aba **Settings** > **Pages**.
4. Em "Source", selecione a branch `main` e a pasta `/ (root)` e clique em **Save**.
5. Aguarde 2 minutos e o seu site já estará no ar com um link oficial do GitHub!

### O que tem nessa Versão 1?
- **Integração do Conteúdo TN&C:** Incorporei as manchetes e categorias do site antigo (como a matéria da Carla Marins e o bloco de Cultura) dentro do novo Design System de alto padrão.
- **Preparação AdSense:** Já deixei um *Ad Slot* (Espaço Publicitário) otimizado na barra lateral. O espaço tem altura fixa para que a tela não "pule" e passe liso na auditoria de SEO do Google.
- **Código Limpo:** Sem as tags confusas do Stitch. É HTML puro rodando a CDN do Tailwind CSS. É o protótipo perfeito para aprovar o visual com a diretoria antes de contratarmos a equipe para montar a infraestrutura Headless (Next.js + Admin).
