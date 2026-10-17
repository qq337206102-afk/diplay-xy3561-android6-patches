# DiPlay · XY3561 Android 6 兼容补丁

[![Source patch checks](https://github.com/qq337206102-afk/diplay-xy3561-android6-patches/actions/workflows/source-checks.yml/badge.svg)](https://github.com/qq337206102-afk/diplay-xy3561-android6-patches/actions/workflows/source-checks.yml)

针对 XY AUTO MT3561 老车机的个人兼容适配，基于 [DiPlay](https://github.com/shihabal3amri/DiPlay)。不是上游官方版本，也不是车机刷机包。本仓库只发布补丁、说明和脱敏测试摘要，不分发 APK、认证材料或车机固件。

## 已确认的结果

2026-10-17，使用者反馈：第一种「车载热点」连接方式已能流畅运行，100% 分辨率、重启及行驶场景均测试正常。这是单台设备的实测反馈，不代表所有 MT3561 设备均兼容；没有采集实车 FPS/延迟基准。请停车后操作安装和设置。

| 项目 | 测试设备/版本 |
| --- | --- |
| 平台 | XY AUTO MT3561，evb3561sv_w_65_m0 |
| 系统 | 实际 Android 6.0 / API 23，不以厂商显示的版本号判断 |
| 内存/存储 | 2GB / 32GB |
| 屏幕 | 竖屏 768×1024；应用可用区域约 768×883 |
| 适配版本 | 0.2.19-xy3561-api23-v3，versionCode 44 |
| 已确认连接 | 车载热点；车机不必购买蜂窝流量套餐 |

## 做了什么

- 补齐 API 23 兼容处理、异步 API 回移和局部加密提供者兼容。
- 无线会话清理完成后再启动新会话，处理旧连接占用。
- 旧系统的 IPv4 地址选择与已有热点启动兼容。
- UDP 5353 明确出现地址占用时，由 JmDNS 回退系统 NSD；其他错误不被掩盖。
- 保留竖屏支持；不改 MCU、CAN、倒车或系统分区。

## 使用与边界

第一次使用请从 [完整下载与构建步骤](docs/BUILD.md) 开始。固定源码补丁版：`xy3561-api23-v3-source.1`；也可从 [Releases](https://github.com/qq337206102-afk/diplay-xy3561-android6-patches/releases) 获取源码快照。它不是可安装 APK。

[兼容性记录](docs/COMPATIBILITY.md) · [变更记录](CHANGELOG.md) · [提交问题](https://github.com/qq337206102-afk/diplay-xy3561-android6-patches/issues/new/choose)

先看 [构建说明](docs/BUILD.md)、[验证记录](docs/VALIDATION.md) 和 [许可证说明](LICENSING.md)。补丁只针对固定上游提交，不能直接安装到车机。

源码构建不包含运行认证材料，**不等于能独立完成 CarPlay 连接**。本仓库不提供材料提取方法、不保证第三方认证材料的使用或再分发权利。只有已取得相应授权的运行输入才应由使用者在本地接入。

上游基线：`c30d3f0df18dd132739d864a9e054c73b3d57d8c`。完整文件清单与 SHA256 见 [manifest.json](manifest.json)。本仓库不替代上游源码及其第三方声明。

## 反馈

请提供真实 API、硬件型号、补丁版本、连接方式和脱敏错误摘要。不要上传私钥、认证包、配对信息、Wi-Fi 密码、完整诊断日志、IMEI、ICCID、精确位置或未遮挡照片。当前只确认上述单台硬件，USB、Wi-Fi Direct 和其他固件不承诺同等稳定性。
