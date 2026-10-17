# 应用补丁与构建

此处是源码补丁，不是可刷固件。保留上游全部许可证和第三方声明。

## 1. 获取固定基线

需要 Git 和 Python 3.10 或以上。在一个没有同名项目子目录的新工作目录中执行，避免覆盖已有工程：

```powershell
git -c core.autocrlf=false clone https://github.com/qq337206102-afk/diplay-xy3561-android6-patches.git
Set-Location diplay-xy3561-android6-patches
git checkout --detach xy3561-api23-v3-source.1
python tools/check_public.py
python -m unittest discover -s tools -p 'test_*.py' -v
python tools/verify_patch.py
Set-Location ..
git clone https://github.com/shihabal3amri/DiPlay.git DiPlay-xy3561
Set-Location DiPlay-xy3561
git checkout --detach c30d3f0df18dd132739d864a9e054c73b3d57d8c
git switch -c xy3561-api23
git apply --check ../diplay-xy3561-android6-patches/patches/0001-xy3561-api23-compat.patch
git apply ../diplay-xy3561-android6-patches/patches/0001-xy3561-api23-compat.patch
```

两个仓库必须是相邻目录。`verify_patch.py` 需要联网获取固定上游，在临时目录应用补丁并检查 47 个源文件哈希，结束后清理临时目录；不编译、不运行上游应用。不要直接对最新上游强行套用。

Linux/macOS 使用 `cd` 代替 `Set-Location`，构建时使用 `./gradlew`。下载补丁仓库时保留 `core.autocrlf=false`，否则 Windows 换行转换可能导致原始补丁 SHA256 校验失败。

## 2. 开发环境

使用上游 Gradle wrapper 和其 Java toolchain 配置，配置 `ANDROID_HOME`。原验证环境使用 Android SDK 37、build-tools 36.0.0、NDK 28.2.13676358；Gradle daemon 使用项目配置的 JDK 25。机器需具备下载依赖及工具链的条件。以固定基线及补丁内配置为准。

```powershell
.\gradlew.bat :shared:testDebugUnitTest :common:testDebugUnitTest :home:testDebugUnitTest :mobile:lintDebug :home:lintDebug :maphost:lintDebug :mobile:assembleDebug :home:assembleDebug :maphost:assembleDebug --max-workers=2 --continue --console=plain
```

普通源码构建不导入认证材料，不能据此宣称已验证 iPhone 配对。需要认证输入的 standalone 构建另受上游 `docs/BUILD.md` 的显式本地输入检查约束；本仓库不提供这些输入。不要用伪造或随意生成的密钥冒充运行身份。

自行构建的签名与先前实测 APK 可能不同，不能保证覆盖安装。卸载会清除设置和配对状态，操作前自行备份。仓库没有生产签名密钥或正式 APK 发布流程。

## 3. 本地审查

在补丁仓库运行 `python tools/check_public.py`，检查文件清单、哈希和常见敏感材料标记。还可运行 `python -O tools/check_public.py`，关键检查不会被优化模式跳过。辅助扫描不是完整安全或法律审计。

已有本地上游工程时，可以运行 `python tools/verify_patch.py --upstream ../DiPlay-xy3561`，它只读取该仓库对象，使用独立索引和临时工作区，不重置或切换原工程。CI 自动做检查器回归、公开材料扫描、固定基线上补丁应用和逐文件哈希验证；**不代表 Android 完整构建或实车测试通过**。

验证结论见 VALIDATION.md。重新构建的二进制必须重新测试，不能自动继承原实测 APK 的结论。请勿刷机或改 MCU；本适配不需要系统升级。
