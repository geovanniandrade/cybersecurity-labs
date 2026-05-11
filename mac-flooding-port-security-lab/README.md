# 🚨 Laboratório de Resposta a Incidente: Ataque MAC Flooding com Port Security

## 🎯 Objetivo

Simular, detectar e mitigar um ataque de **MAC Flooding** em um ambiente controlado, reproduzindo um incidente real de segurança em **Camada 2**, sob a perspectiva de um **SOC — Security Operations Center**.

---

## 🧠 Cenário

Durante a operação normal da rede, usuários começaram a relatar:

- Instabilidade intermitente de conectividade
- Alta latência
- Acesso inconsistente a sistemas internos

Esse comportamento indicava uma possível anomalia de rede, possivelmente relacionada a um ataque em **Camada 2** ou a uma configuração incorreta no switch.

---

## 🚨 Detecção

O incidente foi identificado a partir de comportamentos anormais na rede:

- Degradação repentina de desempenho
- Aumento de tráfego broadcast
- Switch apresentando comportamento semelhante ao de um hub

### Indicadores de Comprometimento — IoCs

- Excesso de entradas de endereços MAC
- Mudanças rápidas na tabela CAM
- Flooding de endereços MAC desconhecidos

---

## 🔍 Investigação

Para validar a hipótese, foi utilizado um ambiente de laboratório controlado.

### 🧪 Simulação do Ataque

- **Ferramenta:** `macof` — Kali Linux
- **Objetivo:** Sobrecarregar a tabela CAM do switch com endereços MAC falsos

```bash
macof -i eth0
