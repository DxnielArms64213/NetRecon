# Date:** 2026-09-25

## Worked On

### Host Discovery — `scanner/discovery.py`

Started building the host discovery module for NetRecon.

The purpose of this module is to take a collection of individual IP addresses and determine which hosts are reachable using ICMP ping.

The module currently contains two main functions:

* `ping_host(ip)` — checks whether an individual host responds to a ping.
* `discover_hosts(targets)` — iterates through multiple IP addresses and returns the hosts that responded.

---

## What I Learned

### `subprocess.run()`

Used Python's `subprocess` module to execute the Windows `ping` command from Python.

```python
subprocess.run(["ping", "-n", "1", "-w", "1000", str(ip)])
```

Learned that:

* `-n 1` tells Windows ping to send one ICMP request.
* `-w 1000` sets the timeout to 1000 milliseconds (1 second).
* `str(ip)` converts an `IPv4Address` or `IPv6Address` object into the string representation required by the external command.
* `subprocess.run()` returns a result object containing information about the command execution.

### Return Codes

Used:

```python
result.returncode
```

A return code of `0` indicates that the ping command completed successfully, allowing `ping_host()` to return `True`.

A non-zero return code causes it to return `False`.

### Iterating Through Targets

Learned that `discover_hosts()` should receive an iterable of **individual IP addresses**, rather than handling networks or ranges itself.

This keeps the modules separated:

```text
Target input
    ↓
target.py
    ↓
expand_target()
    ↓
Individual IP addresses
    ↓
discovery.py
    ↓
discover_hosts()
    ↓
Alive hosts
```

### Why `return` Belongs Outside the Loop

`discover_hosts()` builds the `alive_hosts` list while checking every target.

The `return alive_hosts` statement therefore belongs **after the loop**.

Putting it inside the loop would cause the function to stop after checking the first host.

### Timeout Design

A scanner cannot wait several seconds for every inactive host, particularly when scanning larger networks.

A 1000 ms timeout gives each host a reasonable opportunity to respond while allowing the scanner to move on quickly.

---

## What I Implemented

### `ping_host()`

Created the initial host-pinging functionality using Windows `ping`.

```python
def ping_host(ip):
    result = subprocess.run(["ping", "-n", "1", "-w", "1000", str(ip)])
    if result.returncode == 0:
        ping = True
        return ping
    else:
        ping = False
        return ping
```

### `discover_hosts()`

Created the multi-host discovery function.

```python
def discover_hosts(targets):
    alive_hosts = []
    for ip in targets:
        ping = ping_host(ip)
        if ping:
            alive_hosts.append(ip)
    return alive_hosts
```

The function stores the actual IP address in `alive_hosts`, rather than storing the Boolean result of the ping.

### Git

Created and committed the new discovery module.

Commit:

```text
2ab392c — Add host discovery module
```

The commit was successfully created locally.

The initial `git push` was rejected because the GitHub repository contained changes that were not present locally.

The planned resolution is:

```text
git fetch origin
git rebase origin/main
git push
```

This will integrate the remote changes without force-pushing.

---

## Problems / Bugs

### Remote Repository Ahead

The first push of the discovery commit was rejected:

```text
! [rejected] main -> main (fetch first)
```

The local commit is safe and has already been created.

The repository needs to be synchronised with the remote using a fetch and rebase before pushing again.

### Temporary Test Code Removed

A temporary test:

```python
print(ping_host("192.168.50.10"))
```

was removed before committing the module.

This prevents `discovery.py` from automatically executing a ping whenever the module is imported.

### Output Suppression Not Yet Implemented

The current `ping_host()` still allows the Windows ping output to appear in the terminal.

`capture_output=True` was identified as the next improvement so that NetRecon can process the result internally without filling the terminal with raw ping output.

---

## Next Session

* Finish cleaning up `discovery.py`.
* Suppress raw ping output with `capture_output=True`.
* Review the discovery logic.
* Connect `target.py` and `discovery.py` through the future `main.py` orchestration layer.
* Perform a complete discovery test using:

  * Single IP
  * Small CIDR network
  * IP range
  * Hosts that respond
  * Hosts that do not respond
* Synchronise and push the Day 3 work to GitHub.
* Begin planning the `scanner/ports.py` module once host discovery is complete.
