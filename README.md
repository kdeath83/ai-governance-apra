# AI Governance Accelerator for APRA Regulated Entities (AREs)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![APRA Aligned](https://img.shields.io/badge/APRA-2025%20AI%20Letter-blue)](https://www.apra.gov.au/ai-letter)

**Cost-Optimized AI Security Governance for Australian Financial Institutions**

> **Target Cost:** <$50/month | **vs Enterprise Solutions:** $5,000+/month

This repository provides a prototype "near-zero" cost architecture for AI governance that meets APRA prudential expectations without the enterprise price tag.

---

## 🎯 What Problem This Solves

APRA's April 2025 AI letter requires regulated entities to:

- ✅ **Board AI literacy and oversight** — sufficient understanding to provide governance
- ✅ **Effective AI risk management** — strategy aligned with risk appetite  
- ✅ **Independent validation** — not relying on vendor assurances
- ✅ **Operational resilience** — defined triggers, monitoring, recovery plans
- ✅ **Comprehensive audit trails** — 7-year retention of AI decisions

**This architecture delivers all five at <$50/month.**

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     GOVERNANCE LAYER (Manual)                    │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────────┐  │
│  │ GitHub Issues   │  │ Markdown Docs   │  │ Board Reporting  │  │
│  │ (Approvals)     │  │ (Policy)        │  │ (Quarterly)      │  │
│  └─────────────────┘  └─────────────────┘  └──────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│                     SECURITY LAYER (AWS)                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────────┐  │
│  │ IAM (SCPs)      │  │ KMS (CMK)       │  │ CloudTrail       │  │
│  │ Least Privilege │  │ Encryption      │  │ (Audit Trail)    │  │
│  └─────────────────┘  └─────────────────┘  └──────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│                     AI RUNTIME (Self-Hosted)                   │
│  ┌─────────────────┐  ┌─────────────────┐                        │
│  │ EC2 Spot        │  │ TinyLlama 1.1B  │  Hardened Container  │
│  │ (g6g.xlarge)    │  │ (Quantized)     │  $10-20/month        │
│  │ Auto-shutdown   │  │ Fast/Cheap      │                        │
│  └─────────────────┘  └─────────────────┘                        │
├─────────────────────────────────────────────────────────────────┤
│                     AUDIT LAYER (S3 + Glacier)                   │
│  ┌─────────────────┐  ┌─────────────────┐                        │
│  │ Inference Logs  │  │ 7-Year Retention│  APRA Requirement    │
│  │ Compressed      │  │ Glacier Deep    │  $0.50/month         │
│  └─────────────────┘  └─────────────────┘                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📋 Quick Start

### 1. Assess Your Current State

```bash
python survey.py
```

Answer 12 questions about your AI governance posture. Generates:
- Maturity score (0-100)
- Recommended components
- Customized deployment roadmap

### 2. Generate Deployment Guide

```bash
python generate-deployment-guide.py
```

Creates `DEPLOYMENT-GUIDE.md` with only the components you need.

### 3. Deploy Infrastructure

```bash
# Deploy core AI inference engine
./deploy-hardened.sh

# Configure audit logging lifecycle
./apply-lifecycle.sh
```

### 4. Run Security Scan

```bash
./scan.sh myapp.py
# Results: myapp.py.security-results.json
```

---

## 📁 Repository Structure

| File | Purpose | Cost | APRA Alignment |
|------|---------|------|----------------|
| `survey.py` | Interactive maturity assessment | $0 | Board literacy, risk appetite |
| `decision-matrix.json` | Maps gaps to components | $0 | Structured decision-making |
| `deploy-hardened.sh` | Hardened EC2 Spot deployment | ~$10-20/mo | Independent validation |
| `inference-logger.py` | Secure Lambda with validation | ~$5/mo | 7-year audit trail |
| `weekly-rollup.py` | Parallel log aggregation | ~$2/mo | Cost-optimized retention |
| `s3-lifecycle.json` | Glacier transition rules | $0 | Long-term retention |
| `apply-lifecycle.sh` | Lifecycle configuration | $0 | Automated compliance |
| `.github/workflows/ai-security-scan-hardened.yml` | Rate-limited CI/CD | $0 | Automated validation |

---

## 🔒 Security Hardening

This is **not** a toy architecture. Production-grade security:

| Control | Implementation |
|---------|---------------|
| **Container Escape Prevention** | Read-only rootfs, no-new-privileges, capability dropping |
| **Spot Interruption Handling** | Graceful shutdown with checkpoint saving |
| **Input Validation** | Path traversal prevention, size limits (100KB) |
| **Network Isolation** | Security group allows localhost only (SSH tunnel required) |
| **Credential Verification** | AWS identity validation at module load |
| **Connection Pooling** | 25 S3 connections, 10 concurrent uploads |
| **Partial Failure Handling** | Dead letter queue for failed records |
| **Rate Limiting** | 15-min CI/CD timeouts, path filtering |

---

## 💰 Cost Breakdown

| Component | Monthly Cost | Notes |
|-----------|--------------|-------|
| **EC2 Spot** (g6g.xlarge, 20 hrs/week) | ~$10-20 | Self-hosted TinyLlama |
| **S3 Standard** (1GB logs) | ~$0.02 | Before lifecycle transition |
| **S3 Glacier IR** (long-term) | ~$0.50 | 7-year retention |
| **Lambda** (1M requests) | ~$2 | Within free tier |
| **KMS** (1 customer key) | ~$1 | APRA-compliant encryption |
| **CloudTrail** (1 trail) | $0 | First trail free |
| **Data Transfer** | ~$5 | Outbound only |
| **TOTAL** | **~$15-30/month** | |

**vs Enterprise Solutions:** $5,000-20,000/month

---

## 📊 APRA Alignment Matrix

| APRA Requirement (April 2025 Letter) | Implementation | Evidence |
|--------------------------------------|----------------|----------|
| **Board AI literacy** | Survey → Maturity scoring + documentation | `survey.py`, governance templates |
| **Effective risk management** | Security scanning, validation workflows | `ai-security-scan-hardened.yml` |
| **Independent validation** | Open-source scanners (Garak, Semgrep) + red team | Scan results, issues logged |
| **Operational resilience** | Spot handling, graceful shutdown, fallbacks | `deploy-hardened.sh` |
| **Comprehensive audit trails** | S3 + Glacier, 7-year retention, inference logging | `inference-logger.py`, `s3-lifecycle.json` |

---

## 🎓 Well-Architected Survey

The `survey.py` script implements a **Well-Architected Framework** specifically for APRA AI governance:

### Four Pillars Assessed

1. **Governance & Strategy** (3 questions)
   - Board AI literacy
   - Documented AI strategy
   - Risk appetite definitions

2. **Risk Management** (3 questions)
   - Model inventory completeness
   - Validation processes
   - Post-deployment monitoring

3. **Audit & Compliance** (2 questions)
   - Inference logging maturity
   - CPS 234 alignment

4. **Deployment Preferences** (2 questions)
   - Cost tolerance
   - Automation vs manual balance

### Maturity Scoring

- **0-33: Basic** — Significant gaps, immediate action required
- **34-66: Developing** — Some controls, standardization needed
- **67-100: Advanced** — Mature governance, optimization focus

---

## 🚀 Deployment Scenarios

### Scenario A: Startup (Near Zero Budget)

**Maturity:** Basic  
**Budget:** <$50/month  
**Deploy:**
- `survey.py` → establish baseline
- `deploy-hardened.sh` → core inference
- `ai-security-scan-hardened.yml` → CI validation
- Manual governance via GitHub Issues

**Timeline:** 1-2 weeks to production

### Scenario B: Mid-Size Bank (Low Budget)

**Maturity:** Developing  
**Budget:** $100-300/month  
**Deploy:**
- All Scenario A components
- `inference-logger.py` → audit trail
- `s3-lifecycle.json` → compliance retention
- `weekly-rollup.py` → cost optimization

**Timeline:** 3-4 weeks with security review

### Scenario C: Major Bank (Full Compliance)

**Maturity:** Advanced  
**Budget:** $500-1,000/month  
**Deploy:**
- All components
- Upgrade to SageMaker Serverless (always-on)
- Add QuickSight dashboards (Board reporting)
- External red team validation (quarterly)

**Timeline:** 6-8 weeks with APRA engagement

---

## ⚠️ Honest Assessment

### What This IS
- ✅ **Phase 1** governance solution for cost-conscious organizations
- ✅ Suitable for **pilot programs** and **low-volume AI use cases**
- ✅ Demonstrates **governance intent** to APRA
- ✅ Foundation for scaling to enterprise solutions

### What This Is NOT
- ❌ Suitable for **high-frequency production** without scaling
- ❌ Substitute for **annual external validation** (still required for APRA attestation)
- ❌ Turnkey solution requiring zero maintenance

---

## 🤝 Contributing

This is an **open-source reference architecture** for the Australian financial services community.

**Ways to contribute:**
- Report APRA alignment gaps
- Share cost optimizations
- Add CI/CD templates for other languages
- Improve documentation

**Not accepting:** Proprietary vendor integrations (keep it vendor-neutral).

---

## 📄 License

MIT License — For APRA-regulated Australian financial institutions and global FSI community.

---

## 🙏 Acknowledgments

- **APRA** for clear 2026 AI governance expectations
- **AWS** for cost-optimized infrastructure primitives
- **Open-source community** (Garak, Semgrep, vLLM, TinyLlama)

---

## 📞 Support

- **Issues:** https://github.com/kdeath83/ai-governance-apra/issues
- **Discussions:** GitHub Discussions tab
- **APRA Reference:** https://www.apra.gov.au/ai-letter

---

**Built with ❤️ for Australian AREs.**

*"Governance doesn't have to be complicated and cost the earth."*
