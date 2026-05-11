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
```

---

## 📊 Comportamento Observado

- **Overflow** da tabela CAM
- **Remoção** de endereços MAC legítimos
- **Switch** passando a encaminhar tráfego para todas as portas

Esse comportamento confirmou a ocorrência de um ataque de **MAC Flooding**.

---

## ⏱️ Linha do Tempo do Incidente

1. Usuários relataram instabilidade na rede
2. Comportamento anormal de broadcast foi identificado
3. Hipótese levantada: ataque em Camada 2
4. Ataque reproduzido em ambiente de laboratório
5. MAC Flooding confirmado
6. Port Security implementado
7. Rede estabilizada após a mitigação

---

## 💥 Impacto

O ataque causou:

- Instabilidade na rede
- Perda de segmentação lógica
- Aumento de tráfego broadcast
- Possível exposição de tráfego para captura de pacotes

### Riscos em um Ambiente Real

- Interceptação de credenciais
- Vazamento de dados
- Movimento lateral não autorizado
- Redução da disponibilidade da rede
- Exposição de comunicações internas

---

## 🛡️ Mitigação — Resposta ao Incidente

Para conter o ataque, foi implementado o recurso de **Port Security** no switch.

### 🔐 Controles de Segurança Aplicados

- Limitação do número de endereços MAC por porta
- Restrição de dispositivos não autorizados
- Definição de ações em caso de violação
- Bloqueio automático da porta em caso de comportamento suspeito

### Exemplo de Configuração

```bash
switchport port-security
switchport port-security maximum 2
switchport port-security violation shutdown
```

---

## ✅ Resultado

Após a implementação dos controles de segurança:

- O ataque foi contido
- A porta afetada foi protegida contra excesso de endereços MAC
- O comportamento anormal de broadcast foi reduzido
- A rede voltou a operar de forma estável
- A superfície de ataque em Camada 2 foi reduzida

---

## 📸 Evidências

### 🔴 Execução do Ataque

![Ataque MAC Flooding](./attack.png)

### 📊 Comportamento da Rede

![Comportamento da Rede](./topology.png)

### 🛡️ Mitigação Aplicada

![Mitigação com Port Security](./mitigation.png)

---

## 🚀 Competências Demonstradas

- Análise de incidente de rede
- Detecção de anomalias em Camada 2
- Simulação controlada de ataque MAC Flooding
- Uso de Kali Linux e ferramenta `macof`
- Análise de impacto e risco
- Implementação de Port Security
- Mentalidade Blue Team / SOC
- Documentação técnica de resposta a incidente

---

## 🧠 Principais Aprendizados

Este laboratório demonstra a importância de:

- Proteger portas de switch contra dispositivos não autorizados
- Monitorar alterações anormais na tabela CAM
- Aplicar controles preventivos em Camada 2
- Utilizar Port Security como medida de contenção
- Correlacionar sintomas de rede com possíveis incidentes de segurança

---

## ⚠️ Aviso Legal

Este projeto foi realizado em um ambiente de laboratório controlado, exclusivamente para fins educacionais e profissionais.
