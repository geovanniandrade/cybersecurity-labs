# 🔐 SSH Brute Force Attack & Defense in Depth (Cisco IOS)

This project demonstrates a practical cybersecurity lab simulating an SSH brute force attack against a Cisco IOS router and the implementation of defensive controls using Defense in Depth.

---

## 🎯 Objective

To demonstrate how weak credentials and insecure configurations can lead to full device compromise, and how proper security controls can mitigate these risks.

---

## 🧱 Lab Environment

- GNS3
- Cisco IOS Router
- Kali Linux (Attacker)
- Layer 2 Switch

**Network:**
- Attacker: 192.168.1.100
- Target: 192.168.1.1

---

## ⚠️ Identified Vulnerabilities

- Weak credentials (admin:1234)
- No login attempt limitation
- Legacy cryptographic algorithms enabled
- Telnet enabled
- No access control (ACL)

---

## 💣 Attack Phase (Red Team)

- Network configuration (Kali)
- Connectivity validation
- SSH cryptographic downgrade
- Wordlist creation
- Hydra brute force attack

👉 Result:
Full administrative access gained in seconds.

---

## 🛡️ Defense Phase (Blue Team)

Implemented security controls:

- Strong password (secret)
- Access control via ACL
- Telnet disabled
- SSH only
- Login rate limiting (Quiet Mode)

---

## 🧪 Validation

After mitigation:

- Hydra attack blocked
- SSH access restricted
- Device remained available (ICMP)

---

## 📸 Evidence

All lab screenshots are available in the `images/` folder.

---

## 📄 Full Report

- [DOCX Version](./report/Relatorio_Tecnico_SSH_BruteForce_Geovanni_final.docx)
- [PDF Version](./report/Relatorio_Tecnico_SSH_BruteForce_Geovanni_final.pdf)

---

## 🧠 Key Takeaways

- Weak credentials can compromise devices in seconds
- Defense in Depth is essential
- Rate limiting is critical against brute force attacks

---

## ⚠️ Disclaimer

This project was conducted in a controlled lab environment for educational purposes only.
