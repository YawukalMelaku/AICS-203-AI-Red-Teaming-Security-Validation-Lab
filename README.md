# ICDFA AICS-203 - Red Teaming and Security Validation of AI

**One-month intensive practical course | Four modules | Ubuntu Server plus Linux workstation**

## Begin here

1. Open `ICDFA_AICS203_Student_Training_Manual.pdf` and follow the installation and safety instructions.
2. Set up an isolated Ubuntu Server virtual machine and a separate Linux workstation.
3. On the server, install OpenSSH and Python 3. Copy this package to `~/AICS203_Lab/`.
4. Connect using SSH from the Linux workstation. Run the **local-only** simulated AI service on the server.
5. Forward server port 8765 over SSH to port 8765 on the workstation. Do not open port 8765 in the server firewall.
6. Run `python3 client/run_cases.py --mode baseline`, followed by the hardened suite.
7. Follow the four module exercises and complete the attached assessment brief.

## Server-side quick start

```bash
sudo apt update
sudo apt install -y openssh-server python3 unzip
sudo systemctl enable --now ssh
mkdir -p ~/AICS203_Lab
# Copy the ZIP to the Ubuntu Server via scp and extract inside ~/AICS203_Lab
cd ~/AICS203_Lab
python3 server/test_engine.py
python3 server/app.py
```

## Linux workstation quick start

```bash
# Replace 192.168.56.20 with your private Ubuntu Server IP
ssh -N -L 8765:127.0.0.1:8765 student@192.168.56.20
# In another local terminal, from your unpacked copy of the same package:
python3 client/run_cases.py --mode baseline
python3 client/run_cases.py --mode hardened
```

You can check access in a separate terminal using `curl http://127.0.0.1:8765/health`.

**Security requirement:** The Python simulation binds only to 127.0.0.1 on the Ubuntu Server. The SSH tunnel transports communication securely. Do not change the binding to 0.0.0.0, do not forward the laboratory port publicly, and do not test real third-party AI systems.

## Course layout

- **Module 1:** Lab topology, Ubuntu Server deployment, SSH access, scope and baselining.
- **Module 2:** Simulated indirect prompt injection and retrieval trust boundaries.
- **Module 3:** Synthetic data disclosure, tool privileges and output encoding.
- **Module 4:** Secure controls, negative tests, retesting, severity and reporting.

## What this package is, and is not

It is an educational, deterministic **simulation of AI-integrated application workflows**. It does not contain a real LLM, model weights or access to live APIs. Its purpose is to demonstrate red-team methodology, evidence-based validation, defensive engineering and SSH-based Linux administration. Optional external toolkits such as PyRIT and garak are **reading resources**, not a requirement for the core lab.

The `student-demo` and `instructor-demo` tokens are deliberately hard-coded teaching values. They are **not real authentication credentials** and must never be treated as a secure authentication mechanism.

## Submission

Use the E-Campus Practical Laboratories assessment. Submit the final PDF report and a private or authorised GitHub repository with executed evidence, excluding any real sensitive information.
