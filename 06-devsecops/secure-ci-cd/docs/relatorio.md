# Esteira CI CD com análise de segurança e aplicação em container

## Identificação

Disciplina: DevSecOps — Avaliação Parcial II. Professor: Alecsandre Camilo Rosa. Entrega e apresentação: 19 de outubro de 2026. Integrantes, RA, instituição e turma: preencher com os dados do grupo antes da entrega.

Este documento descreve a implementação da prova de conceito TechSecure. Os resultados locais já verificados são separados das evidências de CI e Docker, que precisam ser anexadas após uma execução real.

## Objetivo

Implementar uma esteira básica de integração e entrega contínuas que execute build, testes e análise estática antes de implantar uma aplicação em container. O cenário utiliza a empresa fictícia TechSecure Solutions e demonstra como um problema de segurança pode ser identificado e corrigido durante o desenvolvimento.

## Aplicação escolhida

Escolhemos uma calculadora web de soma de inteiros. A simplicidade permite concentrar a apresentação nos controles da pipeline. A interface fornece uma operação de soma e consulta a saúde e a versão da aplicação. A API aceita somente dois inteiros de até nove dígitos separados por um sinal de adição. A operação é implementada com conversão para int e soma, sem execução dinâmica da entrada.

## Arquitetura

O código fica no GitHub, no repositório cybersecurity-labs, dentro de 06-devsecops/secure-ci-cd. Pushes e pull requests que alteram esse laboratório iniciam o workflow DevSecOps AP II. Um runner hospedado executa as etapas em sequência. O gate precisa ser aprovado antes da construção da imagem e do deploy. Após iniciar o container, o workflow valida endpoints HTTP e captura a página com Playwright. Logs e resultados são preservados como artefatos.

O deploy é temporário e termina com o job. O container local é utilizado para a apresentação interativa. Esta implementação não inclui um servidor de hospedagem persistente.

## Tecnologias utilizadas

Python 3.12 fornece a aplicação e o framework unittest. Bandit 1.8.6 executa a análise estática. Docker empacota a aplicação. GitHub Actions automatiza a esteira e preserva os artefatos. Playwright captura a evidência visual no CI. A aplicação utiliza somente a biblioteca padrão no runtime.

## Descrição da pipeline

O checkout obtém o código e não preserva credenciais Git no workspace. O build instala a ferramenta de análise e executa compileall, que verifica a sintaxe e gera bytecode. Em seguida, unittest valida a soma, os limites de entrada, a rejeição de conteúdo inválido e as respostas HTTP.

A análise didática executa Bandit sobre uma amostra isolada e verifica o achado B307. O gate analisa a aplicação real e interrompe a esteira se encontrar problemas de severidade média ou alta. Somente depois desse gate o Docker constrói a imagem e inicia o container. Um smoke test confirma a saúde, a versão do commit, o resultado do cálculo e a resposta 400 para uma entrada inválida.

O workflow captura uma imagem da aplicação funcionando, publica os artefatos e encerra o container. Falhas anteriores impedem o deploy. A coleta de evidências usa always para preservar resultados parciais quando houver falha.

## Dockerfile e execução

A imagem parte de python:3.12-slim. O Dockerfile define o diretório de trabalho, cria usuário e grupo com identificador 10001, copia apenas app, muda para o usuário sem privilégios, expõe a porta 8080 e define health check. O comando final inicia o servidor WSGI educacional.

O comando de deploy limita memória e CPU, remove capabilities, habilita no-new-privileges e torna o sistema de arquivos somente leitura. A porta publicada é vinculada ao loopback. A variável APP_VERSION registra o commit implantado. O Dockerfile completo acompanha o repositório e deve ser incluído no anexo da entrega escrita.

## Ferramenta de segurança e achado

Bandit realiza análise estática de Python. A amostra security-fixtures/unsafe_calculator.py utiliza eval(expression), identificada pela regra B307. Na execução local com Bandit 1.8.6, o achado apresentou severidade MEDIUM e confiança HIGH. Se uma entrada não confiável alcançar essa função, poderá ser interpretada como código Python.

A mitigação implementada em app/calculator.py define uma gramática restrita para dois inteiros positivos e realiza a soma explicitamente. A amostra insegura fica fora da imagem e não é disponibilizada por uma rota. O achado demonstra uma classe de problema; não representa uma exploração realizada nem uma CVE.

## Resultados e evidências

Na validação local de 7 de outubro de 2026, os dez testes automatizados passaram. O Bandit identificou B307 na amostra didática, com severidade média e confiança alta. O gate da aplicação não identificou achados médios ou altos. Esses resultados cobrem os testes e o scan locais, sem comprovar a imagem Docker ou o deploy no CI.

Completar após a execução: URL do run, SHA analisado, resultado de cada etapa, identificação da imagem, logs do container, smoke.json e screenshot. Acrescentar prints do run aprovado e do run bloqueado pelo gate. Não declarar a entrega concluída enquanto essas evidências estiverem pendentes.

## Dificuldades e limitações

A preparação foi validada em um ambiente sem Docker disponível. Por esse motivo, o build da imagem e o container devem ser comprovados no GitHub Actions ou no computador do grupo. Registrar aqui as dificuldades realmente observadas nessas execuções, suas causas e as soluções aplicadas.

A imagem base utiliza uma tag mutável. Para maior reprodutibilidade, uma evolução pode fixar seu digest e automatizar atualizações. As Actions também usam tags de versão; uma evolução de hardening pode fixar SHAs completos. Bandit não cobre vulnerabilidades da imagem base ou todas as falhas da aplicação. O servidor WSGI é educacional e não deve ser usado como referência de produção.

## Conclusão

A implementação conecta versionamento, validação funcional e análise de segurança antes do deploy. A correção de eval por validação restrita demonstra como um controle de entrada pode ser verificado junto à automação. A conclusão experimental sobre o fluxo completo deve ser confirmada com os artefatos reais da execução em Docker, incluindo a alteração do código e a nova versão implantada.

## Referências

Bandit. Documentação da ferramenta e regra B307. https://bandit.readthedocs.io/en/latest/ e https://bandit.readthedocs.io/en/latest/blacklists/blacklist_calls.html#b307-eval

GitHub. Segurança em GitHub Actions. https://docs.github.com/en/actions/reference/security/secure-use

Docker. Dockerfile reference. https://docs.docker.com/reference/dockerfile/

Enunciado da AP II de DevSecOps fornecido pela disciplina, versão atualizada de 2026.
