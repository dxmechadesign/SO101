# SO-101 ロボットアーム - LeRobot セットアップ（Windows）

このリポジトリは、HuggingFaceの[LeRobot](https://github.com/huggingface/lerobot)フレームワークを使用して、SO-101ロボットアームをWindows環境でセットアップするためのドキュメントとスクリプトを含んでいます。

## 概要

SO-101は、リーダーアーム（操作側）とフォロワーアーム（制御される側）の2つのアームで構成されるテレオペレーション対応ロボットアームシステムです。LeRobotフレームワークを使用することで、以下のことが可能になります：

- **テレオペレーション**: リーダーアームを手で動かすことで、フォロワーアームをリアルタイムで制御
- **データ収集**: 動作データを記録して機械学習用データセットを作成
- **模倣学習**: 収集したデータを使用してロボットに動作を学習させる

## 主な特徴

- ✅ **Windowsネイティブ対応**: WSL2不使用（USBレイテンシ問題の回避）
- ✅ **Feetech STS3215サーボモーター**: 6軸×2アーム（合計12モーター）
- ✅ **キャリブレーション**: 精密な動作制御のための自動キャリブレーション
- ✅ **テストスクリプト**: 動作確認・デバッグ用の便利なスクリプト群
- ✅ **詳細なドキュメント**: ステップバイステップのセットアップガイド

## クイックスタート

SO-101ロボットアームのセットアップとテレオペレーションまでの流れは以下の通りです。

### セットアップ手順

詳細な手順は **[setup.md](setup.md)** を参照してください。

1. **ツールのインストール** - uv、FFmpegをインストール
2. **依存関係のインストール** - `uv sync`で自動セットアップ
3. **ファームウェア更新** - Feetech公式ソフトウェアで更新
4. **モーターID設定** - リーダー・フォロワー各6個のモーターIDを設定
5. **キャリブレーション** - 両アームのキャリブレーション実行
6. **テレオペレーション** - リーダーアームでフォロワーアームを制御

### 最小限のコマンド例

```powershell
# 1. 依存関係のインストール
uv sync

# 2. 仮想環境の有効化
.venv\Scripts\Activate.ps1

# 3. リーダーアームのキャリブレーション
python -m lerobot.scripts.lerobot_calibrate --teleop.type=so101_leader --teleop.port=COM3 --teleop.id=my_awesome_leader_arm

# 4. フォロワーアームのキャリブレーション
python -m lerobot.scripts.lerobot_calibrate --robot.type=so101_follower --robot.port=COM4 --robot.id=my_awesome_follower_arm

# 5. テレオペレーション実行
python -m lerobot.scripts.lerobot_teleoperate \
  --robot.type=so101_follower --robot.port=COM4 --robot.id=my_awesome_follower_arm \
  --robot.cameras='{}' \
  --teleop.type=so101_leader --teleop.port=COM3 --teleop.id=my_awesome_leader_arm \
  --display_data=false
```

**⚠️ 重要**: 上記は最小限の例です。ファームウェア更新やモーターID設定など、必須の手順は **[setup.md](setup.md)** で確認してください。

## プロジェクト構成

```
SO101/
├── README.md              # このファイル
├── setup.md               # 詳細なセットアップガイド
├── pyproject.toml         # Pythonプロジェクト設定
├── .venv/                 # Python仮想環境
└── scripts/               # テスト・ユーティリティスクリプト
    ├── README.md          # スクリプトの詳細説明
    ├── test_follower_arm.py    # フォロワーアーム位置確認
    ├── test_leader_arm.py      # リーダーアーム位置確認
    ├── move_to_zero.py         # 0ポジションへ移動
    └── disable_torque.py       # トルク制御
```

## ドキュメント

- **[setup.md](setup.md)**: 完全なセットアップガイド
  - ツールのインストール
  - ファームウェア更新
  - モーターID設定
  - キャリブレーション
  - テレオペレーション
  - トラブルシューティング

- **[scripts/README.md](scripts/README.md)**: テストスクリプトの使い方

## テストスクリプト

### アーム位置の確認

```powershell
# フォロワーアームの位置をリアルタイム表示（トルクOFF）
python scripts\test_follower_arm.py

# リーダーアームの位置をリアルタイム表示（トルクOFF）
python scripts\test_leader_arm.py --port COM3
```

### 0ポジションへ移動

```powershell
# リーダーアームを0ポジション（中央位置）へ移動
python scripts\move_to_zero.py --type leader

# フォロワーアームを0ポジション（中央位置）へ移動
python scripts\move_to_zero.py --type follower --speed 10
```

### トルク制御

```powershell
# リーダーアームのトルクをOFF
python scripts\disable_torque.py --type leader --port COM3

# フォロワーアームのトルクをOFF
python scripts\disable_torque.py --type follower --port COM4
```

## 技術仕様

### ハードウェア

- **サーボモーター**: Feetech STS3215
  - リーダーアーム: ST-3215-C044, C001, C046 (7.4V)
  - フォロワーアーム: ST-3215-C001/C018/C047 (7.4V or 12V)
- **通信**: USB-TTL（1000000 baud）
- **ジョイント構成**: 6軸 × 2アーム
  1. shoulder_pan（肩パン）
  2. shoulder_lift（肩リフト）
  3. elbow_flex（肘フレックス）
  4. wrist_flex（手首フレックス）
  5. wrist_roll（手首ロール）
  6. gripper（グリッパー）

### ソフトウェア

- **Python**: 3.12-3.13（3.14は非対応）
- **LeRobot**: HuggingFace（mainブランチ）
- **PyTorch**: 2.7.x with CUDA 12.8
- **OpenCV**: 画像処理
- **Feetech SDK**: サーボモーター制御

## トラブルシューティング

### ポートが見つからない

```powershell
# COMポートを確認
python -m lerobot.scripts.lerobot_find_port
```

またはデバイスマネージャーで「ポート（COMとLPT）」を確認してください。

### キャリブレーションファイルが見つからない

キャリブレーションファイルの場所：
- リーダー: `C:\Users\<ユーザー名>\.cache\huggingface\lerobot\calibration\teleoperators\so101_leader\my_awesome_leader_arm.json`
- フォロワー: `C:\Users\<ユーザー名>\.cache\huggingface\lerobot\calibration\robots\so101_follower\my_awesome_follower_arm.json`

再キャリブレーションが必要な場合は、ファイルを削除してから再度キャリブレーションを実行してください。

### モーターIDが保存されない

LeRobotのPythonスクリプトではIDがEEPROMに保存されません。**必ずFeetech公式ソフトウェア（FD.exe）を使用**してください。

詳細なトラブルシューティングは[setup.MD](setup.MD)を参照してください。

## 参考資料

- [LeRobot公式リポジトリ](https://github.com/huggingface/lerobot)
- [Seeed Studio Wiki - LeRobot SO-100M](https://wiki.seeedstudio.com/lerobot_so100m/)
- [元記事（Zenn）](https://zenn.dev/komination/articles/464cb07be1b77f)

## ライセンス

このプロジェクトは、LeRobotフレームワークのライセンス（Apache License 2.0）に従います。

## 貢献

問題報告や改善提案は、Issueまたはプルリクエストでお願いします。

## 注意事項

⚠️ **電源の注意**
- STS3215 7.4Vモーター: 5V電源を使用
- STS3215 12Vモーター: 12V電源を使用
- 誤った電源を接続するとモーターが焼損する可能性があります

⚠️ **安全な操作**
- テレオペレーション中は、フォロワーアームの可動範囲に障害物がないことを確認してください
- 初めて動作させる場合は、低速（`--speed 10`）で開始してください
- 異常な動作や音がする場合は、すぐに電源を切ってください

---

**Happy Robot Learning! 🤖**
