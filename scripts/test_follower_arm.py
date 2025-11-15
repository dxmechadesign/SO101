"""
フォロワーアームの動作確認スクリプト
リアルタイムで各ジョイントの位置を表示します
トルクはOFFのままで動作します
"""
import time
import json
from pathlib import Path
from lerobot.robots.so101_follower.config_so101_follower import SO101FollowerConfig
from lerobot.motors.feetech import FeetechMotorsBus
from lerobot.motors import Motor, MotorNormMode, MotorCalibration

def test_follower_arm(port: str = "COM4", arm_id: str = "my_awesome_follower_arm"):
    """
    フォロワーアームに接続して位置情報を表示（トルクOFF）

    Args:
        port: COMポート
        arm_id: アームID
    """
    print(f"フォロワーアームに接続中...")
    print(f"ポート: {port}")
    print(f"アームID: {arm_id}")
    print("=" * 60)

    try:
        # 設定を作成
        config = SO101FollowerConfig(port=port, id=arm_id)

        # キャリブレーションファイルを読み込み
        calibration_path = Path.home() / ".cache" / "huggingface" / "lerobot" / "calibration" / "robots" / "so101_follower" / f"{arm_id}.json"
        calibration = {}

        if calibration_path.exists():
            print(f"\nキャリブレーションファイルを読み込み中: {calibration_path}")
            with open(calibration_path, 'r') as f:
                calib_data = json.load(f)
                for motor_name, calib in calib_data.items():
                    calibration[motor_name] = MotorCalibration(
                        id=calib['id'],
                        drive_mode=calib['drive_mode'],
                        homing_offset=calib['homing_offset'],
                        range_min=calib['range_min'],
                        range_max=calib['range_max']
                    )
            print("[成功] キャリブレーションファイルを読み込みました")
        else:
            print(f"\n[警告] キャリブレーションファイルが見つかりません: {calibration_path}")
            print("生のエンコーダ値（0-4095）を表示します")

        # モーターバスを直接作成（トルクをOFFのまま維持）
        bus = FeetechMotorsBus(
            port=config.port,
            motors={
                "shoulder_pan": Motor(1, "sts3215", MotorNormMode.DEGREES),
                "shoulder_lift": Motor(2, "sts3215", MotorNormMode.DEGREES),
                "elbow_flex": Motor(3, "sts3215", MotorNormMode.DEGREES),
                "wrist_flex": Motor(4, "sts3215", MotorNormMode.DEGREES),
                "wrist_roll": Motor(5, "sts3215", MotorNormMode.DEGREES),
                "gripper": Motor(6, "sts3215", MotorNormMode.RANGE_0_100),
            },
            calibration=calibration if calibration else None
        )

        # バスに接続
        bus.connect()

        # トルクをOFFにする
        print("\nトルクをOFFにしています...")
        bus.disable_torque()

        print(f"\n[成功] {arm_id} に接続しました！")
        print("\nフォロワーアームを手で動かしてください。")
        if calibration:
            print("正規化された位置情報（度数/パーセント）がリアルタイムで表示されます。")
            print("キャリブレーション時の中央位置が約0度になります。")
        else:
            print("生のエンコーダ値（0-4095）がリアルタイムで表示されます。")
        print("終了するには Ctrl+C を押してください。")
        print("=" * 60)
        print()

        # 位置情報を継続的に読み取り
        while True:
            # キャリブレーションがあれば正規化された値、なければ生の値
            if calibration:
                positions = bus.sync_read("Present_Position", normalize=True)
                unit = "°"
            else:
                positions = bus.sync_read("Present_Position", normalize=False)
                unit = ""

            # 表示（ジョイントごとに整形）
            print(f"\r現在位置: ", end="")
            for joint_name, position in positions.items():
                if joint_name == "gripper" and calibration:
                    print(f"{joint_name}: {position:6.1f}% | ", end="")
                else:
                    print(f"{joint_name}: {position:7.1f}{unit} | ", end="")

            time.sleep(0.1)  # 100msごとに更新

    except KeyboardInterrupt:
        print("\n\n終了します...")
    except Exception as e:
        print(f"\n[エラー] {e}")
        raise
    finally:
        try:
            bus.disconnect(disable_torque=True)
            print("[完了] フォロワーアームから切断しました")
        except:
            pass

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="フォロワーアームの動作確認")
    parser.add_argument("--port", type=str, default="COM4", help="COMポート (デフォルト: COM4)")
    parser.add_argument("--id", type=str, default="my_awesome_follower_arm",
                       help="アームID (デフォルト: my_awesome_follower_arm)")

    args = parser.parse_args()

    test_follower_arm(port=args.port, arm_id=args.id)
