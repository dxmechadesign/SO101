# SO-101 テストスクリプト

このフォルダには、SO-101ロボットアームのテストと制御用スクリプトが含まれています。

## スクリプト一覧

### test_follower_arm.py
フォロワーアームの位置をリアルタイムで表示します（トルクOFF状態）。

**使用方法:**
```powershell
python scripts\test_follower_arm.py
```

**オプション:**
- `--port`: COMポート（デフォルト: COM4）
- `--id`: アームID（デフォルト: my_awesome_follower_arm）

**機能:**
- キャリブレーション済みの場合、正規化された位置（度数/パーセント）を表示
- キャリブレーション時の中央位置が約0度として表示
- 手でアームを動かしながら各ジョイントの角度を確認可能
- Ctrl+Cで終了

---

### test_leader_arm.py
リーダーアームの位置をリアルタイムで表示します（トルクOFF状態）。

**使用方法:**
```powershell
python scripts\test_leader_arm.py
```

**オプション:**
- `--port`: COMポート（デフォルト: COM3）
- `--id`: アームID（デフォルト: my_awesome_leader_arm）

**機能:**
- リーダーアームの各ジョイント位置をリアルタイム表示
- Ctrl+Cで終了

---

### move_to_zero.py
アーム（リーダー/フォロワー）を0ポジション（キャリブレーション時の中央位置）へ自動的に移動します。

**使用方法:**
```powershell
# リーダーアームを0ポジションへ移動
python scripts\move_to_zero.py --type leader

# フォロワーアームを0ポジションへ移動
python scripts\move_to_zero.py --type follower
```

**オプション:**
- `--type`: アームタイプ（leader / follower、デフォルト: leader）
- `--port`: COMポート（デフォルト: leader=COM3, follower=COM4）
- `--id`: アームID（デフォルト: 自動設定）
- `--speed`: 移動速度 1-100%（デフォルト: 10 = 超低速）

**動作の流れ:**
1. すべてのモーターのトルクをOFFにする
2. 1軸目（shoulder_pan）のみトルクON → 0ポジションへ移動
3. 2軸目（shoulder_lift）のみトルクON → 0ポジションへ移動（1軸目はトルクONのまま保持）
4. 以下同様に6軸まで順番に移動
5. すべてのジョイントが0ポジションに到達
6. Enterキーを押すとトルクをOFFにして終了

**注意:**
- 移動中、まだ動いていないモーターはトルクOFFでフリー状態になります（干渉防止）
- 移動完了後、すべてのモーターはトルクONで0ポジションを保持します

---

### disable_torque.py
アームのトルクを手動でOFF/ONします。

**使用方法:**
```powershell
# リーダーアームのトルクをOFF
python scripts\disable_torque.py --type leader --port COM3

# フォロワーアームのトルクをOFF
python scripts\disable_torque.py --type follower --port COM4
```

**オプション:**
- `--type`: アームタイプ（leader / follower）
- `--port`: COMポート
- `--id`: アームID（オプション）

**機能:**
- すべてのモーターのトルクをOFFにして、手で自由に動かせる状態にします
- キャリブレーション時にトルクがONになってしまった場合の対処に使用

---

## 実行前の準備

すべてのスクリプトを実行する前に、仮想環境を有効化してください：

```powershell
.venv\Scripts\Activate.ps1
```

## キャリブレーションについて

これらのスクリプトを使用する前に、アームのキャリブレーションが完了している必要があります。
キャリブレーション方法は、プロジェクトルートの[setup.MD](../setup.MD)を参照してください。
