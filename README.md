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
3. The Nmap flag you need starts with `-s` and stands for "service version detection."

---

## Walkthrough (spoilers)

> Try the challenge yourself first. Come back here only if you get stuck.

### Step 1: Basic port scan

Start with a default scan to see what's open on the target:

```
nmap 10.20.30.10
```

**Expected output:**
```
PORT     STATE SERVICE
21/tcp   open  ftp
22/tcp   open  ssh
80/tcp   open  http
8080/tcp open  http-proxy
```

You can see four ports are open, but Nmap is just guessing the services based on standard port numbers. There's no flag visible yet.

### Step 2: Service version detection

The default scan doesn't tell us what software is actually running — only what *should* be running on those ports. To get version info, we need the `-sV` flag:

```
nmap -sV 10.20.30.10
```

**Expected output:**
```
PORT     STATE SERVICE      VERSION
21/tcp   open  ftp          ProFTPD 1.3.5-FLAG{nmap_service_version_detection} Server (NovaCorp FTP)
22/tcp   open  ssh          OpenSSH 8.2p1 Ubuntu 4ubuntu0.5
80/tcp   open  http         Apache httpd 2.4.41 ((Ubuntu))
8080/tcp open  http-proxy   nginx 1.18.0
```

There it is — the flag is embedded in the FTP service version banner. Nmap connected to port 21, read the banner the FTP server sent back, and parsed it as version info.

### 🚩 Flag: `FLAG{nmap_service_version_detection}`

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
