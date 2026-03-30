# 🟣 MAC Flooding Attack & Mitigation (Port Security)

## 📌 Overview
This lab demonstrates a Layer 2 attack (MAC Flooding) and its mitigation using Port Security on a switch.

## 🧪 Environment
- GNS3
- Cisco IOSvL2
- Kali Linux
- VPCS

## ⚔️ Attack
The attack was performed using:

```bash
macof -i eth1

This floods the switch MAC table with fake addresses.

🚨 Impact
High CPU usage
Switch instability
Network degradation

🛡️ Mitigation
interface gi0/1
switchport mode access
switchport port-security
switchport port-security maximum 2
switchport port-security violation shutdown
switchport port-security mac-address sticky
✅ Result

The switch detected the attack and shut down the interface (secure-shutdown).
