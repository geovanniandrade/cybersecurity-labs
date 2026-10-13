# MAC Flooding e Port Security

## 🎯 Objetivo
Simular um ataque de MAC Flooding em camada 2 e aplicar Port Security como medida de contenção.

## 🛠️ Ambiente e ferramentas
- Kali Linux com `macof`
- Switch com suporte a Port Security
- Topologia de laboratório

## 🔎 Procedimento
1. Simular o envio de múltiplos endereços MAC:
   ```bash
   macof -i eth0
   ```
2. Observar o comportamento da rede e da tabela CAM.
3. Configurar Port Security no switch:
   ```text
   switchport port-security
   switchport port-security maximum 2
   switchport port-security violation shutdown
   ```
4. Validar a contenção no ambiente de testes.

## ✅ Resultados
- Comportamento anormal associado ao MAC Flooding identificado no laboratório.
- Port Security aplicado para limitar endereços MAC por porta.
- Contenção e estabilização da rede relatadas após a mitigação.

## 📸 Evidências
- [Topologia](topology.png)
- [Simulação do ataque](attack.png)
- [Mitigação aplicada](mitigation.png)

## 🛡️ Mitigações
- Limitar endereços MAC permitidos por porta.
- Configurar ações para violações de Port Security.
- Monitorar mudanças anormais na tabela CAM.

> Laboratório educacional realizado em ambiente controlado.
