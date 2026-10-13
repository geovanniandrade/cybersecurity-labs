# SSH Brute Force — Cisco IOS

## 🎯 Objetivo
Simular um ataque de força bruta SSH contra um roteador Cisco IOS e implementar controles de Defense in Depth.

## 🛠️ Ambiente e ferramentas
- GNS3, Cisco IOS e switch Layer 2
- Kali Linux e Hydra
- Atacante: `192.168.1.100` | Alvo: `192.168.1.1`

## 🔎 Procedimento
1. Identificar credenciais fracas e configurações inseguras, incluindo Telnet habilitado e ausência de ACL.
2. Simular um ataque de força bruta SSH com Hydra.
3. Aplicar senha forte com `secret`, ACL e limitação de tentativas de login.
4. Desabilitar Telnet e validar o acesso restrito por SSH.

## ✅ Resultados
- Acesso administrativo obtido no cenário inicial de teste.
- Ataque com Hydra bloqueado após as mitigações.
- Acesso SSH restrito às origens autorizadas.

## 📸 Evidências
- [Relatório técnico completo (PDF)](Relatorio_Tecnico.pdf)

## 🛡️ Mitigações
- Senhas fortes e limitação de tentativas de login.
- ACL para acesso administrativo.
- Desativação de Telnet e uso de SSH.

> Laboratório educacional realizado em ambiente controlado.
