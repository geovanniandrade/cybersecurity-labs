# 🔐 Ataque de Força Bruta SSH e Defesa em Profundidade em Cisco IOS

Este projeto demonstra um laboratório prático de cibersegurança, simulando um ataque de força bruta via SSH contra um roteador Cisco IOS e a implementação de controles defensivos utilizando o conceito de **Defense in Depth**.

> 📄 **Relatório Técnico:** [Visualizar PDF](./Relatorio_Tecnico.pdf)

---

## 🎯 Objetivo

Demonstrar como credenciais fracas e configurações inseguras podem permitir o comprometimento completo de um dispositivo de rede, além de apresentar como controles adequados de segurança podem mitigar esses riscos.

---

## 🧱 Ambiente de Laboratório

- GNS3
- Roteador Cisco IOS
- Kali Linux — atacante
- Switch Layer 2

**Rede:**

- Atacante: `192.168.1.100`
- Alvo: `192.168.1.1`

---

## ⚠️ Vulnerabilidades Identificadas

- Credenciais fracas: `admin:1234`
- Ausência de limitação de tentativas de login
- Algoritmos criptográficos legados habilitados
- Telnet habilitado
- Ausência de controle de acesso via ACL

---

## 💣 Fase de Ataque — Red Team

Atividades realizadas:

- Configuração de rede no Kali Linux
- Validação de conectividade com o alvo
- Downgrade criptográfico para compatibilidade com SSH legado
- Criação de wordlist
- Ataque de força bruta utilizando Hydra

**Resultado:**

Foi obtido acesso administrativo completo ao dispositivo em poucos segundos.

---

## 🛡️ Fase de Defesa — Blue Team

Foram implementados os seguintes controles de segurança:

- Configuração de senha forte com `secret`
- Controle de acesso via ACL
- Desativação do Telnet
- Uso exclusivo de SSH
- Limitação de tentativas de login com Quiet Mode

---

## 🧪 Validação

Após a aplicação das mitigações:

- O ataque com Hydra foi bloqueado
- O acesso SSH ficou restrito a origens autorizadas
- O dispositivo permaneceu disponível para validação de conectividade via ICMP

---

## 📸 Evidências

Todas as capturas de tela do laboratório estão disponíveis na pasta `images/`.

---

## 🧠 Principais Aprendizados

- Credenciais fracas podem comprometer dispositivos de rede em poucos segundos
- Defense in Depth é essencial para reduzir riscos em ambientes corporativos
- Limitação de tentativas de login é uma medida crítica contra ataques de força bruta
- Telnet deve ser desabilitado em ambientes seguros
- ACLs ajudam a restringir o acesso administrativo a dispositivos de rede

---

## ⚠️ Aviso Legal

Este projeto foi conduzido em um ambiente de laboratório controlado, exclusivamente para fins educacionais e profissionais.
