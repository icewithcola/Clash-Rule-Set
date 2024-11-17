# About this Repo
This repo is for my personal rules in clash, supporting most variants.\

# Types
|File Name|Behavior|
|---|---|
|`adskip.yaml`|domain|
|`ai.yaml`|domain|
|`bilibili.yaml`|domain|
|`cnip6.yaml`|ipcidr|
|`download.yaml`|domain|
|`email.yaml`|classical|
|`feishu.yaml`|domain|
|`microsoft.yaml`|domain|
|`overseasCommunicate.yaml`|domain|
|`overseasGame.yaml`|domain|
|`overseasVideo.yaml`|domain|
|`scholar.yaml`|domain|
|`telegram.yaml`|ipcidr|
# Links
`https://raw.githubusercontent.com/icewithcola/Clash-Rule-Set/master/file`

# Any problem?
Issues are welcome, new rules/ changes on rules are welcome. But I do not want to do what others already have done.

## Data Sources
- telegram.yaml: [Telegram official(IP-CIDRs)](https://core.telegram.org/resources/cidr.txt), `95.161.64.0/20` is used by telegram but not in the official document.
- feishu.yaml: [Link (Chinese)](https://www.feishu.cn/hc/zh-CN/articles/360044683233-%E9%85%8D%E7%BD%AE%E4%BC%81%E4%B8%9A%E5%86%85%E7%BD%91%E9%98%B2%E7%81%AB%E5%A2%99%E5%9F%9F%E5%90%8D%E5%92%8C%E7%99%BD%E5%90%8D%E5%8D%95#tabs0|lineguid-EwRIB)
- email.yaml: [Cloudflare Help](https://www.cloudflare.com/zh-cn/learning/email-security/smtp-port-25-587/)
- cnip6.yaml: [blackmatrix7/ios_rule_script: 国内网站/IP合集](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Surge/ChinaMax/README.md)
- adskip.yaml: Some ad domains, but always connect even un-connectable. Skip reject them for saving power.