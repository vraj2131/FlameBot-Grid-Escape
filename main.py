from environment import ShipEnvironment

def main():
    env = ShipEnvironment(grid_size=40)
    
    env.create_environment()

if __name__ == "__main__":
    main()
