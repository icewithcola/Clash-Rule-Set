# About this Repo
This repo holds my personal rule sets for clash. The format works with most clash variants.

# Rule Files
| File Name | Behavior | Notes |
|---|---|---|
| `adskip.yaml` | domain | Ad-related domains that keep retrying. Skip-reject them to save power. |
| `ai.yaml` | domain | AI services such as Gemini, OpenAI, Claude. |
| `bilibili.yaml` | domain | Bilibili main domains. |
| `cnip6.yaml` | ipcidr | China IPv6 ranges. |
| `cnSites.yaml` | domain | China sites. Auto-generated daily from v2fly domain list. |
| `doProxy.yaml` | domain | Sites that need a proxy. Should be loaded before other rules. |
| `download.yaml` | domain | Big download hosts, used for AOSP sync. |
| `email.yaml` | classical | Common SMTP/IMAP ports. |
| `feishu.yaml` | domain | Feishu / Lark domains. |
| `microsoft.yaml` | domain | Microsoft services. |
| `overseasCommunicate.yaml` | domain | Overseas chat apps such as Discord. |
| `overseasGame.yaml` | domain | Overseas game services such as Epic. |
| `overseasVideo.yaml` | domain | Overseas video sites such as YouTube. |
| `scholar.yaml` | domain | Academic sites such as IEEE, ACM, Springer. |
| `tailscale-domain.yaml` | domain | Tailscale DERP relay hostnames. Auto-generated daily. |
| `tailscale-ip.yaml` | ipcidr | Tailscale DERP relay IPs. Auto-generated daily. |
| `telegram.yaml` | ipcidr | Telegram IP ranges. |

# Links
Use this URL pattern, replace `<file>` with the file name above:
```
https://raw.githubusercontent.com/icewithcola/Clash-Rule-Set/master/<file>
```

# Auto Update
Some files are kept fresh by GitHub Actions:
- `cnSites.yaml` is built from [v2fly/domain-list-community](https://github.com/v2fly/domain-list-community). Runs daily at 01:30 Beijing time. Script: `scripts/generate_cn_sites.py`.
- `tailscale-domain.yaml` and `tailscale-ip.yaml` are built from the Tailscale DERP map. Runs daily at 00:00 UTC. Script: `scripts/generate_derp.py`.

You can also run the workflows by hand from the Actions tab.

# Any Problem?
Issues and pull requests are welcome. New rules and changes to current rules are welcome too. I do not want to redo work that other lists already cover well.

## Data Sources
- `telegram.yaml`: [Telegram official CIDR list](https://core.telegram.org/resources/cidr.txt). `95.161.64.0/20` is also added because Telegram uses it but does not list it.
- `feishu.yaml`: [Feishu help page (Chinese)](https://www.feishu.cn/hc/zh-CN/articles/360044683233)
- `email.yaml`: [Cloudflare: SMTP ports](https://www.cloudflare.com/zh-cn/learning/email-security/smtp-port-25-587/)
- `cnip6.yaml`: [blackmatrix7/ios_rule_script ChinaMax list](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Surge/ChinaMax/README.md)
- `cnSites.yaml`: [v2fly/domain-list-community](https://github.com/v2fly/domain-list-community), filtered to `domain:` rules only and skipping the `@!cn` tag.
- `tailscale-*.yaml`: [Tailscale DERP map](https://controlplane.tailscale.com/derpmap/default).
- `adskip.yaml`: a small hand-picked list of ad domains that keep reconnecting.
