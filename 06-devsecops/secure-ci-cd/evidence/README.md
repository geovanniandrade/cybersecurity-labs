# Evidências de execução

Baixe o artifact `devsecops-evidence-*` na página da execução do GitHub Actions. Os arquivos gerados não são evidências até a execução ocorrer de fato.

| Arquivo | O que comprova |
|---|---|
| tests.txt | Execução dos testes |
| bandit-fixture.json e finding.txt | Achado B307 |
| bandit-app.json | Resultado do gate na aplicação |
| docker-build.txt e image.json | Build e identificação da imagem |
| container.json e container.log | Container implantado |
| smoke.json | HTTP, cálculo, entrada inválida e versão |
| application.png | Aplicação em execução |
| tool-versions.txt | Versões de Python e Bandit |

Inclua também prints da página da pipeline, do código alterado e do commit. Preserve a URL e o SHA de cada run. Os artefatos do CI são retidos por 30 dias; baixe-os antes do vencimento. Revise dados identificáveis antes de publicar qualquer captura.
