# Nmap Service Version Detection — Mini CTF

**CAPEC-309 | Network Topology Mapping**
**Author:** Gabriel Ruegner

A small Docker lab to practice the most common technique in network reconnaissance: using Nmap to identify services running on a target and grab their version information. The flag is hidden in plain sight — but you have to know how to ask Nmap to show it to you.

**Time to complete:** ~10 minutes
**Tools used:** Nmap

---

## Setup

You'll need [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

Download and unpack the `nmap-mini-lab` folder, then open PowerShell (or your terminal) and:

```
cd nmap-mini-lab
docker compose up -d --build
```

This builds and starts two containers:
- **target** (10.20.30.10) — the machine you're scanning
- **attacker** (10.20.30.20) — your scanning box, comes with Nmap pre-installed

Verify both are running:

```
docker compose ps
```

Now shell into the attacker box:

```
docker exec -it ctf-attacker sh
```

---

## The Challenge

You're a penetration tester. You have one target on the network at `10.20.30.10`. Your job is to identify what's running on it and find the flag.

The flag format is: `FLAG{...}`

### Hints

1. A basic Nmap scan tells you which ports are open. A *better* scan tells you what software is running on each port — and what version.
2. Service banners often leak more information than developers realize. Pay close attention to version strings.
3. How do you find the service Version again?

---

## Key Lesson

This is the difference between a basic port scan and a real reconnaissance scan. Anyone can find open ports — that's table stakes. The real intelligence comes from `-sV`, which tells you exactly what software (and which version) is running on each port. In a real engagement, that version info gets cross-referenced against CVE databases to find known exploits.

For defenders, this is why service banners should be customized or stripped wherever possible. The default banners that ship with FTP/SSH/HTTP daemons broadcast your software version to anyone who connects — including attackers doing exactly what you just did.

---

## Cleanup

When you're done, exit the attacker container (`exit`) and tear it all down:

```
docker compose down --rmi all
```
