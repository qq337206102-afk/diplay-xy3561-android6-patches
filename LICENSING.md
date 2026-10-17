# 许可证与来源

本适配以 [DiPlay](https://github.com/shihabal3amri/DiPlay) 固定提交为基础；其接收器源自 [xcertplay](https://github.com/shilapi/xcertplay)。作者与上游保留原有权利。本项目不是 Apple、XY AUTO 或上游作者的官方产品。

不要把所有补丁简单视为同一许可证：

- 原工程主要代码采用 GPL-3.0，全文见 LICENSE；没有其他声明的新增兼容辅助代码按 GPL-3.0-only 发布。
- `common/src/main/java/com/shilapi/xcertplay/DiPlayActivity.kt` 保留 `AGPL-3.0-only` 声明，源自 DiAuto 的界面语言/实现；本补丁对该文件的修改沿用该声明。全文见 LICENSES/AGPL-3.0.txt；[DiAuto](https://github.com/shihabal3amri/DiAuto)。
- 原文件已有的许可、版权、第三方声明继续适用。应用补丁后必须保留上游 `docs/THIRD_PARTY_NOTICES.md` 及关联许可证，不能以本摘要取代。

本仓库不复制上游图标、品牌素材、APK、原生库、认证材料或第三方依赖二进制；不授予 Apple 标识或任何认证身份的使用权。上游实验性认证材料未被重新许可为项目源码，其一般再分发权利尚未解决，故排除在外。

适配新增依赖（由 Gradle 获取，不在本仓库打包）：

| 依赖 | 许可来源 |
| --- | --- |
| org.conscrypt:conscrypt-android:2.7.0 | [Conscrypt](https://github.com/google/conscrypt)，Apache-2.0；参考全文 LICENSES/Apache-2.0.txt |
| net.sourceforge.streamsupport:android-retrofuture:1.7.4 | [android-retrofuture](https://github.com/retrostreams/android-retrofuture)，POM 声明 GPL-2.0 + Classpath Exception；部分 JSR166 派生代码为 CC0-1.0，须保留其原许可声明 |

本仓库仅提供技术整理，不作法律合规保证。若要发布完整 APK，请先核清认证输入、全部素材和依赖的再分发条件，并准备相应源码及许可说明；当前没有这种发布产物。
