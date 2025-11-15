"""
すべてのモーターのトルクをOFFにするスクリプト
"""
import argparse
from lerobot.teleoperators.so101_leader.so101_leader import SO101Leader
from lerobot.teleoperators.so101_leader.config_so101_leader import SO101LeaderConfig
from lerobot.robots.so101_follower.so101_follower import SO101Follower
from lerobot.robots.so101_follower.config_so101_follower import SO101FollowerConfig

def disable_torque_leader(port: str = "COM3", arm_id: str = "my_awesome_leader_arm"):
    """
    リーダーアームのトルクをOFF

    Args:
        port: COMポート
        arm_id: アームID
    """
    print(f"リーダーアームのトルクをOFFにします")
    print(f"ポート: {port}")
    print(f"アームID: {arm_id}")
    print("=" * 60)

    try:
        # 設定を作成
        config = SO101LeaderConfig(port=port, id=arm_id)

        # リーダーアームに接続
        leader = SO101Leader(config)
        leader.connect(calibrate=False)

        print(f"\n[成功] {arm_id} に接続しました")

        # トルクをOFF
        print("\nトルクを無効化中...")
        leader.bus.disable_torque()
        print("[完了] すべてのモーターのトルクをOFFにしました")

        # 切断
        leader.disconnect()
        print("[完了] 切断しました\n")

    except Exception as e:
        print(f"\n[エラー] {e}")
        import traceback
        traceback.print_exc()

def disable_torque_follower(port: str = "COM4", arm_id: str = "my_awesome_follower_arm"):
    """
    フォロワーアームのトルクをOFF

    Args:
        port: COMポート
        arm_id: アームID
    """
    print(f"フォロワーアームのトルクをOFFにします")
    print(f"ポート: {port}")
    print(f"アームID: {arm_id}")
    print("=" * 60)

    try:
        # 設定を作成
        config = SO101FollowerConfig(port=port, id=arm_id)

        # フォロワーアームに接続
        follower = SO101Follower(config)
        follower.connect(calibrate=False)

        print(f"\n[成功] {arm_id} に接続しました")

        # トルクをOFF
        print("\nトルクを無効化中...")
        follower.bus.disable_torque()
        print("[完了] すべてのモーターのトルクをOFFにしました")

        # 切断
        follower.disconnect()
        print("[完了] 切断しました\n")

    except Exception as e:
        print(f"\n[エラー] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="モーターのトルクをOFFにする")
    parser.add_argument("--type", type=str, required=True, choices=["leader", "follower"],
                       help="アームタイプ: leader または follower")
    parser.add_argument("--port", type=str, required=True, help="COMポート (例: COM3)")
    parser.add_argument("--id", type=str, default=None,
                       help="アームID (省略時: デフォルトID)")

    args = parser.parse_args()

    if args.type == "leader":
        arm_id = args.id if args.id else "my_awesome_leader_arm"
        disable_torque_leader(port=args.port, arm_id=arm_id)
    else:
        arm_id = args.id if args.id else "my_awesome_follower_arm"
        disable_torque_follower(port=args.port, arm_id=arm_id)
