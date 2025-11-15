"""
アーム（リーダー/フォロワー）を0ポジション（中央位置）へ低速で移動するスクリプト
"""
import time
from lerobot.teleoperators.so101_leader.so101_leader import SO101Leader
from lerobot.teleoperators.so101_leader.config_so101_leader import SO101LeaderConfig
from lerobot.robots.so101_follower.so101_follower import SO101Follower
from lerobot.robots.so101_follower.config_so101_follower import SO101FollowerConfig

def move_to_zero_position(arm_type: str = "leader", port: str = "COM3", arm_id: str = None, speed: int = 10):
    """
    アームを0ポジション（中央位置）へ低速で移動

    Args:
        arm_type: "leader" または "follower"
        port: COMポート
        arm_id: アームID
        speed: 移動速度 (0-100, デフォルト: 10 = 超低速)
    """
    # デフォルトのarm_idを設定
    if arm_id is None:
        arm_id = "my_awesome_leader_arm" if arm_type == "leader" else "my_awesome_follower_arm"

    print(f"{arm_type.capitalize()}アームを0ポジションへ移動します")
    print(f"ポート: {port}")
    print(f"アームID: {arm_id}")
    print(f"速度: {speed}%")
    print("=" * 60)

    try:
        # アームタイプに応じて設定を作成
        if arm_type == "leader":
            config = SO101LeaderConfig(port=port, id=arm_id)
            arm = SO101Leader(config)
            arm.connect(calibrate=False)
            get_position = lambda: arm.get_action()
        elif arm_type == "follower":
            config = SO101FollowerConfig(port=port, id=arm_id)
            arm = SO101Follower(config)
            arm.connect(calibrate=False)
            # フォロワーの場合、observationからモーター位置のみを抽出
            get_position = lambda: {k: v for k, v in arm.get_observation().items() if k.endswith('.pos')}
        else:
            raise ValueError(f"無効なarm_type: {arm_type} (leader または follower を指定してください)")

        print(f"\n[成功] {arm_id} に接続しました！")

        # 現在位置を取得
        current_positions = get_position()
        print("\n現在位置:")
        for joint_name, position in current_positions.items():
            name = joint_name.replace('.pos', '')
            print(f"  {name}: {position:7.2f}")

        print("\n目標位置: すべてのジョイントを 0.0 に設定")
        print("動作方法: 1軸ずつ順番に移動（干渉防止）")

        # 移動速度を設定
        # Goal_Velocity: 移動速度を制御 (0-4095, 値が大きいほど速い)
        print(f"\n移動速度を設定中... ({speed}%)")

        # speedに応じて移動速度を計算
        velocity_value = int(4095 * speed / 100)

        for motor in arm.bus.motors:
            arm.bus.write("Goal_Velocity", motor, velocity_value, normalize=False)

        print(f"移動速度を設定しました (Goal_Velocity: {velocity_value})")

        # モーター順序（shoulder_pan, shoulder_lift, elbow_flex, wrist_flex, wrist_roll, gripper）
        motor_names = list(arm.bus.motors.keys())

        # 最初に全モーターのトルクをOFFにする
        print("\nすべてのモーターのトルクをOFFにしています...")
        arm.bus.disable_torque()
        print("トルクをOFFにしました")

        print("\n0ポジションへ移動開始...")
        print("=" * 60)

        # 1軸ずつ順番に移動
        for i, motor in enumerate(motor_names, 1):
            print(f"\n[{i}/{len(motor_names)}] {motor} を移動中...")

            # このモーターのみトルクON、他はOFFのまま
            arm.bus.write("Torque_Enable", motor, 1, normalize=False)

            # 目標位置を0に設定
            arm.bus.write("Goal_Position", motor, 0.0)

            # 移動完了を監視
            moving = True
            timeout_count = 0
            max_timeout = 50  # 10秒タイムアウト（0.2秒 × 50回）

            while moving and timeout_count < max_timeout:
                time.sleep(0.2)

                # 現在位置を取得
                current_positions = get_position()
                current_pos = current_positions[f"{motor}.pos"]

                # 移動状態を表示
                print(f"\r  {motor}: {current_pos:6.2f} → 0.00", end="")

                # 目標位置に到達したか確認（許容誤差: 5.0に拡大）
                if abs(current_pos - 0.0) < 5.0:
                    moving = False
                else:
                    timeout_count += 1

            print(f"  [完了]")
            # このモーターはトルクONのまま維持

        print("\n" + "=" * 60)
        print("[完了] すべてのジョイントが0ポジションに到達しました！")

        # 最終位置を表示
        final_positions = get_position()
        print("\n最終位置:")
        for joint_name, position in final_positions.items():
            name = joint_name.replace('.pos', '')
            print(f"  {name}: {position:7.2f}")

        # すべてのモーターのトルクはONのまま保持
        print("\n注意: すべてのモーターのトルクはONのままです")
        print("      0ポジションを保持しています")
        print("\nEnterキーを押すとトルクをOFFにして終了します...")

        # Enterキー待ち
        try:
            input()
        except:
            pass

        # トルクをOFF
        print("\nトルクを無効化中...")
        arm.bus.disable_torque()
        print("トルクを無効化しました")

        # 切断
        arm.disconnect()
        print(f"\n[完了] {arm_type.capitalize()}アームから切断しました")

    except KeyboardInterrupt:
        print("\n\n[中断] ユーザーによって中断されました")
        try:
            arm.bus.disable_torque()
            arm.disconnect()
        except:
            pass
    except Exception as e:
        print(f"\n[エラー] {e}")
        import traceback
        traceback.print_exc()
        try:
            arm.bus.disable_torque()
            arm.disconnect()
        except:
            pass
        raise

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="アームを0ポジションへ移動")
    parser.add_argument("--type", type=str, default="leader", choices=["leader", "follower"],
                       help="アームタイプ: leader または follower (デフォルト: leader)")
    parser.add_argument("--port", type=str, default=None,
                       help="COMポート (デフォルト: leader=COM3, follower=COM4)")
    parser.add_argument("--id", type=str, default=None,
                       help="アームID (デフォルト: leader=my_awesome_leader_arm, follower=my_awesome_follower_arm)")
    parser.add_argument("--speed", type=int, default=10, choices=range(1, 101),
                       help="移動速度 1-100%% (デフォルト: 10 = 超低速)")

    args = parser.parse_args()

    # デフォルトのポートを設定
    if args.port is None:
        args.port = "COM3" if args.type == "leader" else "COM4"

    move_to_zero_position(arm_type=args.type, port=args.port, arm_id=args.id, speed=args.speed)
