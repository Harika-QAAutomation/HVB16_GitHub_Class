
# Correct way to start SSH agent on Windows (PowerShell / CMD)
---

## CMD

```
ssh-keygen -t ed25519 -C "your.email@company.com"
# SSH folder created in the respective path
```

<img width="925" height="359" alt="image" src="https://github.com/user-attachments/assets/14ca7179-1411-4aaf-b2c9-253c0b48b32d" />

---
## Powershell

```

Get-Service ssh-agent | Set-Service -StartupType Automatic
Start-Service ssh-agent
ssh-add C:\Users\Saz130user\SSH\test 

```

<img width="655" height="148" alt="image" src="https://github.com/user-attachments/assets/71fee62b-ff6e-441f-89cc-41ab0c04f76b" />

---

```
type C:\Users\Saz130user\SSH\test.pub
```

<img width="829" height="45" alt="image" src="https://github.com/user-attachments/assets/e641ec66-b062-4e2c-a9fc-0a71ffadddf8" />

---


<img width="1239" height="650" alt="image" src="https://github.com/user-attachments/assets/22b031c3-663b-49ea-9c85-891fc2e0544d" />

---

```
ssh -T git@github.com
```

<img width="828" height="153" alt="image" src="https://github.com/user-attachments/assets/711486f1-3036-482c-bf94-f1aa13d810a2" />
---

<img width="685" height="359" alt="image" src="https://github.com/user-attachments/assets/d44e8574-d968-4506-a710-5b2ad54dcc7b" />

