# Detecção de Força Bruta com Wazuh

## Objetivo
Simular tentativas de autenticação malsucedidas no Windows e analisar os eventos detectados pelo Wazuh.

## Ambiente e ferramentas
- Windows Endpoint com Wazuh Agent
- Wazuh SIEM (coleta e análise de eventos)
- Kali Linux (opcional no cenário)

## Procedimento
1. Simular tentativas de login com senha incorreta no Windows:
   ```cmd
   runas /user:vboxuser cmd
   ```
2. Coletar os eventos pelo Wazuh Agent.
3. Analisar os alertas e detalhes de autenticação no Wazuh.

## Resultados
- Eventos de autenticação malsucedida apresentados no Wazuh.
- Análise das tentativas de login e dos registros associados.
- Evidência de bloqueio de conta documentada no laboratório.

## Evidências
- [Eventos de força bruta](images/03-bruteforce-events-detection.png)
- [Detalhes dos logs](images/04-event-details-log-analysis.png)
- [Bloqueio de conta](images/05-account-lockout-evidence.png)

## Mitigações recomendadas
- Política de bloqueio de conta e autenticação multifator (MFA).
- Senhas fortes e restrição de contas privilegiadas.
- Monitoramento de eventos de autenticação.

> Laboratório educacional realizado em ambiente controlado.
