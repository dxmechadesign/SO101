"""
リーダーアームの動作確認スクリプト
リアルタイムで各ジョイントの位置を表示します
"""
import time
from lerobot.teleoperators.so101_leader.so101_leader import SO101Leader
from lerobot.teleoperators.so101_leader.config_so101_leader import SO101LeaderConfig

def test_leader_arm(port: str = "COM3", arm_id: str = "my_awesome_leader_arm"):
    """
    リーダーアームに接続して位置情報を表示

    Args:
        port: COMポート
        arm_id: アームID
    """
    print(f"リーダーアームに接続中...")
    print(f"ポート: {port}")
    print(f"アームID: {arm_id}")
    print("=" * 60)

    try:
        # 設定を作成
        config = SO101LeaderConfig(port=port, id=arm_id)

        # リーダーアームに接続
        leader = SO101Leader(config)
        leader.connect(calibrate=False)  # キャリブレーション済みなのでスキップ

        print(f"\n[成功] {arm_id} に接続しました！")
        print("\nリーダーアームを手で動かしてください。")
        print("位置情報がリアルタイムで表示されます。")
        print("終了するには Ctrl+C を押してください。")
        print("=" * 60)
        print()

        # 位置情報を継続的に読み取り
        while True:
            # 現在の位置を読み取り
            action = leader.get_action()

            # 表示（ジョイントごとに整形）
            print(f"\r現在位置: ", end="")
            for joint_name, position in action.items():
                # .posを除いたジョイント名を表示
                name = joint_name.replace('.pos', '')
                print(f"{name}: {position:7.2f} | ", end="")

            time.sleep(0.1)  # 100msごとに更新

    except KeyboardInterrupt:
        print("\n\n終了します...")
    except Exception as e:
        print(f"\n[エラー] {e}")
        raise
    finally:
        try:
            leader.disconnect()
            print("[完了] リーダーアームから切断しました")
        except:
            pass

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="リーダーアームの動作確認")
    parser.add_argument("--port", type=str, default="COM3", help="COMポート (デフォルト: COM3)")
    parser.add_argument("--id", type=str, default="my_awesome_leader_arm",
                       help="アームID (デフォルト: my_awesome_leader_arm)")

    args = parser.parse_args()

    test_leader_arm(port=args.port, arm_id=args.id)
