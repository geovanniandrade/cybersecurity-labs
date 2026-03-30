# 🚨 Incident Response Lab: MAC Flooding Attack (Port Security)

## 🎯 Objective
Simulate, detect, and mitigate a MAC Flooding attack in a controlled environment, replicating a real-world Layer 2 security incident from a SOC (Security Operations Center) perspective.

---

## 🧠 Scenario

During normal network operations, users began experiencing:

- Intermittent connectivity issues  
- High latency  
- Inconsistent access to internal systems  

This behavior indicated a potential network anomaly, possibly related to a Layer 2 attack or switch misconfiguration.

---

## 🚨 Detection

The issue was identified through abnormal network behavior:

- Sudden degradation in network performance  
- Increase in broadcast traffic  
- Switch behaving similarly to a hub  

### Indicators of Compromise (IoCs):

- Excessive MAC address entries  
- Rapid CAM table changes  
- Unknown MAC address flooding  

---

## 🔍 Investigation

To validate the hypothesis, a controlled lab environment was used.

### 🧪 Attack Simulation

- Tool: `macof` (Kali Linux)  
- Objective: Overflow the switch CAM table with fake MAC addresses  

```bash
macof -i eth0
```

🔎 Observed Behavior:

CAM table overflow
Legitimate MAC addresses removed
Switch started broadcasting traffic to all ports

This confirmed the presence of a MAC Flooding attack.

⏱️ Incident Timeline

Users reported network instability
Abnormal broadcast behavior identified
Hypothesis: Layer 2 attack
Attack reproduced in lab environment
MAC Flooding confirmed
Port Security implemented
Network stabilized

💥 Impact
The attack caused:

Network instability
Loss of segmentation
Increased broadcast traffic
Potential exposure to packet sniffing
Real-World Risks:
Credential interception
Data leakage
Unauthorized lateral movement

🛡️ Mitigation (Response)

To contain the attack, Port Security was implemented on the switch.

🔐 Security Controls Applied:

Limit number of MAC addresses per port
Restrict unauthorized devices
Define violation actions (shutdown / restrict)
Example Configuration:
switchport port-security
switchport port-security maximum 2
switchport port-security violation shutdown

📸 Evidence
- attack.png  
- switch.png  
- mitigation.png
