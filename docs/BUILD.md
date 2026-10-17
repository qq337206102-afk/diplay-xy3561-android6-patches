# 应用补丁与构建

此处是源码补丁，不是可刷固件。保留上游全部许可证和第三方声明。

## 1. 获取固定基线

在新目录中执行，避免覆盖已有工程：

```powershell
git clone https://github.com/shihabal3amri/DiPlay.git DiPlay-xy3561
Set-Location DiPlay-xy3561
git checkout --detach c30d3f0df18dd132739d864a9e054c73b3d57d8c
git switch -c xy3561-api23
git apply --check ../diplay-xy3561-android6-patches/patches/0001-xy3561-api23-compat.patch
git apply ../diplay-xy3561-android6-patches/patches/0001-xy3561-api23-compat.patch
```

相邻目录名请与实际下载目录一致。不要直接对最新上游强行套用。

## 2. 开发环境

使用上游 Gradle wrapper 和其 Java toolchain 配置，配置 `ANDROID_HOME`。原验证环境使用 Android SDK 37、build-tools 36.0.0、NDK 28.2.13676358；Gradle daemon 使用项目配置的 JDK 25。机器需具备下载依赖及工具链的条件。以固定基线及补丁内配置为准。

```powershell
.\gradlew.bat :shared:testDebugUnitTest :common:testDebugUnitTest :home:testDebugUnitTest :mobile:lintDebug :home:lintDebug :maphost:lintDebug :mobile:assembleDebug :home:assembleDebug :maphost:assembleDebug --max-workers=2 --continue --console=plain
```

普通源码构建不导入认证材料，不能据此宣称已验证 iPhone 配对。需要认证输入的 standalone 构建另受上游 `docs/BUILD.md` 的显式本地输入检查约束；本仓库不提供这些输入。不要用伪造或随意生成的密钥冒充运行身份。

自行构建的签名与先前实测 APK 可能不同，不能保证覆盖安装。卸载会清除设置和配对状态，操作前自行备份。仓库没有生产签名密钥或正式 APK 发布流程。

## 3. 本地审查

在补丁仓库运行 `python tools/check_public.py`，检查文件清单、哈希和常见敏感材料标记。这是辅助检查，不是完整安全或法律审计。

验证结论见 VALIDATION.md。重新构建的二进制必须重新测试，不能自动继承原实测 APK 的结论。请勿刷机或改 MCU；本适配不需要系统升级。
