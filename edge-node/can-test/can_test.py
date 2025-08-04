from can_bus import CAN_Bus
import time

TX_ID = 0x256

def main():

    can0 = CAN_Bus(channel="can0", bitrate=500_000)

    try:
        while True: 
            msg = can0.receive_data()
            if msg:
                print(f"\nRecieved on can0.")

            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        can0.disable_can()

if __name__ == "__main__":
    main()      