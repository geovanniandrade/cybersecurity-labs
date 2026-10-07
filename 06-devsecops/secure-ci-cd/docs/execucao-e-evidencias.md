# Guia de execução e evidências

## Antes de começar

Leia o README, instale Git, Python 3.12 e Docker Desktop. Clone a branch do laboratório. Nenhuma credencial corporativa, token ou dado real é necessário para a aplicação. O workflow não usa secrets e não implanta em infraestrutura da empresa.

## Validar a pipeline

Após o push ou abertura do pull request, abra Actions e aguarde o run. Uma execução aprovada deve mostrar todas as etapas concluídas, incluindo o deploy e a captura visual. Baixe o artifact de evidências e compare `smoke.json`, `application.png` e o SHA da execução.

Se o GitHub pedir aprovação para um workflow de contribuição, aprove apenas após revisar o código. A pipeline requer que Actions esteja habilitado e que a conexão usada para publicar tenha permissão para gravar workflows.

## Prints para a entrega

| Número | Captura | Explicação para a legenda |
|---|---|---|
| 01 | Repositório e estrutura | Onde estão código, Dockerfile, testes e pipeline |
| 02 | Pipeline com etapas | Sequência automática após a alteração |
| 03 | Build da aplicação | Compilação de bytecode e preparação |
| 04 | Testes | Quantidade, aprovação e casos inválidos |
| 05 | Achado B307 | Regra, componente, severidade e confiança |
| 06 | Gate da aplicação | Resultado do scan na versão corrigida |
| 07 | Build e image inspect | Tag e identificação da imagem |
| 08 | Container e smoke test | Container iniciado e HTTP validado |
| 09 | Aplicação | Página e versão do commit implantado |
| 10 | Commit antes e depois | Alteração visível e novo run |
| 11 | Gate reprovado | Imagem e deploy bloqueados na demonstração |

## Problemas e diagnóstico

| Sintoma | Ação |
|---|---|
| Workflow não aparece | Verificar Actions habilitado, branch e filtro de caminhos |
| Falha ao baixar imagem ou pacote | Conferir log e acesso a Docker Hub e PyPI |
| Porta local ocupada | Encerrar a aplicação do próprio laboratório ou escolher outra porta e adaptar smoke test |
| Nome de container ocupado | Inspecionar o container antes de removê-lo |
| Scan didático falha | Conferir exit code e JSON; B307 deve aparecer |
| Gate falha | Corrigir o achado em app e refazer commit |
| Screenshot falha | Verificar instalação do Chromium e etapa de deploy |

## Limite do deploy

O deploy automático de demonstração ocorre no runner do GitHub e dura apenas o job. A aplicação não recebe uma URL pública permanente. Para uma demonstração ao vivo no navegador, mantenha o container local ativo. Se a avaliação exigir que o ambiente continue disponível após o término da pipeline, será necessário configurar um destino persistente; essa integração não está incluída nesta versão.
