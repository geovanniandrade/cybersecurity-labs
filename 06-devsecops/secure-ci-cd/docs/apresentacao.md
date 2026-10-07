# Roteiro de apresentação e vídeo

## Apresentação de 15 minutos

| Tempo | Conteúdo | Participação sugerida |
|---|---|---|
| 0 a 2 min | Cenário, objetivo e arquitetura | Integrante 1 |
| 2 a 4 min | Aplicação, testes e Dockerfile | Integrante 2 |
| 4 a 7 min | Bandit, B307 e correção | Integrante 3 |
| 7 a 11 min | Alteração, commit, push e pipeline | Integrante 4 |
| 11 a 14 min | Deploy, versão e evidências | Integrante 5 |
| 14 a 15 min | Limitações e conclusão | Grupo |

Adapte a divisão ao número real de participantes, até cinco. Todos devem falar. Deixe uma execução anterior e seus artefatos disponíveis, pois a instalação do navegador e o build podem ultrapassar o tempo da apresentação.

## Vídeo de 5 a 10 minutos

1. Mostre o README e explique a arquitetura.
2. Mostre a página funcionando no container local.
3. Abra testes, Dockerfile e workflow.
4. Mostre B307 na amostra e explique severidade, impacto e correção.
5. Altere uma frase, faça commit e push e mostre o início automático do run.
6. Mostre build, testes, gate, imagem, deploy e smoke test.
7. Baixe o artifact e mostre a aplicação atualizada e a versão.
8. Explique que o runner é temporário e que a aplicação não tem URL pública permanente.

Pode acelerar a espera no vídeo, identificando o corte. Não apresente logs de uma execução anterior como se fossem da alteração atual.

## Perguntas para ensaiar

- Qual a diferença entre integração contínua e deploy automático?
- O que B307 detecta e por que eval é arriscado?
- Por que o exemplo inseguro não está na imagem?
- Qual falha impede o deploy nesta política?
- Como provar que a alteração chegou à aplicação?
- Quais análises de segurança ainda faltam?
- Onde o container roda e quanto tempo permanece ativo?
