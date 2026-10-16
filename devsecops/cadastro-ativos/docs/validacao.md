# Validação

## Dashboard

11 testes unittest passaram: CRUD, migração do esquema anterior com preservação de IDs e dados, filtros, métricas globais, valores em centavos, CSRF, entradas SQL e HTML tratadas como dados. Chromium validou cadastro, detalhes, edição, confirmação de remoção e busca em 1440 px e 390 px. As prévias contêm dados fictícios.

O usuário confirmou o dashboard v2 rodando na VM após build e atualização manual. A preservação dos registros deve ser capturada nas evidências reais.

## Pipeline e updater

11 testes passaram novamente em 08/10/2026 UTC. Bandit 1.9.4 e pip-audit 2.10.1 concluíram sem achados locais. Relatórios em security/.

O script passou em simulações de imagem igual, falha de pull, falha de backup, deploy saudável e rollback após falha de saúde. Bash e YAML foram verificados. Simulações não substituem Docker real: o ambiente de preparação não possui Docker. A execução no Actions e a ativação do timer na VM aguardam validação.

A atividade ainda precisa das evidências do pipeline/deploy e de ao menos um achado real de segurança com correção ou mitigação.
